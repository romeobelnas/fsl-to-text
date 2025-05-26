import cv2
import numpy as np
from keras.models import load_model

model = load_model('testsadasd.h5')

SPACE = 0x20
SPACE = chr(SPACE)


def preProcessing(img1):
    return img1


def predict(hsv):
    img1 = np.asarray(hsv)
    img1 = cv2.resize(img1, (64, 64))
    img1 = preProcessing(img1)
    img1 = img1.reshape(1, 64, 64, 3)

    predictions = model.predict(img1)
    prob_val = np.amax(predictions)

    classIndex = int(model.predict_classes(img1))
    return classIndex, prob_val


def letters(classIndex):
    letter_dict = {
        0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I",
        9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q",
        17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X", 24: "Y", 25: "Z"
    }

    if classIndex in letter_dict:
        return letter_dict[classIndex]
    else:
        raise ValueError("Error: No Letter")
