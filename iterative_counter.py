## Author: nitin-rajesh

import numpy as np
from cv2 import Mat
from skimage import io, exposure, data, img_as_ubyte
from skimage.color import rgb2gray
from skimage.filters import unsharp_mask, threshold_otsu, threshold_local
from skimage.transform import rescale


def boostContrast(image):

    grayscale_img = rgb2gray(image)
    grayscale_img = exposure.adjust_gamma(grayscale_img, 3)
    grayscale_img = exposure.adjust_sigmoid(grayscale_img, 1, 3)
    grayscale_img = exposure.rescale_intensity(grayscale_img)
    grayscale_img = unsharp_mask(grayscale_img, radius=5, amount=1)
    local_thresh = threshold_local(grayscale_img, 35)
    binary_local = grayscale_img > local_thresh

    return binary_local


def findFibreCount(img_arr, block_size):
    fibreCount = []
    transitionCount = 0
    currentState = 0

    for row in img_arr:
        transitionCount = 0
        counter = 0
        for col in row:
            counter = counter + 1
            if col != currentState and counter > block_size:
                counter = 0
                currentState = col
                transitionCount += 1

        fibreCount.append(transitionCount)

    transitionCount = sum(fibreCount) / len(fibreCount)

    return transitionCount


def getImageArr(filename):
    try:
        processed_image = io.imread(filename)
    except:
        return []

    return np.reshape(processed_image.flatten(), processed_image.shape)


def fabricDiagnosis(fname, block_size=1):
    full_img = boostContrast(io.imread(fname))
    block_size_arr = [i / 100 for i in range(5, 100, 10)]
    fibre_count_arr = []
    for i in block_size_arr:
        img = rescale(full_img, scale=i)
        local_thresh = threshold_local(img, 35)
        binary_local = img > local_thresh
        img_arr = np.reshape(binary_local.flatten(), binary_local.shape)
        fibre_count_arr.append(
            findFibreCount(img_arr=binary_local, block_size=block_size)
        )

    # for block_size, fibre_count in zip(block_size_arr,fibre_count_arr):
    #     print(block_size,':',fibre_count)
    return full_img, fibre_count_arr


def slopeDropPoint(arr):
    slopeArr = []
    slopeRate = []
    for i in range(0, len(arr) - 1):
        slopeArr.append(arr[i + 1] - arr[i])
    print(slopeArr)
    for i in range(0, len(slopeArr) - 1):
        slopeRate.append(abs(slopeArr[i + 1] - slopeArr[i]) / slopeArr[i])
    print(slopeRate)

    return slopeRate.index(max(slopeRate))


def fabricEstimate(arr):
    i = slopeDropPoint(arr)
    return arr[i + 1]


def iterativeCounterEstimate(path: str) -> tuple[Mat, str]:
    full_img, diag = fabricDiagnosis(path)
    return img_as_ubyte(full_img), f"Estimate: {fabricEstimate(diag)}"
