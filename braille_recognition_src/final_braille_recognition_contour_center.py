import cv2
import numpy as np

src = cv2.imread('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img3/test_cap_img24.jpg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

if src is None:
    raise ValueError("Failed to load image from {}".format(src))

x, y, width, height = 120, 160, 460, 90
cropped_gray_image = src_gray[y:y+height, x:x+width]
cropped_image = src[y:y+height, x:x+width]

background = cv2.medianBlur(cropped_gray_image, 27)
foreground = cv2.absdiff(cropped_gray_image, background)

img_crop_bilateral = cv2.bilateralFilter(foreground, 3, 15, 15)
img_gaussian = cv2.GaussianBlur(img_crop_bilateral, (3, 3), 0)

_, img_binary = cv2.threshold(img_gaussian, 0, 255, cv2.THRESH_OTSU)

window = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
morph2 = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, window, iterations=1)

contours, hierarchy = cv2.findContours(morph2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

centroids = []

# 모든 컨투어에 대해 반복합니다.
for contour in contours:
    # 컨투어의 모멘트를 계산합니다.
    M = cv2.moments(contour)

    # 중심값을 계산합니다.
    if M['m00'] == 0:
        M['m00'] += 1
        continue

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # 중심값을 리스트에 추가합니다.
    centroids.append((cx, cy))
    print((cx,cy))
    # 이미지에 중심을 그립니다.
    cv2.circle(cropped_image, (cx, cy), 3, (0, 255, 0), -1)
# print(centroids)

cv2.imshow('center',cropped_image)

cv2.waitKey()
cv2.destroyAllWindows()