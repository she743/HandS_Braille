import cv2
import numpy as np

def preprocess_img(src_path):

    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
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

    return cropped_image, morph2


def find_contour_center(processed_img):

    contours, hierarchy = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centroids = []

    # Repeat for all detected contours
    for contour in contours:
        # Calculate moment of contour
        M = cv2.moments(contour)

        # Give value 1 in case denominator is zero - to avoid division by zero
        if M['m00'] == 0:
            M['m00'] += 1
            continue

        # Calculate centroids
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Add to list
        centroids.append((cx, cy))
        # print((cx,cy))

    return centroids

cv2.waitKey()
cv2.destroyAllWindows()