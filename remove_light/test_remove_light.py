import numpy as np
import cv2
img1 = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img2/test_cap_img10.jpg')
img2 = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img2/test_cap_img10.jpg')

gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
bg = cv2.medianBlur(gray, 101)  # Compute the background (use a large filter radius for excluding the dots)
fg = cv2.absdiff(gray, bg)  # Compute absolute difference 
_, thresh = cv2.threshold(fg, 0, 255, cv2.THRESH_OTSU)  # Apply binary threshold (THRESH_OTSU applies automatic threshold level)
edges = cv2.Canny(gray, threshold1=50, threshold2=100)  # Apply Canny edge detection.
thresh = cv2.bitwise_or(thresh, edges)  # Merge edges with thresh
# _, _, boxes, _ = cv2.connectedComponentsWithStats(thresh)
# boxes = boxes[1:]
# filtered_boxes = []
# for x, y, w, h, pixels in boxes:
#     #if pixels < 1000 and h < 35 and w < 35 and h > 14 and w > 14 and x > 15 and y > 15 and pixels > 100:
#     if pixels < 1000 and x > 15 and y > 15 and pixels > 200:
#         filtered_boxes.append((x, y, w, h))
# for x, y, w, h in filtered_boxes:
#     W = int(w)/2
#     H = int(h)/2
#     cv2.circle(img1, (x+int(W), y+int(H)), 2, (0, 255, 0), 1) 

circles1 = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 15, param1=20, param2=11, minRadius=2, maxRadius=22)
circles2 = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 15, param1=20, param2=11, minRadius=2, maxRadius=22)

circles1 = np.uint16(np.around(circles1))
circles2 = np.uint16(np.around(circles2))

for i in circles1[0,:]:
    cv2.circle(img1,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

for i in circles1[0,:]:
    cv2.circle(img2,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

cv2.imshow('circle1', img1)
cv2.imshow('circle2', img2)

# Show images for testing
cv2.imshow('bg', bg)
cv2.imshow('fg', fg)
cv2.imshow('gray', gray)
cv2.imshow('edges', edges)
cv2.imshow('thresh', thresh)

cv2.waitKey()
cv2.destroyAllWindows()