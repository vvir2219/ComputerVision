__author__ = 'vlad'
import numpy as np
import cv2
import sys
import time
import platform
from matplotlib import pyplot as plt

print(cv2.__version__)
print(platform.architecture())

img = cv2.imread('./logo.png', 1)
img_height, img_width, _= img.shape

mask = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
_, mask = cv2.threshold(mask, 190, 255, cv2.THRESH_BINARY)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
cv2.imshow("mask", mask)

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening device camera")
    exit(-1)

top_left_corner, bottom_right_corner = [], []
def drawCallback(image):
    def drawRectangle(action, x, y, flags, *userdata):
        # Referencing global variables 
        global top_left_corner, bottom_right_corner
        # Mark the top left corner, when left mouse button is pressed
        if action == cv2.EVENT_LBUTTONDOWN:
            top_left_corner = [(x,y)]
        # When left mouse button is released, mark bottom right corner
        elif action == cv2.EVENT_LBUTTONUP:
            bottom_right_corner = [(x,y)]
            # Draw the rectangle
            cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0,255,0),2,8)
            cv2.imshow("camera",image)

    return drawRectangle

#  cv2.namedWindow('camera')
#  cv2.setMouseCallback('camera', drawRectangle)

while(True):
    ret,frame=cap.read()

    blue, green, red = cv2.split(frame)
    #  empty = np.zeros_like(blue)

    #  cv2.imshow("blue2", cv2.merge((blue, empty, empty)))
    #  cv2.imshow("green", cv2.merge((empty, green, empty)))
    #  cv2.imshow("red", cv2.merge((empty, empty, red)))

    frame[0:img_height, 0:img_width] &= mask
    frame[0:img_height, 0:img_width] |= img&(~mask)

    cv2.setMouseCallback('camera', drawCallback(frame))
    cv2.imshow("camera", frame)

    _, bintres = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("threshold", bintres)

    #  cv2.imshow("rgb", cv2.merge((red, green, blue)))
    #  cv2.imshow("rbg", cv2.merge((red, blue, green)))
    #  cv2.imshow("bgr", cv2.merge((blue, green, red)))
    #  cv2.imshow("brg", cv2.merge((blue, red, green)))
    #  cv2.imshow("gbr", cv2.merge((green, blue, red)))
    #  cv2.imshow("grb", cv2.merge((green, red, blue)))
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
