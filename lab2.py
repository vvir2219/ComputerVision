#!/usr/local/bin/python3

__author__ = 'vlad'
import numpy as np
import cv2 as cv
import sys
import time
import platform
print(cv.__version__)
print(platform.architecture())

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def floodFill(image, showImage):
    kernel = np.ones((5,5),np.uint8)
    grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contour = cv.morphologyEx(grayimg, cv.MORPH_GRADIENT, kernel)
    ret, thresh = cv.threshold(contour, 15, 255, cv.THRESH_BINARY)
    contour = ~cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    #  cv.imshow('contour', contour)

    fillmorph = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))

    @static_vars(pick_color=True, picked_color=[255, 255, 255])
    def handler(event, x, y, flags, param):
        nonlocal fillmorph, image, contour

        if event == cv.EVENT_LBUTTONDOWN:
            if (handler.pick_color):
                handler.pick_color = False
                handler.picked_color = image[y][x]
            else:
                fill = np.zeros_like(contour)
                fill[y][x] = 255
                while True:
                    new_fill = cv.dilate(fill, fillmorph) & contour
                    if np.array_equal(new_fill, fill):
                        break
                    else:
                        fill = new_fill

                B = np.vectorize(lambda x: handler.picked_color[0] if x > 0 else np.uint8(0))
                G = np.vectorize(lambda x: handler.picked_color[1] if x > 0 else np.uint8(0))
                R = np.vectorize(lambda x: handler.picked_color[2] if x > 0 else np.uint8(0))

                image |= cv.merge((B(fill), G(fill), R(fill)))
                showImage()

                handler.picked_color = False

    showImage()
    return handler

img = cv.imread('./rocket.jpg', 1)

cv.namedWindow('image')
cv.setMouseCallback('image', floodFill(img, lambda: cv.imshow('image', img)))

while(1):
    k = cv.waitKey(0) & 0xFF
    if k == ord('q') or k == 27:
        break

cv.destroyAllWindows()
