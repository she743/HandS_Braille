import cv2
import numpy as np

src = cv2.imread('/home/rasp/Desktop/HandS_Braille/vid_process_src/captured_img/test_cap_img2.jpg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# print(src_gray)
x, y, width, height = 83, 153, 472, 150

cropped_image = src_gray[y: y+height, x:x+width]
cv2.imshow('cropped', cropped_image)

kernel = np.array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])

img_sharp = cv2.filter2D(cropped_image, -1, kernel)
cv2.imshow('sharp', img_sharp)

img_sharp_bilateral = cv2.bilateralFilter(img_sharp, 7, 25, 25)
cv2.imshow('sharp_bilateral', img_sharp_bilateral)

equalized = cv2.equalizeHist(img_sharp_bilateral)
cv2.imshow('equalize', equalized)

img_bilateral = cv2.bilateralFilter(equalized, 13, 15, 15)
cv2.imshow('equal_bi', img_bilateral)

img_gaussian1 = cv2.GaussianBlur(img_bilateral, (5, 5), 1)
cv2.imshow('bi_gaussian1', img_gaussian1)

img_median = cv2.medianBlur(img_gaussian1, 5)
cv2.imshow('first_med', img_median)

img_gaussian2 = cv2.GaussianBlur(img_median, (5, 5), 1)
cv2.imshow('gaussian1', img_gaussian2)

dst1 = np.zeros(img_gaussian2.shape, np.uint8)

bw = img_gaussian2.shape[1] // 4
bh = img_gaussian2.shape[0] // 4

for y in range(4):
    for x in range(4):
        src_ = img_gaussian2[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
        dst_ = dst1[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
        cv2.threshold(src_, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU, dst_)

cv2.imshow('dst1', dst1)

cnt1, _ = cv2.connectedComponents(dst1)
print('cnt1:', cnt1)

dst2 = cv2.morphologyEx(dst1, cv2.MORPH_OPEN, None)
cv2.imshow('dst2', dst2)

cnt2, _ = cv2.connectedComponents(dst2)
print('cnt2:', cnt2)

cv2.waitKey()
cv2.destroyAllWindows()