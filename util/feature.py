import numpy as np
import pywt


def swtFeatureMap(normalized_img, wavelet='db3', level=7):
    swt_list = np.zeros((normalized_img.shape[0], level + 1, normalized_img.shape[1]), dtype=np.uint8)  # (40, 8, 512)
    for index, value in enumerate(normalized_img):
        # cA7, cD7, cD6, cD5, cD4, cD3, cD2, cD1
        swt_coeffs = pywt.swt(data=value, wavelet=wavelet, level=level, trim_approx=True)
        for coeff in swt_coeffs:
            coeff[coeff > 0] = 1
            coeff[coeff < 0] = 0
        swt_list[index] = np.array(swt_coeffs)
    swt_list = swt_list.swapaxes(0, 1)  # (8, 40, 512)
    feature = swt_list.reshape((-1, 512))
    # feature = swt_list[4:5].reshape((-1, 512))
    return feature


def mallatFeatureMap(normalized_img, wavelet='db3', level=7):
    coeff_list = np.zeros((normalized_img.shape[0], level + 1, normalized_img.shape[1]))
    for index, value in enumerate(normalized_img):
        # cA7, cD7, cD6, cD5, cD4, cD3, cD2, cD1
        coeffs = pywt.wavedec(data=value, wavelet=wavelet, level=level)
        for i, coeff in enumerate(coeffs):
            coeffs[i] = np.pad(np.array(coeff), (0, normalized_img.shape[1] - len(coeff)), 'constant')  # 末尾补零至等长
        coeff_list[index] = np.array(coeffs)
    feature = coeff_list[4:5].reshape((-1, 512))
    return feature
