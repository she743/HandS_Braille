import cv2
import numpy as np

src = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img2/test_cap_img25.jpg', cv2.IMREAD_COLOR)

x, y, width, height = 83, 153, 472, 150

cropped_image = src[y:y+height, x:x+width]

# Convert to HSV color space
hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv_image)

# Apply histogram equalization to the value channel
equalized_v = cv2.equalizeHist(v)
equalized_hsv_image = cv2.merge([h, s, equalized_v])

# Convert back to BGR color space
equalized_image = cv2.cvtColor(equalized_hsv_image, cv2.COLOR_HSV2BGR)
equalized_gray = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2GRAY)

img_crop_bilateral = cv2.bilateralFilter(equalized_gray, 3, 15, 15)
cv2.imshow('sharp_bilateral', img_crop_bilateral)

img_gaussian = cv2.GaussianBlur(img_crop_bilateral, (3, 3), 0)
cv2.imshow('gaussian1', img_gaussian)

# _, img_binary = cv2.threshold(img_gaussian, 185, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('binary', img_binary)
img_adapt_thresh = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0.1)
cv2.imshow('binary_adapt', img_adapt_thresh)

img_median = cv2.medianBlur(img_adapt_thresh, 5)
cv2.imshow('first_med', img_median)

window = np.uint8([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]])
morph2 = cv2.morphologyEx(img_median, cv2.MORPH_ERODE, window, iterations=1)
cv2.imshow('morph', morph2)

cv2.waitKey()
cv2.destroyAllWindows()