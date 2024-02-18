import cv2
import numpy as np
method=[cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR,
            cv2.TM_CCOEFF_NORMED,cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]


class preprocess:
    def __init__(self,image=None,contours=None,contourCropBoundary=None):
        self.image=image
        self.contours=contours
        self.contourCropBoundary=contourCropBoundary

    def contoursfind(self):
        BWimage=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        cannyimg=cv2.Canny(BWimage,50,150,apertureSize=5)
        contours,hierarchy=cv2.findContours(cannyimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        return contours
    
    def biggestContour(self):
        biggest=np.array([])
        max_area=0
        for i in self.contours:
            area=cv2.contourArea(i)
            if area > 50:
                peri = cv2.arcLength(i,True)
                approx=cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                    biggest=approx
                    max_area=area
        return biggest

    def cropImg(self):
        if self.contourCropBoundary.size!=0:
            x,y,w,h=cv2.boundingRect(self.contourCropBoundary)
            return x,y,w,h

class drow:
    def __init__(self,image,xpoint,ypoint,width,height):
        self.image=image
        self.xpoint=xpoint
        self.ypoint=ypoint
        self.width=width
        self.height=height

    def guidline(self):
        
        xspace=int(self.width/8)
        xlocation=int(xspace/2)
        yspace=int(self.height/8)
        ylocation=int(yspace/2)
        image=self.image
        for i in range(0,8):
            image=cv2.line(image,(xlocation,0),(xlocation,int(self.height)),(0,255,0),thickness=1)
            xlocation=xlocation+xspace
            image=cv2.line(image,(0,ylocation),(int(self.width),ylocation),(0,255,0),thickness=1)
            ylocation=ylocation+yspace
        
        return image
        

class objfinder:
    def __init__(self,chessman,feedimg):
        self.chessman=chessman
        self.feedimg=feedimg

    def finder(self):
        screenshot=np.array(self.feedimg)
        feedimg1=cv2.cvtColor(screenshot,cv2.COLOR_BGR2GRAY)
        tempchessman=self.chessman
        w,h=tempchessman.shape[::-1]

        board = cv2.matchTemplate(feedimg1,tempchessman,method[3])
        location = np.where(board>=0.6)
        loc=zip(*location[::-1])
        return loc,w,h