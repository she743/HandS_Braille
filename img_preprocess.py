import cv2
import numpy as np

src = cv2.imread('./example_image_flash/KakaoTalk_Photo_2024-01-31-23-34-54 002.jpeg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

img_hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
img_hlsgray = cv2.cvtColor(img_hls, cv2.COLOR_BGR2GRAY)

img_median = cv2.medianBlur(img_hlsgray, 15)
# cv2.imshow('first_med', img_median)

img_bilateral = cv2.bilateralFilter(img_median, 9, 75, 75)
cv2.imshow('bilateral', img_bilateral)

img_gaussian1 = cv2.GaussianBlur(img_bilateral, (15, 15), 0)
cv2.imshow('gaussian1', img_gaussian1)

img_adaptive = cv2.adaptiveThreshold(img_gaussian1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 27, 0.3)
cv2.imshow('adpthreshold', img_adaptive)

img_median2 = cv2.medianBlur(img_adaptive, 15)
cv2.imshow('second_median', img_median2)

img_bilateral2 = cv2.bilateralFilter(img_median2, 35, 125, 125)
cv2.imshow('second_bilateral', img_bilateral2)

img_gaussian2 = cv2.GaussianBlur(img_bilateral2, (9, 9), 2)
cv2.imshow('gaussian2', img_gaussian2)


circles = cv2.HoughCircles(img_gaussian2, cv2.HOUGH_GRADIENT, 1, 30, param1=250, param2=11, minRadius=0, maxRadius=40)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(src,(int(i[0]),int(i[1])), 18, (0,0,255), 5)

cv2.imshow('circles', src)

cv2.waitKey() #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()