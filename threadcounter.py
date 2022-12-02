## tkinter GUI
## layout:
## Choose file
## Choose algorithm
## Choose parameters
## Compute -> returns 2 lists, images & values

import cv2 as cv

from tkinter import *
from tkinter import ttk, filedialog, messagebox

from PIL import ImageTk, Image

import os

## Any function that returns an image and a text can be passed to compute function
## so we can customize which algorithm, from the GUI. image return value should
## contain preprocessed image.
##
## This is a dummy function. replace its usages by actual algorithms.
def dummyAlgorithm(image: cv.Mat):
    return image, str(image.size)


## Convert OpenCV image into something displayable by tkinter
def getTkImage(image: cv.Mat):
    global imgtk
    b, g, r = cv.split(image)
    rgb = cv.merge((r, g, b))
    im = Image.fromarray(rgb, "RGB")
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk


def main():
    root = Tk()
    frame = ttk.Frame(root, padding=40)
    frame.grid()
    path = None
    chooseFileButton = None
    filePathLabel = None
    unselectButton = None
    imageDisplay = None
    resultDisplay = None

    def unselect():
        nonlocal chooseFileButton, path, filePathLabel, unselectButton
        path = None
        chooseFileButton = Button(
            frame, text="Please choose an image file", command=chooseFile
        )
        chooseFileButton.grid(row=0, column=0)
        for widget in [filePathLabel, unselectButton, imageDisplay, resultDisplay]:
            if widget:
                widget.grid_remove()

    def chooseFile():
        nonlocal chooseFileButton, path, filePathLabel, unselectButton, imageDisplay
        path = filedialog.askopenfilename()
        if not path:
            messagebox.showwarning(title="Error", message="Please select a file!")
            path = None
            return
        chooseFileButton.grid_remove()
        filePathLabel = ttk.Label(frame, text=path)
        filePathLabel.grid(row=0, column=0)
        unselectButton = ttk.Button(frame, text="Unselect", command=unselect)
        unselectButton.grid(row=0, column=1)

    def compute(algorithm: str):
        nonlocal imageDisplay, resultDisplay
        fn: function[tuple[cv.Mat, str], [cv.Mat]] = {
            "canny": dummyAlgorithm,
            "iterative": dummyAlgorithm,
        }[algorithm]
        ## TODO: If path is not set, show error
        if path is None:
            messagebox.showwarning(title="Error", message="Please select a file!")
            return
        for widget in [imageDisplay, resultDisplay]:
            if widget:
                widget.grid_remove()
        preprocessedImage, textResult = fn(cv.imread(path))
        imageDisplay = ttk.Label(frame, image=getTkImage(preprocessedImage), width=100)
        imageDisplay.grid(row=5, column=0)
        resultDisplay = ttk.Label(frame, text=textResult)
        resultDisplay.grid(row=6, column=0)

    unselect()

    radioVar = StringVar(frame, "canny")
    ttk.Radiobutton(
        frame, text="Canny edge detector", variable=radioVar, value="canny"
    ).grid(row=1, column=0)
    ttk.Radiobutton(
        frame, text="Iterative counting", variable=radioVar, value="iterative"
    ).grid(row=2, column=0)

    ttk.Button(
        frame, text="Compute", command=lambda: compute(algorithm=radioVar.get())
    ).grid(row=3, column=0)

    ttk.Separator().grid(row=4, column=0)

    root.mainloop()


if __name__ == "__main__":
    main()
