#!/usr/local/bin/python3

__author__ = 'vlad'
import numpy as np
import cv2 as cv
import sys
import time
import platform
print(cv.__version__)
print(platform.architecture())

img = cv.imread('./rocket.jpg', 1)

def mouseHandler(image):
    def handler(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print(x, y)

    return handler

cv.namedWindow('image')
cv.setMouseCallback('image', mouseHandler(img))

kernel = np.ones((3,3),np.uint8)
grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#  cv.imshow('grayimg', grayimg)

#  thr = cv.adaptiveThreshold(grayimg, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
#  cv.imshow('thr', thr)
#  
#  closing = cv.morphologyEx(thr, cv.MORPH_CLOSE, kernel)
#  cv.imshow('closing', closing)
#  
#  erode = cv.erode(thr, kernel, iterations=1)
#  cv.imshow('erode', erode)

contour = cv.dilate(grayimg, np.ones((5,5), np.uint8), iterations=1) - \
          cv.erode(grayimg, np.ones((5,5), np.uint8), iterations=1)
#  cv.imshow('contour', contour)

ret, thresh = cv.threshold(contour, 15, 255, cv.THRESH_BINARY)
#  thres = cv.adaptiveThreshold(contour, 30, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 19, 7)


def floodFill(image):
    kernel = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))

    def handler(event, x, y, flags, param):
        nonlocal kernel, image

        if event == cv.EVENT_LBUTTONDOWN:
            fill = np.zeros_like(image)
            fill[y][x] = 255
            while True:
                new_fill = cv.dilate(fill, kernel) & ~image
                if np.array_equal(new_fill, fill):
                    break
                else:
                    fill = new_fill

            image |= fill
            print(x, y)

    return handler

contour = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

cv.namedWindow('contour')
cv.setMouseCallback('contour', floodFill(contour))

while(1):
    cv.imshow('contour',contour)
    k = cv.waitKey(0) & 0xFF

    if k == ord('q') or k == 27:
        break

cv.destroyAllWindows()
