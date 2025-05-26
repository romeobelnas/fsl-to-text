import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import letter_module
from letter_module import *
import cv2
import pyttsx3
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

model = letter_module.model

window = Tk()
window.title("Filipino Sign Language to Text")
window.iconbitmap('icon_fsl.ico')

imageFrame = tk.Frame(window, width=150, height=110)
imageFrame.grid()
label = Label(window, text="Home Page", fg="#263942", font='Helvetica 20 bold')
label.grid(row=0, column=0, ipadx=22)
render = PhotoImage(file='homepagepic.jpg')
img = tk.Label(image=render)
img.grid(row=0, column=1, rowspan=4)

predicted_text = ""
word = ""
add_space = " "

# HSV Values
# H, S, V = 0, 58, 50

def close_window():
    window.destroy()


def main():
    window = tk.Toplevel()
    window.resizable(False, False)
    window.wm_title("Filipino Sign Language to Text")
    window.iconbitmap('icon_fsl.ico')

    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=5, pady=5, columnspan=5)

    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0, padx=5, pady=5, columnspan=6)
    cap = cv2.VideoCapture(0)

    # ROI
    upper_left = (350, 50)
    bottom_right = (600, 300)

    def nothing(x):
        pass

    cv2.namedWindow('Trackbars')

    # For lower_value
    cv2.createTrackbar('L - H', 'Trackbars', 101, 179, nothing)
    cv2.createTrackbar('L - S', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('L - V', 'Trackbars', 0, 255, nothing)

    # For higher_value
    cv2.createTrackbar('U - H', 'Trackbars', 179, 179, nothing)
    cv2.createTrackbar('U - S', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('U - V', 'Trackbars', 255, 255, nothing)

    def delete_text():
        global word
        predict_text_label.config(text=word)
        word = word[:-1]

    def say_text():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.say(word)
        engine.runAndWait()

    def add_text():
        global word
        predict_text_label.config(text=predicted_text)
        word += predicted_text
        predict_text_label.config(text=word)
        print(predicted_text)


    def add_space():
        global word
        global add_space
        predict_text_label.config(text=word)
        word += ' '
        print(word)


    def show_frame():
        global predicted_text
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        L_H = cv2.getTrackbarPos('L - H', 'Trackbars')
        L_S = cv2.getTrackbarPos('L - S', 'Trackbars')
        L_V = cv2.getTrackbarPos('L - V', 'Trackbars')

        U_H = cv2.getTrackbarPos('U - H', 'Trackbars')
        U_S = cv2.getTrackbarPos('U - S', 'Trackbars')
        U_V = cv2.getTrackbarPos('U - V', 'Trackbars')

        lower_value = np.array([L_H, L_S, L_V])
        upper_value = np.array([U_H, U_S, U_V])

        roi = cv2.rectangle(frame, upper_left, bottom_right, (0, 128, 0), 3)
        rect_image = hsv[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

        #remove mask

        # mask = cv2.inRange(rect_image, lower_value, upper_value)

        classIndex = predict(rect_image)[0]
        prob_val = predict(rect_image)[1]

        print(prob_val)

        predicted_text = letters(classIndex)
        font = cv2.FONT_HERSHEY_COMPLEX

        cv2.putText(frame, "Prediction: ", (50, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        if prob_val > 0.90:
            cv2.putText(frame, predicted_text, (250, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Nothing", (250, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

        cv2.imshow("Capture", rect_image)

    predict_label = tk.Label(window, text="Prediction:", width=10, height=2, bg='#C0C0C0', font='Helvetica 11 bold')
    predict_label.grid(row=1, column=0)

    predict_text_label = tk.Label(window, text=predicted_text, width=56, height=2, bg='#C0C0C0',
                                  font='Helvetica 11 bold')
    predict_text_label.grid(row=1, column=1, columnspan=3)

    label_space = Label(window, height=1)
    label_space.grid(row=2, column=0)

    button_delete = tk.Button(window, text='Delete', font='Helvetica 20 bold', command=delete_text)
    button_delete.grid(row=3, column=0, ipadx=6)

    button_add = tk.Button(window, text='Add', font='Helvetica 20 bold', command=add_text)
    button_add.grid(row=3, column=1, ipadx=25)

    button_say = tk.Button(window, text='Say', font='Helvetica 20 bold', command=say_text)
    button_say.grid(row=3, column=2, ipadx=25)

    # button_exit = tk.Button(window, text='Exit', font='Helvetica 20 bold', command=window.destroy)
    # button_exit.grid(row=3, column=3, ipadx=25)

    button_space = tk.Button(window, text='Space', font='Helvetica 20 bold', command=add_space)
    button_space.grid(row=3, column=3, ipadx=25)

    show_frame()


button_start = Button(window, text='Start', fg="#ffffff", bg="#263942", font='Helvetica 16 bold',command=main)
button_start.grid(row=1, column=0, ipady=3, ipadx=7)

space = Label(window, height=1)
space.grid(row=2, column=0)

button_space = tk.Button(window, text='Exit', font='Helvetica 16 bold', command=close_window)
button_space.grid(row=3, column=0, ipady=3, ipadx=12)

space2 = Label(window, height=1)
space2.grid(row=4, column=0)

window.mainloop()
