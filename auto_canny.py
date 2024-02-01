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

src = cv2.imread('./example_image_flash/KakaoTalk_Photo_2024-01-31-23-34-34.jpeg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

img_hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
img_hlsgray = cv2.cvtColor(img_hls, cv2.COLOR_BGR2GRAY)

edge = auto_canny(img_hlsgray)
cv2.imshow('auto_canny', edge)

cv2.waitKey() #아무키나 누르면 지나감 안에 값이 1이면 그냥 지나가지만 키를 눌렀을때 반응함
cv2.destroyAllWindows()