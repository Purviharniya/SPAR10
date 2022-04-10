
import numpy as np 
import cv2
from keras.models import load_model

img_size = 224
categories={
    0: 'The uploaded image is an ADVERTISEMENT!!',
    1: 'The uploaded image is an EMAIL!!',
    2: 'The uploaded image is a FORM!!',
    3: 'The uploaded image is a LETTER!!',
    4: 'The uploaded image is a MEMO!!',
    5: 'The uploaded image is a NEWS ARTICLE!!',
    6: 'The uploaded image is a NOTE!!',
    7: 'The uploaded image is a REPORT!!',
    8: 'The uploaded image is a RESUME!!',
    9: 'The uploaded image is a SCIENTIFIC PAPER!!'
}

model = load_model("classifier/final_trained_model.h5")

def predict_category(path):
  img_data = []
  img_data.append(cv2.resize(cv2.imread(path, cv2.IMREAD_COLOR), (img_size, img_size)))
  img_test = np.array(img_data)
  predict_img = model.predict(img_test) 
  classes_img = np.argmax(predict_img,axis=1)
  return categories[classes_img[0]]