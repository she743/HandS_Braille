import cv2
import numpy as np
import sys

src = cv2.imread('/home/rasp/Desktop/HandS_Braille/captured_img/test_cap_img0.jpg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

if src is None:
    print('Image load failed!')
    sys.exit()

img_hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
img_hlsgray = cv2.cvtColor(img_hls, cv2.COLOR_BGR2GRAY)

# cv2.imshow('hlsgray', img_hlsgray)

img_grayscale_gaussian1 = cv2.GaussianBlur(img_hlsgray, (3, 3), 0)
# img_grayscale_gaussian2 = cv2.GaussianBlur(img_grayscale, (1, 1), 0)
img_grayscale = cv2.adaptiveThreshold(img_grayscale_gaussian1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 37, 0)

kernel = np.array([[1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]])*(1/3)

image_blur = cv2.filter2D(img_grayscale, -1, kernel)
# cv2.imshow('sharp', image_blur)

img_median = cv2.medianBlur(image_blur, 5)

# src 영상에 지역 이진화 수행
dst1 = np.zeros(img_median.shape, np.uint8)

bw = img_median.shape[1] // 4
bh = img_median.shape[0] // 4

for y in range(4):
    for x in range(4):
        src_ = img_median[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
        dst_ = dst1[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
        cv2.threshold(src_, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU, dst_)


# 영상 안에 있는 흰색 덩어리를 정수 형태로 리턴
cnt1, _ = cv2.connectedComponents(dst1)
print('cnt1:', cnt1)

# 모폴로지 열기
dst2 = cv2.morphologyEx(dst1, cv2.MORPH_OPEN, None)

# 영상 안에 있는 흰색 덩어리를 정수 형태로 리턴
cnt2, _ = cv2.connectedComponents(dst2)
print('cnt2:', cnt2)

# cimg = cv2.cvtColor(img_median, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img_median, cv2.HOUGH_GRADIENT, 1, 30, param1=250, param2=11, minRadius=5, maxRadius=12)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(img_median,(int(i[0]),int(i[1])), 18, (0,255,255), 5)

# cv2.imshow('dst1', dst1)
# cv2.imshow('dst2', dst2)

# cv2.imshow('gaussiangray', img_grayscale_gaussian1)
# cv2.imshow('adaptivegray2', img_grayscale)
cv2.imshow('median', img_median)

cv2.waitKey() #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()