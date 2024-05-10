import tkinter as tk
from tkinter import *

import PIL
import numpy as np
import win32gui
from PIL import ImageGrab

import pickle


model = pickle.load(open('./model1.h5', 'rb'))



def predict_digit(img):
    
    img = img.resize((28, 28))
    
    img = img.convert('L')
    img = np.invert(np.array(img))
    
    img = img.reshape(1,-1)
    
    res = model.predict(img)
    return res[0]


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Draw", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Recognise", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        hwnd = self.canvas.winfo_id()  
        rect = win32gui.GetWindowRect(hwnd) 
        a, b, c, d = rect
        rect = (a + 4, b + 4, c - 4, d - 4)
        im = ImageGrab.grab(rect)

        angle = 90

        im = im.rotate(angle, expand=True)

        im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)

        digit = predict_digit(im)
        self.label.configure(text=str(digit))
        # self.clear_all()

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 7
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
