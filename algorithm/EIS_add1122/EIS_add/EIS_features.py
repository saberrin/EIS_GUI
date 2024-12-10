import numpy as np


def main(freq, realdata, imagdata, R0,SOC):
    gradient_imag = np.gradient(-imagdata, axis=0)
    Rct_num = np.zeros((1, 2))
    freq_num = np.zeros((1, 2))
    Rct_num[0, 1] = len(imagdata) - 1
    Rct_feature_data = np.zeros((1, 10))
    for num in range(len(imagdata) - 1):
        # 若系数为0 则认定20Hz及1Hz为标准位置
        if np.abs(freq[num + 1, 0] - 20) < np.abs(freq[int(freq_num[0, 0]), 0] - 20):
            freq_num[0, 0] = num + 1
        if np.abs(freq[num + 1, 0] - 1) < np.abs(freq[int(freq_num[0, 1]), 0] - 1):
            freq_num[0, 1] = num + 1

        if 0.1 <= freq[num, 0] <= 1000:
            # 斜率由正到负
            if gradient_imag[num, 0] >= 0 >= gradient_imag[num + 1, 0]:
                Rct_num[0, 0] = num
            elif gradient_imag[num, 0] <= 0 <= gradient_imag[num + 1, 0]:
                Rct_num[0, 1] = num

    if Rct_num[0, 0] == 0:
        Rct_num[0, 0] = freq_num[0, 0]
    if Rct_num[0, 1] == 0:
        Rct_num[0, 1] = freq_num[0, 1]

    Rct_feature_data[0, 0] = R0
    Rct_feature_data[0, 1] = Rct_num[0, 0]
    Rct_feature_data[0, 2] = freq[int(Rct_num[0, 0]), 0]
    Rct_feature_data[0, 3] = realdata[int(Rct_num[0, 0]), 0]
    Rct_feature_data[0, 4] = imagdata[int(Rct_num[0, 0]), 0]
    Rct_feature_data[0, 5] = Rct_num[0, 1]
    Rct_feature_data[0, 6] = freq[int(Rct_num[0, 1]), 0]
    Rct_feature_data[0, 7] = realdata[int(Rct_num[0, 1]), 0]
    Rct_feature_data[0, 8] = imagdata[int(Rct_num[0, 1]), 0]
    Rct_feature_data[0, 9] = SOC
    # 保存数据至文件
    path = './para_need/EIS_features_all.txt'
    with open(path, mode='a') as f:
        np.savetxt(f, Rct_feature_data, fmt='%.15f', delimiter=' ')
        f.close()
    return Rct_feature_data
