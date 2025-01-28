# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 08:47:53 2019

@author: bkeelson
"""


""" IMPORTS """

import cv2
import numpy as np


""" FUNCTIONS """

drawing = False #when true mouse is pressed
mode = True # when true we draw rectangle else we draw a circle toggle using m
ix,iy = -1,-1
#mouse callback function
def draw_shape(event, x, y, flags, param):
    global ix,iy,mode,drawing
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # activate drawing on nouse movement
        drawing = True
        # set location of left upper corner of rectangle
        ix, iy = x, y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode == True:
                # make a copy of the image
                # Question: is this the most efficient way to draw the temporary ractangle? 
                # Hint: copying images is computationally expensive and needs to be done only if there is no other option.
                tmp = img.copy()
                # draw the temporary rectangle on the image copy
                cv2.rectangle(tmp, (ix,iy), (x,y), (0,100,0), -1)
                # show temporary image
                cv2.imshow('image', tmp)
            else:
                # draw circle on image
                cv2.circle(img, (x,y), 5, (255,0,0), -1)
                # show image
                cv2.imshow('image', img)
                
    elif event == cv2.EVENT_LBUTTONUP:
        # deactivate drawing om mouse movement
        drawing = False
        if mode == True:
            # draw final rectangle on image
            cv2.rectangle(img, (ix,iy), (x,y), (0,255,0), -1)   
            # show image
            cv2.imshow('image', img)
            
            
""" MAIN """

if __name__ == "__main__":

    events= [i for i in dir(cv2) if 'EVENT' in i]
    # print(events)
    
    img = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_shape)
    cv2.imshow('image', img)
    
    while(1):
        k = cv2.waitKey(50) &0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break
        
    cv2.destroyAllWindows()
