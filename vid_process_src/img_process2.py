import cv2
import numpy as np

src = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img/test_cap_img2.jpg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

x, y, width, height = 83, 153, 472, 150

cropped_image = src_gray[y: y+height, x:x+width]
cv2.imshow('cropped', cropped_image)

equalized = cv2.equalizeHist(cropped_image)
cv2.imshow('equalize', equalized)

# kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

# sharpened_img = cv2.filter2D(equalized, -1, kernel)
# cv2.imshow('sharp', sharpened_img)

img_median = cv2.medianBlur(equalized, 5)
cv2.imshow('first_med', img_median)

img_bilateral = cv2.bilateralFilter(img_median, 9, 15, 15)
cv2.imshow('bilateral', img_bilateral)

img_gaussian1 = cv2.GaussianBlur(img_bilateral, (5, 5), 1)
cv2.imshow('gaussian1', img_gaussian1)

img_src_adapt = cv2.adaptiveThreshold(img_gaussian1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0.1)
cv2.imshow('binary_adapt', img_src_adapt)

img_median2 = cv2.medianBlur(img_src_adapt, 5)
cv2.imshow('second_median', img_median2)

circles = cv2.HoughCircles(img_median2, cv2.HOUGH_GRADIENT, 1, 17, param1=250, param2=10, minRadius=5, maxRadius=60)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(cropped_image, (int(i[0]),int(i[1])), 2, (0,0,255), 5)

cv2.circle(src, (83, 153), 2, (255,0,255), 5)
cv2.circle(src, (555, 303), 2, (255,0,255), 5)

cv2.imshow('circles', cropped_image)

cv2.waitKey()
cv2.destroyAllWindows()