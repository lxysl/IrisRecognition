import cv2


def displayCircle(img, outer_x, outer_y, outer_r, inner_x, inner_y, inner_r):
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(cimg, (inner_x, inner_y), inner_r, (0, 255, 0), 1)
    cv2.circle(cimg, (outer_x, outer_y), outer_r, (0, 255, 0), 1)
    cv2.circle(cimg, (inner_x, inner_y), 2, (0, 0, 255), 3)
    cv2.circle(cimg, (outer_x, outer_y), 2, (0, 0, 255), 3)
    # cv2.imshow('detected circles', cimg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return cimg
