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
    contour = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contour = cv.erode(contour, np.ones((3, 3)), iterations=2)
    contour = cv.morphologyEx(contour, cv.MORPH_GRADIENT, np.ones((4, 4)))
    ret, contour = cv.threshold(contour, 15, 255, cv.THRESH_BINARY)
    #  contour = cv.morphologyEx(contour, cv.MORPH_CLOSE, np.ones((5, 5)))
    #  contour = ~cv.adaptiveThreshold(contour,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,3,2)
    #  contour = cv.dilate(contour, np.ones((3, 3)))
    #  contour = cv.erode(contour, np.ones((3, 3)))
    #  contour = cv.morphologyEx(contour, cv.MORPH_CLOSE, np.ones((3, 3)))
    contour = ~contour

    cv.imshow('contour', contour)

    fillmorph = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))

    @static_vars(pick_color=True, picked_color=[255, 255, 255])
    def handler(event, x, y, flags, param):
        nonlocal fillmorph, image, contour

        if event == cv.EVENT_LBUTTONDOWN:
            if (handler.pick_color):
                handler.pick_color = False
                handler.picked_color = image[y][x]
                print("Picked color: ", handler.picked_color)
            else:
                print("Filling with color")
                mask = np.zeros_like(contour)
                mask[y][x] = 1
                while True:
                    new_fill = cv.dilate(mask, fillmorph) & contour
                    if np.array_equal(new_fill, mask):
                        break
                    else:
                        mask = new_fill

                reverse_mask = ((1 - cv.merge((mask, mask, mask)))*(-1)).astype(np.uint8)
                colored_mask = cv.merge((mask*handler.picked_color[0], mask*handler.picked_color[1], mask*handler.picked_color[2]))
                image = (image & reverse_mask) + colored_mask
                print("Filled with color")
                #  cv.imshow('colored_mask', colored_mask)

                showImage(image)
                handler.pick_color = True

    showImage(image)
    return handler

img = cv.imread('./rocket.jpg', 1)

cv.namedWindow('image')
cv.setMouseCallback('image', floodFill(img, lambda image: cv.imshow('image', image)))

while(1):
    k = cv.waitKey(0) & 0xFF
    if k == ord('q') or k == 27:
        break

cv.destroyAllWindows()
