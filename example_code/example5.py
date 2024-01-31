import cv2
import argparse
import numpy as np

img= cv2.imread('KakaoTalk_Photo_2024-01-31-15-26-36 005.jpeg', cv2.IMREAD_COLOR)

img2 = img.copy()

# 그레이스케일과 바이너리 스케일 변환
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
# ret, th = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)

img_grayscale_gaussian1 = cv2.GaussianBlur(imgray, (3, 3), 0)
# img_grayscale_gaussian2 = cv2.GaussianBlur(img_grayscale, (1, 1), 0)
img_grayscale = cv2.adaptiveThreshold(img_grayscale_gaussian1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 13, 0)

# 컨투어 찾기 ---①
contours, hierachy = cv2.findContours(img_grayscale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = contours[0]
# 전체 둘레의 0.05로 오차 범위 지정 ---②
epsilon = 0.05 * cv2.arcLength(contour, True)
# 근사 컨투어 계산 ---③
approx = cv2.approxPolyDP(contour, epsilon, True)

# 각각 컨투어 선 그리기 ---④
cv2.drawContours(img, [contour], -1, (0,255,0), 3)
cv2.drawContours(img2, [approx], -1, (0,255,0), 3)

# 결과 출력
cv2.imshow('contour', img)
cv2.imshow('approx', img2)

cv2.waitKey(0) #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()