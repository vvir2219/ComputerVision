__author__ = 'vlad'
import numpy as np
import cv2
import sys
import time
import platform
print(cv2.__version__)
print(platform.architecture())

img = cv2.imread('./logo.png', 1)
img_height, img_width, _= img.shape

minlim, maxlim = tuple([30]*3), tuple([255]*3)
mask = cv2.inRange(img, minlim, maxlim)
mask = cv2.merge((mask, mask, mask))
mask //= 255

cv2.imshow("image",img)
#  cv2.moveWindow("image",200,200)

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening device camera")
    exit(-1)

while(True):
    ret,frame=cap.read()
    frame[0:img_height, 0:img_width] *= mask
    frame[0:img_height, 0:img_width] += img*(1-mask)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
