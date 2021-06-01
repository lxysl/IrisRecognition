import numpy as np
import cv2


def innerCircle(img):
    '''
    :param img: cv2.imread() numpy.ndarrdy
    :return: 瞳孔霍夫圆 numpy.ndarray [x, y, r]
    '''
    # img = cv2.GaussianBlur(img, (3, 3), 0)
    # img = cv2.Canny(img, 45, 110)

    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    img = cv2.bitwise_not(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 5,
                               param1=110, param2=20, minRadius=10, maxRadius=130)
    circles = np.uint16(np.around(circles))
    circles[0, :, 2] += 3

    # distance = np.zeros(len(circles[0]))
    # for index, value in enumerate(circles[0, :]):
    #     distance[index] = np.linalg.norm(center - np.array((value[0], value[1])))
    # return circles[0][np.argmin(distance)]
    return circles[0][0]
