import os
import cv2
import pywt
import numpy as np

from util.innerCircle import innerCircle
from util.outerCircle import outerCircle
from util.normalize import normalize
from util.config import feature_dataset_path as fdp
from util.config import dataset_path as dp

height = 40
width = 512


def generateFeatureDataset(feature_dataset_path=fdp, dataset_path=dp, mode='swt'):
    """
    生成特征数据库，目录格式与数据集目录相对应
    :param feature_dataset_path: 特征目录
    :param dataset_path: 数据集目录 './dataset/name/L/1.jpeg'
    :param mode: 特征提取模式
    """
    i = 0
    for path, dir_list, file_list in os.walk(dataset_path):
        save_dir = feature_dataset_path + path[len(dataset_path):]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for file_name in file_list:
            img_path = os.path.join(path, file_name)
            save_path = feature_dataset_path + img_path[len(dataset_path):-len(file_name.split('.')[-1])] + 'bmp'
            feature = getFeatureMap(cv2.imread(img_path, 0), mode)
            cv2.imwrite(save_path, feature)
            i += 1


def getFeatureMap(img, mode='swt'):
    # 提取每张照片的特征
    inner = innerCircle(img)
    outer = outerCircle(img, inner)
    polar_array, polar_noise = normalize(img, outer[0], outer[1], outer[2], inner[0], inner[1], inner[2], height, width)
    if mode == 'swt':
        feature = swtFeatureMap(polar_array, wavelet='db3', level=7)  # 静态小波变换
    else:
        feature = mallatFeatureMap(polar_array, wavelet='db3', level=7)  # mallat小波变换
    return feature


def swtFeatureMap(normalized_img, wavelet='db3', level=7):
    # 提取规范化后（矩形区域）的图片特征
    swt_list = np.zeros((normalized_img.shape[0], level + 1, normalized_img.shape[1]), dtype=np.uint8)  # (40, 8, 512)
    for index, value in enumerate(normalized_img):
        # cA7, cD7, cD6, cD5, cD4, cD3, cD2, cD1
        swt_coeffs = pywt.swt(data=value, wavelet=wavelet, level=level, trim_approx=True)
        for coeff in swt_coeffs:
            coeff[coeff > 0] = 1
            coeff[coeff < 0] = 0
        swt_list[index] = np.array(swt_coeffs)
    swt_list = swt_list.swapaxes(0, 1)  # (8, 40, 512)
    feature = swt_list.reshape((-1, 512))  # (320, 512)
    # feature = swt_list[1:5].reshape((-1, 512))
    return feature


def mallatFeatureMap(normalized_img, wavelet='db3', level=7):
    """效果不好弃用"""
    coeff_list = np.zeros((normalized_img.shape[0], level + 1, normalized_img.shape[1]))
    for index, value in enumerate(normalized_img):
        # cA7, cD7, cD6, cD5, cD4, cD3, cD2, cD1
        coeffs = pywt.wavedec(data=value, wavelet=wavelet, level=level)
        for i, coeff in enumerate(coeffs):
            coeffs[i] = np.pad(np.array(coeff), (0, normalized_img.shape[1] - len(coeff)), 'constant')  # 末尾补零至等长
        coeff_list[index] = np.array(coeffs)
    feature = coeff_list[4:5].reshape((-1, 512))
    return feature
