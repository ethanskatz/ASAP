import tkinter as tk

import cv2
from PIL import Image, ImageTk

cap = cv2.VideoCapture(0)

root = tk.Tk()
label = tk.Label(root)
label.pack()


def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    root.after(15, update_frame)  # ~60 fps max


def on_close():
    cap.release()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
update_frame()
root.mainloop()
