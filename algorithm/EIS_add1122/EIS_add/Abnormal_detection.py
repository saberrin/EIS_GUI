import numpy as np
import os


def main():
    # 打开文件
    features_path = './para_need/EIS_features_all.txt'  # 文件路径
    features = np.loadtxt(features_path).reshape(-1, 10)
    # 析锂检测
    if len(features[:-1, 0]) > 1:
        R0_history = features[:-1, 0].reshape(-1, 1)
        R0 = features[-1, 0]
        # 按照概率检测 该值为负数 则不考虑 该值大于3 需要认真考虑 该值大于6 需要极其认真的考虑 （猜的）
        R0_history_std = np.std(R0_history)
        if R0_history_std < 1.8503e-06:
            Pxili = (R0 - np.mean(R0_history)) / 1.8503e-06
        else:
            Pxili = (R0 - np.mean(R0_history)) / R0_history_std
    else:
        Pxili = 0
    # 数据返回用于绘图
    R0_SOC = np.column_stack((features[:, 0] * 1000000, features[:, -1]* 100))
    Rct1_Real_SOC = np.column_stack((features[:, 3] * 1000000, features[:, -1] * 100))
    Rct1_imag_SOC = np.column_stack((features[:, 4] * 1000000, features[:, -1] * 100))
    Rct2_Real_SOC = np.column_stack((features[:, 7] * 1000000, features[:, -1] * 100))
    Rct2_imag_SOC = np.column_stack((features[:, 8] * 1000000, features[:, -1] * 100))
    return Pxili, R0_SOC, Rct1_Real_SOC, Rct1_imag_SOC, Rct2_Real_SOC, Rct2_imag_SOC
