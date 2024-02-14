import numpy as np
from collections import Counter
import cv2
import math

def img_preprocess(src_path):
    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
    if src is None:
        raise ValueError("Failed to load image from {}".format(src_path))
    
    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    x, y, width, height = 120, 160, 460, 120
    cropped_gray_image = src_gray[y:y+height, x:x+width]
    cropped_image = src[y:y+height, x:x+width]

    background = cv2.medianBlur(cropped_gray_image, 27)
    foreground = cv2.absdiff(cropped_gray_image, background)

    img_crop_bilateral = cv2.bilateralFilter(foreground, 3, 15, 15)
    img_gaussian = cv2.GaussianBlur(img_crop_bilateral, (3, 3), 0)

    _, img_binary = cv2.threshold(img_gaussian, 0, 255, cv2.THRESH_OTSU)
    
    window = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    morph2 = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, window, iterations=1)
    cv2.imshow('morph', morph2)
    
    med_morph = cv2.medianBlur(morph2, 3)
    cv2.imshow('med_morph', med_morph)
    # circles = cv2.HoughCircles(morph2, cv2.HOUGH_GRADIENT, 1, 12, param1=250, param2=10, minRadius=0, maxRadius=15)

    # circles = np.uint16(np.around(circles))

    # for i in circles[0,:]:
    #     cv2.circle(cropped_image,(int(i[0]),int(i[1])), int(i[2])+1, (0,255,255), 1)

    # cv2.imshow('circle', cropped_image)

    return cropped_image, med_morph

def get_diameter(ctrs):
    if not ctrs:
        raise ValueError("No contours found.")
    
    boundingBoxes = [list(cv2.boundingRect(c)) for c in ctrs]
    c = Counter([i[2] for i in boundingBoxes])
    mode = c.most_common(1)[0][0]

    if mode == 1:
        diam = c.most_common(2)[1][0] if len(c) > 1 else 1
    else:
        diam = mode
    return diam

# def get_circles(ctrs, diam):
#     questionCtrs = []
#     for c in ctrs:
#         (x, y, w, h) = cv2.boundingRect(c)
#         aspect_ratio = w / float(h)
#         if diam * 0.8 <= w <= diam * 1.2 and 0.8 <= aspect_ratio <= 1.2:
#             questionCtrs.append(c)
#     return questionCtrs

def get_circles(src, processed): 
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(processed, cv2.HOUGH_GRADIENT, 1, 11, param1=250, param2=8, minRadius=0, maxRadius=(diameter+2))

    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # Draw the circles
        for i in circles[0, :]:
            # Draw the outer circle
            # cv2.circle(src, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(src, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow('circles', src)
    return src



def calculate_slope_angle(x1, y1, x2, y2):
    # 두 점 사이의 가로, 세로 거리 계산
    dx = x2 - x1
    dy = y2 - y1
    
    # 기울기 각도 계산 (라디안)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

def get_spacing(boundingBoxes):
    spacingX = sorted(set([b[0] for b in boundingBoxes]))
    spacingY = sorted(set([b[1] for b in boundingBoxes]))
    return spacingX, spacingY

def draw_lines(src, boundingBoxes):
    for box in boundingBoxes:
        x, y, w, h = box
        cv2.rectangle(src, (x, y), (x + diameter, y + diameter), (0, 255, 0), 1)
    for x in spacingX:
        cv2.line(src, (x, min(spacingY)), (x, src.shape[1]), (0, 0, 255), 1)
    return src

# Main code
try:
    src, processed = img_preprocess('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img3/test_cap_img19.jpg')
    # Get the height and width of the image
    height, width = src.shape[:2]
    
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    diameter = get_diameter(contours)
    print(diameter)
    # braille = get_circles(contours, diameter)
    hough = get_circles(src, processed)

    # boundingBoxes = [list(cv2.boundingRect(c)) for c in braille]
    # spacingX, spacingY = get_spacing(boundingBoxes)
    # print(min(spacingX), max(spacingY), max(spacingX), (max(spacingY)+diameter))
    # angle = calculate_slope_angle(min(spacingX), max(spacingY), max(spacingX), (max(spacingY)+diameter))
    # print(angle)

    # Calculate the rotation matrix
    # rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    # print(rotation_matrix)

    # # Perform the rotation using warpAffine
    # rotated_image = cv2.warpAffine(src, rotation_matrix, (width, height))

    # result_image = draw_lines(src, boundingBoxes)

    # cv2.imshow('Rotated Image', rotated_image)
    # cv2.imshow('Result Image', result_image)

    cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    cv2.destroyAllWindows()

except Exception as e:
    print("An error occurred:", e)

cv2.waitKey(0)
cv2.destroyAllWindows()