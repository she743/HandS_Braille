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

src = cv2.imread('C:/Users/tony8/HandS_Braille/vid_process_src/captured_img2/test_cap_img2.jpg', cv2.IMREAD_COLOR)
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

# for i in circles[0,:]:
#     cv2.circle(cropped_image,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

# cv2.imshow('circle', cropped_image)

# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img = morph2
ret, th = cv2.threshold(img, 127,255,cv2.THRESH_BINARY_INV)

# 컨튜어 찾기
contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contr = contours[0]

# 감싸는 사각형 표시(검정색)
x1,y1,w,h = cv2.boundingRect(contr)
cv2.rectangle(cropped_image, (x1,y1), (x1+w, y1+h), (0,0,0), 3)

# 최소한의 사각형 표시(초록색)
rect = cv2.minAreaRect(contr)
box = cv2.boxPoints(rect)   # 중심점과 각도를 4개의 꼭지점 좌표로 변환
box = np.int0(box)          # 정수로 변환
cv2.drawContours(cropped_image, [box], -1, (0,255,0), 3)

# 최소한의 원 표시(파랑색)
(x1,y1), radius = cv2.minEnclosingCircle(contr)
cv2.circle(cropped_image, (int(x1), int(y1)), int(radius), (255,0,0), 2)

# 최소한의 삼각형 표시(분홍색)
ret, tri = cv2.minEnclosingTriangle(contr)
cv2.polylines(cropped_image, [np.int32(tri)], True, (255,0,255), 2)

# 최소한의 타원 표시(노랑색)
# ellipse = cv2.fitEllipse(contr)
# cv2.ellipse(cropped_image, ellipse, (0,255,255), 3)

# 중심점 통과하는 직선 표시(빨강색)
# [vx,vy,x1,y1] = cv2.fitLine(contr, cv2.DIST_L2,0,0.01,0.01)
# cols,rows = cropped_image.shape[:2]
# cv2.line(cropped_image,(0, 0-x1*(vy/vx) + y), (cols-1, (cols-x1)*(vy/vx) + y1), (0,0,255),2)

# 결과 출력
cv2.imshow('contour', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.waitKey()
cv2.destroyAllWindows()