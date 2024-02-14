import numpy as np
from collections import Counter
import cv2

def img_preprocess(src_path):
    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
    if src is None:
        raise ValueError("Failed to load image from {}".format(src_path))
    
    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    x, y, width, height = 85, 143, 458, 140
    cropped_gray_image = src_gray[y:y+height, x:x+width]
    cropped_image = src[y:y+height, x:x+width]

    background = cv2.medianBlur(cropped_gray_image, 27)
    foreground = cv2.absdiff(cropped_gray_image, background)

    img_crop_bilateral = cv2.bilateralFilter(foreground, 3, 15, 15)
    img_gaussian = cv2.GaussianBlur(img_crop_bilateral, (3, 3), 0)

    _, img_binary = cv2.threshold(img_gaussian, 0, 255, cv2.THRESH_OTSU)
    
    window = np.uint8([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]])
    morph2 = cv2.morphologyEx(img_binary, cv2.MORPH_GRADIENT, window, iterations=1)
    cv2.imshow('morph', morph2)

    cv2.imshow('circle', cropped_image)

    return cropped_image, morph2

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

def get_circles(ctrs, diam):
    questionCtrs = []
    for c in ctrs:
        (x, y, w, h) = cv2.boundingRect(c)
        aspect_ratio = w / float(h)
        if diam * 0.8 <= w <= diam * 1.2 and 0.8 <= aspect_ratio <= 1.2:
            questionCtrs.append(c)
    return questionCtrs


def get_spacing(boundingBoxes):
    spacingX = sorted(set([b[0] for b in boundingBoxes]))
    spacingY = sorted(set([b[1] for b in boundingBoxes]))
    return spacingX, spacingY

def draw_lines(src, boundingBoxes):
    for box in boundingBoxes:
        x, y, w, h = box
        cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 1)
    for x in spacingX:
        cv2.line(src, (x, min(spacingY)), (x, src.shape[1]), (0, 0, 255), 1)
    return src

# Main code
try:
    src, processed = img_preprocess('/Users/tsshin/Desktop/HandS_Braille/vid_process_src/captured_img3/test_cap_img2.jpg')
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    diameter = get_diameter(contours)
    print(diameter)
    braille = get_circles(contours, diameter)
    
    boundingBoxes = [list(cv2.boundingRect(c)) for c in braille]
    spacingX, spacingY = get_spacing(boundingBoxes)
    
    result_image = draw_lines(src, boundingBoxes)

    # cv2.imshow('Rotated Image', rotated_image)
    cv2.imshow('Result', result_image)

    cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    cv2.destroyAllWindows()

except Exception as e:
    print("An error occurred:", e)