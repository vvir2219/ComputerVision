__author__ = 'dadi'
import numpy as np
import cv2
import sys
import time
import platform
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

while(True):
    ret,frame=cap.read()
    frame[0:img_height, 0:img_width] &= mask
    frame[0:img_height, 0:img_width] |= img&(~mask)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
