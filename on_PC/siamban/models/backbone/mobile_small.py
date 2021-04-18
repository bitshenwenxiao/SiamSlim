from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
import torch.nn as nn
import torch.nn.functional as F
from siamban.models.backbone.alexnet import AlexNet2
import time
def conv_bn(inp, oup, stride, padding=1):
    return nn.Sequential(
        nn.Conv2d(inp, oup, 3, stride, padding, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True)
    )


def conv_1x1_bn(inp, oup):
    return nn.Sequential(
        nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True)
    )


class InvertedResidual(nn.Module):
    def __init__(self, inp, oup, stride, expand_ratio, dilation=1):
        super(InvertedResidual, self).__init__()
        self.stride = stride

        self.use_res_connect = self.stride == 1 and inp == oup

        padding = 2 - stride
        if dilation > 1:
            padding = dilation

        self.conv = nn.Sequential(
            # pw
            nn.Conv2d(inp, inp * expand_ratio, 1, 1, 0, bias=False),
            nn.BatchNorm2d(inp * expand_ratio),
            nn.ReLU6(inplace=True),
            # dw
            nn.Conv2d(inp * expand_ratio, inp * expand_ratio, 3,
                      stride, padding, dilation=dilation,
                      groups=inp * expand_ratio, bias=False),
            nn.BatchNorm2d(inp * expand_ratio),
            nn.ReLU6(inplace=True),
            # pw-linear
            nn.Conv2d(inp * expand_ratio, oup, 1, 1, 0, bias=False),
            nn.BatchNorm2d(oup),
        )

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)


class MobileNetV2(nn.Sequential):
    def __init__(self, width_mult=1.0, used_layers=[3, 5, 7]):
        super(MobileNetV2, self).__init__()

        self.interverted_residual_setting = [
            # t, c, n, s
            [1, 16, 1, 1, 1],
            [6, 24, 2, 2, 1],
            [6, 32, 3, 2, 1],
            [6, 64, 4, 2, 1],
            [6, 96, 3, 1, 1],
            [6, 160, 3, 2, 1],
            [6, 320, 1, 1, 1],
        ]
        # 0,2,3,4,6

        self.interverted_residual_setting = [
            # t, c, n, s
            [1, 8, 1, 1, 1],
            [6, 12, 1, 2, 1],
            [6, 16, 1, 2, 1],
            [6, 32, 1, 1, 2],
            [6, 48, 1, 1, 2],
            [6, 32, 1, 1, 4],
            [6, 64, 1, 1, 4],
        ]
        self.ad3 = nn.Conv2d(16, 64, kernel_size=1)
        self.ad5 = nn.Conv2d(48, 64, kernel_size=1)
        self.ad7 = nn.Conv2d(64, 64, kernel_size=1)
        #self.channels = [24, 32, 96, 320]
        #self.channels = [int(c * width_mult) for c in self.channels]

        input_channel = int(16 * width_mult)
        self.last_channel = int(1280 * width_mult) \
            if width_mult > 1.0 else 1280

        self.add_module('layer0', conv_bn(3, input_channel, 2, 0))

        last_dilation = 1

        self.used_layers = used_layers

        for idx, (t, c, n, s, d) in \
                enumerate(self.interverted_residual_setting, start=1):
            output_channel = int(c * width_mult)

            layers = []

            for i in range(n):

                if i == 0:
                    if d == last_dilation:
                        dd = d
                    else:
                        dd = max(d // 2, 1)
                    layers.append(InvertedResidual(input_channel,
                                                   output_channel, s, t, dd))
                else:
                    layers.append(InvertedResidual(input_channel,
                                                   output_channel, 1, t, d))
                input_channel = output_channel

            last_dilation = d

            self.add_module('layer%d' % (idx), nn.Sequential(*layers))



    def forward(self, x):
        outputs = []

        #print(x.shape)
        for idx in range(8):
            name = "layer%d" % idx
            x = getattr(self, name)(x)
            #print(x.shape)
            outputs.append(x)
        out3 = self.ad3(outputs[3])
        out5 = self.ad5(outputs[5])
        out7 = self.ad7(outputs[7])

        out = torch.cat([out3, out5, out7], dim=1)
        return out


def mobilenetv2(**kwargs):
    model = MobileNetV2(**kwargs)
    return model


if __name__ == '__main__':
    net = mobilenetv2()
    net2 = AlexNet2().cuda()

    #print(net)

    tensor = torch.Tensor(1, 3, 255, 255).cuda()
    net = net.cuda()


    net2(tensor)
    if 1:
        tensor = torch.Tensor(1, 3, 255, 255).cuda()
        net = net.cuda()
        t1 = time.time()
        for i in range(0, 100):
            net(tensor)
            torch.cuda.synchronize()
        t2 = time.time()
        print(t2-t1)

        tensor = torch.Tensor(1, 3, 271, 271).cuda()
        net2(tensor)
        t1 = time.time()
        for i in range(0, 100):
            net2(tensor)
            torch.cuda.synchronize()
        t2 = time.time()
        print(t2 - t1)

