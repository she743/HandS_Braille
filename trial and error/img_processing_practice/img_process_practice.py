import cv2
import numpy as np

# Read the image
image = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img/test_cap_img2.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('original_img', image)

# Apply threshold to convert the image to binary
_, binary_image = cv2.threshold(image, 92, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('img', binary_image)

window = np.uint8([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]])
morph2 = cv2.morphologyEx(binary_image, cv2.MORPH_DILATE, window, iterations=2)
cv2.imshow('morph2', morph2)

binary_med = cv2.medianBlur(binary_image, 3)
cv2.imshow('medimg', binary_med)

# Apply morphological operations to remove small black dots
kernel = np.zeros((5, 5), np.uint8)
opening = cv2.morphologyEx(binary_med, cv2.MORPH_OPEN, kernel, iterations=2)
cv2.imshow('morph', opening)


# Find contours in the processed image
contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Set a threshold area
#  to filter out small contours (you can adjust this threshold)
min_contour_area = 100

# Iterate through the contours and draw only the ones above the threshold
filtered_image = np.zeros_like(image)
for contour in contours:
    if cv2.contourArea(contour) > min_contour_area:
        cv2.drawContours(filtered_image, [contour], 0, 255, -1)

# Display the original and processed images
cv2.imshow('Original Image', image)
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()