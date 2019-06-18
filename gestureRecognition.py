import cv2
import numpy as np
import math

black = (0,0,0)
white = (255,255,255)

capture = cv2.VideoCapture(0)
while(capture.isOpened()) :
    ret,img = capture.read()

    grayscale_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gaussian_blur_frame = cv2.GaussianBlur(grayscale_frame,(5,5),0)
    ret,thresh = cv2.threshold(gaussian_blur_frame,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    abc, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0
    for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if(area>max_area):
                max_area=area
                contour_index=i
    contour=contours[contour_index]
    hull = cv2.convexHull(contour)
    moments = cv2.moments(contour)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    center=(cx,cy)       
    cv2.circle(img,center,5,[0,0,255],2)       
    cv2.drawContours(drawing,[contour],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
    contour = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    hull = cv2.convexHull(contour,returnPoints = False)
    
    if(1):
        defects = cv2.convexityDefects(contour,hull)
        mind=0
        maxd=0
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            dist = cv2.pointPolygonTest(contour,center,True)
            cv2.line(img,start,end,[0,255,0],2)
            cv2.circle(img,far,5,[0,0,255],-1)
            print(e)
            
            
    cv2.imshow('output',drawing)
    cv2.imshow('input',img)

    k = cv2.waitKey(10)
    if k==27:
        break