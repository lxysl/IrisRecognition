import numpy as np
import cv2
from skimage.transform import hough_circle, hough_circle_peaks


def outerCircle(img, inner):
    clip_img = img[(inner[1] - inner[2]): (inner[1] + inner[2]), :]
    clip_img = cv2.medianBlur(clip_img, 11)
    # img = cv2.medianBlur(img, 11)
    # img = cv2.medianBlur(img, 11)
    eye_edges = cv2.Canny(clip_img, threshold1=15, threshold2=30, L2gradient=True)
    circles = cv2.HoughCircles(eye_edges, cv2.HOUGH_GRADIENT, 2, 5,
                               param1=30, param2=20, minRadius=int(inner[2] * 1.8), maxRadius=int(inner[2] * 2.5))
    circles = np.uint16(np.around(circles))
    circles[0, :, 1] += inner[1] - inner[2]

    distance = np.zeros(len(circles[0]))
    for index, value in enumerate(circles[0, :]):
        distance[index] = np.linalg.norm(np.array((inner[0], inner[1])) - np.array((value[0], value[1])))
    best_fit = circles[0][np.argmin(distance)]
    return best_fit
