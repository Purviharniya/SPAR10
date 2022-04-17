import os
import cv2
import math
import easyocr
import numpy as np
import pandas as pd
from scipy import ndimage
from tqdm import tqdm

# searches for images in a folder and returns a list containing path of the image
def load_images_from_folder(folder):
    images = []
    for file_name in os.listdir(folder):
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.JPG') \
                or file_name.endswith('.JPEG') or file_name.endswith('.png') or file_name.endswith('.PNG'):
            img = os.path.join(folder, file_name)
            if img is not None:
                images.append(img)
    return images


# takes a list of images, returns a list containing images that are rotated with a specific angle if found or else do not rotate it
def rotated_images(list_of_images):
    rotated_images = []
    for img in tqdm(list_of_images):
        img = cv2.imread(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_gaussian = cv2.GaussianBlur(img_gray, (3, 3), 0)
        img_edges = cv2.Canny(gray_gaussian, 50, 150)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

        # if no angle found return the original image
        if lines is None:
            median_angle = 0.0
        else:
            angles = []
            for [[x1, y1, x2, y2]] in lines:
                # convert radian into degrees
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                angles.append(angle)
                median_angle = np.median(angles)

        if median_angle == -90.0:
            img_rotated = img
        else:
            img_rotated = ndimage.rotate(img, median_angle)

        rotated_images.append(img_rotated)
    return rotated_images

def extract_text_from_id_using_easyOcr(list_rotated_images):
    for img_rotated in tqdm(list_rotated_images):

        text_from_id = []
        image = img_rotated.copy()

        classNames = ['invoiceNumber', 'invoiceDate', 'totalAmount']
        CONFIDENCE_THRESHOLD = 0.2
        NMS_THRESHOLD = 0.4

        configPath = 'extractor/yolov3_testing.cfg'
        weightsPath = 'extractor/yolov3_training_4000.weights'

        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

        reader= easyocr.Reader(['en'])
        classes, scores, boxes = model.detect(img_rotated, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

        list_label = ['invoiceNumber', 'invoiceDate', 'totalAmount']
        for (box, classid) in zip(boxes, classes):
            if classNames[classid] in list_label:
                x, y, l, b = box
                cropped = image[y:b + y, x:x + l]
                cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                text = reader.readtext(cropped)
                inside_list = []
                for i in range(0, len(text)):
                    inside_list.append(text[i][1])
                    if text[i][2] == 0.0:
                        continue
                text_from_id.append(inside_list)
        data = dict(zip(list_label, text_from_id))
    return data

def text_extractor():
    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.4

    classNames = ['invoiceNumber', 'invoiceDate', 'totalAmount']

    configPath = 'extractor/yolov3_testing.cfg'
    weightsPath = 'extractor/yolov3_training_4000.weights'

    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

    reader= easyocr.Reader(['en'])

    folder_path = "static/uploads/text_extraction"
    path_of_images = load_images_from_folder(folder_path)

    new_images = rotated_images(path_of_images)
    data = extract_text_from_id_using_easyOcr(new_images)

    return data
