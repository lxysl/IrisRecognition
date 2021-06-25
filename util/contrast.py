import os
import cv2
import numpy as np
from util.feature import getFeatureMap
from util.config import feature_dataset_path as fdp


def contrast(test_img, mode='swt', feature_dataset_path=fdp):
    score_dict = {}
    test_img_feature = getFeatureMap(test_img, mode)

    score_per_eye = 0
    for path, dir_list, file_list in os.walk(feature_dataset_path):
        if len(file_list) != 0:
            for img_path in file_list:
                img_feature = cv2.imread(os.path.join(path, img_path), -1)
                distance = np.count_nonzero(test_img_feature != img_feature)
                score_per_eye += distance
            path_split = path.split('\\')  # windows下为'\\'，linux下为'/'
            score_dict[path_split[-2] + '-' + path_split[-1]] = score_per_eye / len(file_list)
            score_per_eye = 0

    sorted_list = sorted(score_dict.items(), key=lambda x: x[1], reverse=False)
    predict = sorted_list[0][0]
    return predict.split('-')[0], predict.split('-')[1], sorted_list  # 姓名，L/R左右眼，分数表
