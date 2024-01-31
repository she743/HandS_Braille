# import cv2
# import numpy as np

# img = cv2.imread('KakaoTalk_Photo_2024-01-31-15-26-36 005.jpeg', cv2.IMREAD_GRAYSCALE)
# img = cv2.medianBlur(img, 5)
# cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,param1=50,param2=25,minRadius=0, maxRadius=0)

# circles = np.uint16(np.around(circles))

# for i in circles[0,:]:
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

# cv2.imshow('img', cimg)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2

src = cv2.imread('KakaoTalk_Photo_2024-01-31-15-26-36 005.jpeg')
dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

img_grayscale_gaussian1 = cv2.GaussianBlur(gray, (3, 3), 0)
# img_grayscale_gaussian2 = cv2.GaussianBlur(img_grayscale, (1, 1), 0)
img_grayscale = cv2.adaptiveThreshold(img_grayscale_gaussian1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 79, 0)

img_grayscale = cv2.bilateralFilter(img_grayscale, -1, 10, 5)
# _, img_grayscale = cv2.threshold(img_grayscale, 0, 255, cv2.THRESH_OTSU)

circles = cv2.HoughCircles(img_grayscale, cv2.HOUGH_GRADIENT, 1, 10, param1 = 60, param2 = 38, minRadius = 3, maxRadius = 50)

print(circles)

for i in circles[0]:
    cv2.circle(src, (int(i[0]), int(i[1])), int(i[2]), (0, 0, 0), 5)

cv2.imshow("original", src)


cv2.waitKey(0)
cv2.destroyAllWindows()