import torch
from tracker import Tracker, mynet
import numpy as np
import cv2
import time
def draw_circle(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing, init, flag, iamge, start

    #if init is False:
    if 1:
        if event == cv2.EVENT_LBUTTONDOWN and flag == 1:
            drawing = True
            x1, y1 = x, y
            x2, y2 = -1, -1
            flag = 2
            
            init = False    
            
        #print(init)
        x2, y2 = x, y
        #if event == cv2.EVENT_LBUTTONDOWN and flag == 2:
            #if drawing is True:
                #x2, y2 = x, y
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
        
def run():       
    global x1, y1, x2, y2, drawing, init, flag, image, getim, start
    flag=1
    init = False
    drawing = False
    getim = False
    start = False
    x1, x2, y1, y2 = -1, -1, -1, -1
    flag_lose = False
    count_lose = 0
    net = mynet()

    net.load_state_dict(torch.load('../alex_slim.model'))
    net.eval().cuda()
    mytracker = Tracker(net)
    x = torch.Tensor(1,3,127,127).cuda()
    net.template(x)
    x = torch.Tensor(1,3,271,271).cuda()
    net.track(x)
    
    cap = cv2.VideoCapture(2)
    cap.set(3,1280)
    cap.set(4,720)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)
    tz = 0.0
    i = 0
    fps = 'fps=0'
    while(1):

        ret, image = cap.read()
        if drawing is True:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if start is False and init is True:
            init_rect = np.array([x1,y1,x2-x1,y2-y1])
            mytracker.init(image, init_rect)
            start = True
            continue

        if start is True:
            t1 = time.time()
            outputs = mytracker.track(image)
            t2 = time.time()-t1
            print(t2)
            tz = tz+t2
            i = i + 1
            bbox = list(map(int, outputs['bbox']))
            res = bbox

            if i>=20:
                print(tz/20)
                i = 0
                fps = 'fps=' + str(20/tz)
                tz = 0.0
                
            cv2.rectangle(image, (res[0], res[1]), (res[0] + res[2], res[1] + res[3]), (0, 255, 255), 2)
            cv2.putText(image, fps, (0,20), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (255,0,0), 2)
        cv2.imshow('image', image)
        cv2.waitKey(1)


if __name__ == '__main__':
    run()


