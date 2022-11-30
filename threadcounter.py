## tkinter GUI
## layout:
## Choose file
## Choose algorithm
## Choose parameters
## Compute -> returns 2 lists, images & values

import cv2 as cv

from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image

import os

## Convert OpenCV image into something displayable by tkinter
def getTkImage(image: cv.Mat):
    global imgtk
    b, g, r = cv.split(image)
    rgb = cv.merge((r, g, b))
    im = Image.fromarray(rgb, "RGB")
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk


def compute(algorithm):
    print(algorithm)


def main():
    root = Tk()
    frame = ttk.Frame(root, padding=40)
    frame.grid()
    path = None
    chooseFileButton = None
    filePathLabel = None
    unselectButton = None
    imageDisplay = None

    def unselect():
        nonlocal chooseFileButton, path, filePathLabel, unselectButton
        path = None
        chooseFileButton = Button(
            frame, text="Please choose an image file", command=chooseFile
        )
        chooseFileButton.grid(row=0, column=0)
        for widget in [filePathLabel, unselectButton, imageDisplay]:
            if widget:
                widget.grid_remove()

    def chooseFile():
        nonlocal chooseFileButton, path, filePathLabel, unselectButton, imageDisplay
        path = filedialog.askopenfilename()
        chooseFileButton.grid_remove()
        filePathLabel = ttk.Label(frame, text=path)
        filePathLabel.grid(row=0, column=0)
        unselectButton = ttk.Button(frame, text="Unselect", command=unselect)
        unselectButton.grid(row=0, column=1)
        tkImage = getTkImage(cv.imread(path))
        print(tkImage)
        imageDisplay = Label(
            frame, image=getTkImage(cv.imread(path)), width=200, height=100
        )
        imageDisplay.grid(row=3, column=0)

    unselect()

    radioVar = StringVar(frame, "1")
    ttk.Radiobutton(frame, text="Algorithm 1", variable=radioVar, value="1").grid(
        row=1, column=0
    )
    ttk.Radiobutton(frame, text="Algorithm 2", variable=radioVar, value="2").grid(
        row=2, column=0
    )

    ttk.Button(
        frame, text="Compute", command=lambda: compute(algorithm=radioVar.get())
    ).grid(row=4, column=0)

    root.mainloop()


if __name__ == "__main__":
    main()
