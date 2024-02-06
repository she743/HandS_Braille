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

src = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img2/test_cap_img15.jpg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

x, y, width, height = 85, 143, 458, 140
cropped_gray_image = src_gray[y:y+height, x:x+width]
cropped_image = src[y:y+height, x:x+width]

# Convert to HSV color space
# hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
# h, s, v = cv2.split(hsv_image)

# # Apply histogram equalization to the value channel
# equalized_v = cv2.equalizeHist(v)
# equalized_hsv_image = cv2.merge([h, s, equalized_v])

background = cv2.medianBlur(cropped_gray_image, 21)
cv2.imshow('background', background)

# Convert back to BGR color space
# equalized_image = cv2.cvtColor(equalized_hsv_image, cv2.COLOR_HSV2BGR)
# equalized_gray = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2GRAY)

foreground = cv2.absdiff(cropped_gray_image, background)
cv2.imshow('foreground', foreground)

img_crop_bilateral = cv2.bilateralFilter(foreground, 3, 15, 15)
img_gaussian = cv2.GaussianBlur(img_crop_bilateral, (3, 3), 0)

_, img_binary = cv2.threshold(img_gaussian, 0, 255, cv2.THRESH_OTSU)
cv2.imshow('binary', img_binary)
img_median_binary = cv2.medianBlur(img_binary, 5)
cv2.imshow('med_binary', img_median_binary)

img_adapt_thresh = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0.1)
cv2.imshow('binary_adapt', img_adapt_thresh)
img_median_adapt= cv2.medianBlur(img_adapt_thresh, 5)
cv2.imshow('med_adapt', img_median_adapt)

window = np.uint8([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]])
morph2 = cv2.morphologyEx(img_median_binary, cv2.MORPH_DILATE, window, iterations=1)
cv2.imshow('morph', morph2)

edge = auto_canny(morph2)
cv2.imshow('auto_canny', edge)

circles = cv2.HoughCircles(morph2, cv2.HOUGH_GRADIENT, 1, 12, param1=250, param2=10, minRadius=0, maxRadius=15)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(cropped_image,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

cv2.imshow('circle', cropped_image)

cv2.waitKey()
cv2.destroyAllWindows()