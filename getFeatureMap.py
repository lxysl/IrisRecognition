import numpy as np
import cv2
from util.innerCircle import innerCircle
from util.outerCircle import outerCircle
from util.normalize import normalize
from util.feature import swtFeatureMap, mallatFeatureMap

height = 40
width = 512


def getFeatureMap(img_path, mode='swt'):
    img = cv2.imread(img_path, 0)
    inner = innerCircle(img)
    outer = outerCircle(img, inner)
    polar_array, polar_noise = normalize(img, outer[0], outer[1], outer[2], inner[0], inner[1], inner[2], height, width)
    if mode == 'swt':
        feature = swtFeatureMap(polar_array, wavelet='db3', level=7)    # 静态小波变换
    else:
        feature = mallatFeatureMap(polar_array, wavelet='db3', level=7)  # mallat小波变换
    return feature
