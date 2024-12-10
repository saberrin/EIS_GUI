import numpy as np
import Abnormal_detection
import DRT_Lasso_RL
import matplotlib.pyplot as plt
import EIS_features
import SOC_OCV_Estimation
import Temperature_Rct_Estimation_all

# 频率上限统一为100Hz
data = np.loadtxt('EIS-2.txt')
# 输入当前电池电压即可 最小为0 最大为1
OCV = 3.1
SOC = SOC_OCV_Estimation.SOC_OCV_Est(OCV)
print(SOC)

coeff = 1
lambda0 = 10 ** -6
Reg_type = "Lasso"
realpart, imagpart, freq, mu_Z_re, mu_Z_im, mu_Z_re2, mu_Z_im2, freq_fine, gamma_ridge_fine, epsilon, x_ridge = DRT_Lasso_RL.main(
    data,
    lambda0,
    coeff,
    Reg_type)

# 目前选取的数据特征点
Rct_feature = EIS_features.main(freq, mu_Z_re2, mu_Z_im2, x_ridge[2, 0], SOC)
# #
# fig = plt.figure(num=1, figsize=(8, 4))
# plt.plot(mu_Z_re2*1000000, -mu_Z_im2*1000000, "r-.d", label="Simu")
# # 设置坐标轴范围
# plt.xlim((300, 900))
# plt.ylim((-300, 300))
# plt.plot(realpart*1000000, -imagpart*1000000, "b-.d", label="Exp")
# plt.show()

delta_Rct = Rct_feature[0, 7] - Rct_feature[0, 3]
imag_Rct = -Rct_feature[0, 4]
# 是否外部添加温度信息 输入为-100则不添加
Temp_add = -100
if Temp_add != -100:
    Temperature_Rct_Estimation_all.Temp_deltaEIS_para_update(delta_Rct, Temp_add)
    Temperature_Rct_Estimation_all.Temp_SingleEIS_para_update(imag_Rct, Temp_add)
# 四种方法估计电池温度
Temp1, Temp2, Temp11, Temp21 = Temperature_Rct_Estimation_all.main(delta_Rct, imag_Rct)
# 也可以直接使用20Hz温度直接估计电池温度
Temp_20Hz = Temperature_Rct_Estimation_all.Temperature_SingleRct_Est(imag_Rct)

print(Temp1)
print(Temp2)
print(Temp11)
print(Temp21)
print(Temp_20Hz)
# 析锂等电池异常检测 只针对恒温的充放电过程
Pxili, R0_SOC, Rct1_Real_SOC, Rct1_imag_SOC, Rct2_Real_SOC, Rct2_imag_SOC = Abnormal_detection.main()
# 这里演示 R0_SOC 的绘制过程，其它可参考 共计5个图
fig = plt.figure(num=1, figsize=(8, 8))
# 设置每一个点的颜色 顺序按照由蓝到红显示
color_need = plt.get_cmap('hsv')(np.linspace(1, 0, round(1.2 * len(R0_SOC[:, 0]))))
for i in range(0, len(R0_SOC[:, 0]), 1):
    plt.plot(R0_SOC[i, 0], R0_SOC[i, 1], "*", color=color_need[i, :], markersize='20')
# 设置坐标轴范围
plt.xlim((min(R0_SOC[:, 0]) - (max(R0_SOC[:, 0]) - min(R0_SOC[:, 0])+30) * 0.1,
          max(R0_SOC[:, 0]) + (max(R0_SOC[:, 0]) - min(R0_SOC[:, 0])+30) * 0.1))
plt.ylim((-5, 105))
plt.yticks(fontproperties='Times New Roman', size=24)
plt.xticks(fontproperties='Times New Roman', size=24)
plt.xlabel('R0 (μΩ)', fontdict={'family': 'Times New Roman', 'size': 24})
plt.ylabel('SOC (%)', fontdict={'family': 'Times New Roman', 'size': 24})
plt.show()

print(Pxili)
