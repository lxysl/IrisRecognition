import numpy as np
import cv2


def outerCircle(img, inner):
    clip_img = img[(inner[1] - inner[2]): (inner[1] + inner[2]), :]
    clip_img = cv2.equalizeHist(clip_img)
    clip_img = cv2.GaussianBlur(clip_img, (9, 9), 0)
    clip_img = cv2.medianBlur(clip_img, 9)

    circles = cv2.HoughCircles(clip_img, cv2.HOUGH_GRADIENT, 2, 5,
                               param1=30, param2=20, minRadius=int(inner[2] * 1.4), maxRadius=int(inner[2] * 3))
    circles = np.int16(np.around(circles))
    circles[0, :, 1] += inner[1] - inner[2]

    distance = np.zeros(len(circles[0]))
    for index, value in enumerate(circles[0, :]):
        distance[index] = np.linalg.norm(np.array((inner[0], inner[1])) - np.array((value[0], value[1])))
    best_fit = circles[0][np.argmin(distance)]
    return best_fit
