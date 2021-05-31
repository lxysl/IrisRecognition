import cv2
import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks


def IrisLocalization(eye):
    brue = cv2.bilateralFilter(eye, 9, 100, 100)
    col, row = eye.shape[:2]
    print(col, row)
    xp = brue.sum(axis=0).argmin()
    yp = brue.sum(axis=1).argmin()
    x = brue[max(0, (yp - 60)):min(yp + 60, col), max((xp - 60), 0):min(xp + 60, row)].sum(axis=0).argmin()
    y = brue[max(0, (yp - 60)):min(yp + 60, col), max((xp - 60), 0):min(xp + 60, row)].sum(axis=1).argmin()
    xp = max(xp - 60, 0) + x
    yp = max(yp - 60, 0) + y
    if xp >= 100 and yp >= 80:
        brue = cv2.GaussianBlur(eye[yp - 60:yp + 60, xp - 60:xp + 60], (5, 5), 0)
        pupil_ciricles = cv2.HoughCircles(brue, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200, param1=200
                                          , param2=12, minRadius=15, maxRadius=80)
        x, y, r = np.round(pupil_ciricles[0][0]).astype('int')
        x = xp - 60 + x
        y = yp - 60 + y
    else:
        pupil_ciricles = cv2.HoughCircles(eye, cv2.HOUGH_GRADIENT, 4, 160, minRadius=25, maxRadius=55, param2=51)
        x, y, r = np.round(pupil_ciricles[0][0]).astype('int')
    r = r + 7
    eye_copy = eye.copy()
    brue = cv2.medianBlur(eye_copy, 11)
    brue = cv2.medianBlur(brue, 11)
    brue = cv2.medianBlur(brue, 11)
    eye_edges = cv2.Canny(brue, threshold1=15, threshold2=30, L2gradient=True)
    eye_edges[x - r - 30, x + r + 30] = 0
    hough_radii = np.arange(r + 45, 150, 2)
    hough_reg = hough_circle(eye_edges, hough_radii)
    accums, xi, yi, ri = hough_circle_peaks(hough_reg, hough_radii, total_num_peaks=1)
    irirs = []
    irirs.extend(xi)
    irirs.extend(yi)
    irirs.extend(ri)
    # cv2.imshow("a",hough_res)
    # cv2.waitKey(0)
    if ((irirs[0] - x) ** 2 + (irirs[1] - y) ** 2) ** 0.5 > r * 0.3:
        irirs[0] = x
        irirs[1] = y
    return np.array(irirs), np.array([x, y, r])


if __name__ == '__main__':
    path = r''
    img = cv2.imread('./intervalDataset/002/R/S1002R04.jpg', 0)
    a1, b1 = IrisLocalization(img)
    img = cv2.circle(img, (a1[0], a1[1]), a1[2], (0, 0, 255))
    img = cv2.circle(img, (b1[0], b1[1]), b1[2], (0, 0, 255))
    cv2.imshow("a", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
