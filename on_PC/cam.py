from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import argparse

import cv2
import torch
import numpy as np
import random
from siamban.core.config import cfg
from siamban.models.model_builder import ModelBuilder
from siamban.tracker.tracker_builder import build_tracker



def draw_circle(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing, init, flag, iamge, start

    if 1:
        if event == cv2.EVENT_LBUTTONDOWN and flag == 1:
            drawing = True
            x1, y1 = x, y
            x2, y2 = -1, -1
            flag = 2
            
            init = False    
        x2, y2 = x, y
        if event == cv2.EVENT_LBUTTONUP and flag == 2:
            w = x2-x1
            h = y2 -y1
            if w>0 and w*h>50:
                init = True   
                start = False   
                flag = 1
                drawing = False
                print(init)
                print([x1,y1,x2,y2])
            else:
                x1, x2, y1, y2 = -1, -1, -1, -1
        if drawing is True:
            x2, y2 = x, y
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
  
    if event == cv2.EVENT_MBUTTONDOWN:
        flag = 1
        init = False
        x1, x2, y1, y2 = -1, -1, -1, -1

# load net
parser = argparse.ArgumentParser(description='tracking demo')
parser.add_argument('--config', type=str, help='config file', default='./experiments/slim_alex/config.yaml')
args = parser.parse_args()
def test():
    
    global x1, y1, x2, y2, drawing, init, flag, image, getim, start
    cfg.merge_from_file(args.config)
    flag=1
    init = False
    drawing = False
    getim = False
    start = False
    x1, x2, y1, y2 = -1, -1, -1, -1
    flag_lose = False
    count_lose = 0

    model = ModelBuilder()
    model.load_state_dict(torch.load('../alex_slim.model'))
    model.eval().cuda()
    tracker = build_tracker(model)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)
    while(1):

        ret, image = cap.read()
        if drawing is True:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if start is False and init is True:
            init_rect = np.array([x1,y1,x2-x1,y2-y1])
            tracker.init(image, init_rect)
            start = True
            continue

        if start is True:
            outputs = tracker.track(image)
            bbox = list(map(int, outputs['bbox']))
            res = bbox

            cv2.rectangle(image, (res[0], res[1]), (res[0] + res[2], res[1] + res[3]), (0, 255, 255), 2)

        cv2.imshow('image', image)
        cv2.waitKey(1)

if __name__ == '__main__':
    test()



