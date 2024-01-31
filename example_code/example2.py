import cv2
import numpy as np

# IMG = cv2.imread('KakaoTalk_Photo_2024-01-31-15-26-24 003.jpeg')
IMG = cv2.imread('KakaoTalk_Photo_2024-01-31-15-26-36 005.jpeg')
GRAY = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)

gftt = cv2.GFTTDetector_create()

keypoints = gftt.detect(GRAY, None)

img_draw = cv2.drawKeypoints(IMG, keypoints, None)

cv2.imshow('original', IMG)
cv2.imshow('GFTT', img_draw)

cv2.waitKey(0) #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()