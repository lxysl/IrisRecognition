import numpy as np
import cv2


def innerCircle(img):
    """
    内圆检测
    :param img: cv2.imread() numpy.ndarrdy
    :return: 瞳孔霍夫圆参数 numpy.ndarray [x, y, r]
    """

    img = cv2.medianBlur(img, 11)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # img = cv2.bitwise_not(img)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 5,
                               param1=110, param2=20, minRadius=20, maxRadius=130)
    circles = np.int16(np.around(circles))
    circles[0, :, 2] += 3

    return circles[0][0]
