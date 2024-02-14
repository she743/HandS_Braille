import cv2
import numpy as np


def auto_canny(image, sigma=0.33):
    image = cv2.bilateralFilter(image, 9, 75, 75)
    cv2.imshow('bilateral', image)
	# compute the median of the single channel pixel intensities
    v = np.median(image)
	# apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
	# return the edged image
    return edged

src = cv2.imread('/home/rasp/Desktop/HandS_Braille/vid_process_src/captured_img3/test_cap_img2.jpg', cv2.IMREAD_COLOR)

x, y, width, height = 83, 153, 472, 150

cropped_image = src[y:y+height, x:x+width]

# Convert to HSV color space
hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
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
morph2 = cv2.morphologyEx(img_median, cv2.MORPH_CLOSE, window, iterations=1)
cv2.imshow('morph', morph2)


edge = auto_canny(img_median)
cv2.imshow('auto_canny', edge)

circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 13, param1=250, param2=11, minRadius=2, maxRadius=18)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(src,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

cv2.imshow('circle', src)

cv2.waitKey()
cv2.destroyAllWindows()