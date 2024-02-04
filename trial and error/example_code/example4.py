import numpy as np
import cv2

image = cv2.imread('KakaoTalk_Photo_2024-01-31-21-41-16.jpeg', cv2.IMREAD_COLOR)

img_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
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
# _, img_grayscale = cv2.threshold(img_grayscale, 0, 255, cv2.THRESH_OTSU)

img_fin = cv2.bilateralFilter(img_median, 11, 101, 39)
# _, img_grayscale = cv2.threshold(img_fin, 0, 255, cv2.THRESH_OTSU)

# cv2.imshow('gaussiangray', img_grayscale_gaussian1)
# cv2.imshow('adaptivegray2', img_grayscale)
cv2.imshow('median', img_median)
cv2.imshow('bilateral', img_fin)
# cv2.imshow('threshold', img_grayscale)



cv2.waitKey(0) #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()