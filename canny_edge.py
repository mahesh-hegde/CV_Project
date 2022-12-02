import cv2
import numpy as np


def cannyEdgeEstimate(path: str) -> tuple[cv2.Mat, str]:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_threshold = 20
    high_threshold = 50
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of intersecting points to detect a line
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(
        edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap
    )

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    lines_count = lines.shape[0]
    inter = lines_count
    s = set()
    for i in range(len(lines)):
        # print(lines[i][0][1])
        s.add(lines[i][0][1] // 20)
    x = len(s)
    y = inter // x
    return lines_edges, f"Horizontal lines: {x}, Vertical lines: {y}"
