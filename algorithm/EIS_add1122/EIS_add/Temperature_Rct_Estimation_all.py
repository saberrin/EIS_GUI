import numpy as np
from scipy.interpolate import interp1d
from numpy.linalg import lstsq


#
def sort_sel(exp_EIS0, exp_Temp0):
    # 先逆序阻抗温度数据
    exp_Temp1 = np.flip(exp_Temp0, axis=0)
    exp_EIS1 = np.flip(exp_EIS0, axis=0)
    # 求数组去重结果
    _, idx = np.unique(exp_Temp1, return_index=True)
    exp_EIS2 = exp_EIS1[idx, :]
    exp_Temp2 = exp_Temp1[idx, :]
    data = np.column_stack((exp_EIS2, exp_Temp2))
    data_sort = data[np.argsort(data[:, 1])]
    exp_EIS_out = data_sort[:, 0]
    exp_Temp_out = data_sort[:, 1]
    return exp_EIS_out, exp_Temp_out


# 数据尽量选择最新的数据
def data_sel(exp_EIS0, exp_Temp0):
    exp_EIS = exp_EIS0
    exp_Temp = exp_Temp0
    # 以原始数据为5个为参考
    if len(exp_Temp0) > 7:
        print(np.std(exp_Temp0[5:, 0]))
        if np.std(exp_Temp0[5:, 0]) > 10:
            exp_EIS = exp_EIS0[5:, 0].reshape(-1, 1)
            exp_Temp = exp_Temp0[5:, 0].reshape(-1, 1)

    return exp_EIS, exp_Temp


# 更新二次函数
def update_quadratic_para(exp_EIS0, exp_Temp0, save_path):
    exp_EIS, exp_Temp = data_sel(exp_EIS0, exp_Temp0)
    A = np.zeros([len(exp_EIS), 3])
    A[::, [0]] = np.ones([len(exp_EIS), 1])
    A[::, [1]] = exp_EIS
    A[::, [2]] = exp_EIS ** 2
    b = exp_Temp
    x = lstsq(A, b, rcond=None)
    quadratic_para = np.zeros([1, 3])
    quadratic_para[0, 0] = x[0].item(0)
    quadratic_para[0, 1] = x[0].item(1)
    quadratic_para[0, 2] = x[0].item(2)
    TEMP = quadratic_para[0, 0] + quadratic_para[0, 1] * exp_EIS[0, 0] + quadratic_para[0, 2] * exp_EIS[0, 0] * exp_EIS[
        0, 0]
    # 存储参数于Temp_delta_EIS_para.txt
    file = open(save_path, 'w')
    # 写入数据
    np.savetxt(file, quadratic_para, delimiter=' ')
    file.close()


# 输入对应的阻抗谱及温度
# 阻抗谱的特征信息已经被采集ct_feature = EIS_features函数采集
# 将温度-阻抗特性信息附加到txt文件最后
def Temp_deltaEIS_para_update(delta_Rct, Temp):
    # 附加阻抗信息
    # delta_Rct = Rct_feature[0,7] - Rct_feature[0,3]
    # delta_Rct = 1
    # 打开文件
    EIS_path = 'para_need/delta_EIS.txt'  # 文件路径
    file_mode = "a"  # 打开模式为追加写入（append mode）
    file = open(EIS_path, file_mode)
    # 写入数据
    file.write("\n" + str(delta_Rct))
    file.close()

    # 附加温度信息
    # Temp = 10
    # 打开文件
    temp_path = 'para_need/Temp_delta_EIS.txt'  # 文件路径
    file_mode = "a"  # 打开模式为追加写入（append mode）
    file = open(temp_path, file_mode)
    # 写入数据
    file.write("\n" + str(Temp))
    file.close()

    exp_EIS = np.loadtxt(EIS_path).reshape(-1, 1)
    exp_Temp = np.loadtxt(temp_path).reshape(-1, 1)
    update_quadratic_para(exp_EIS, exp_Temp, 'para_need/Temp_delta_EIS_para.txt')


# 输入对应的阻抗谱及温度
# 阻抗谱的特征信息已经被采集ct_feature = EIS_features函数采集
# 将温度-阻抗特性信息附加到txt文件最后
def Temp_SingleEIS_para_update(imag_Rct, Temp):
    # 附加阻抗信息
    # delta_Rct = Rct_feature[0,7] - Rct_feature[0,3]
    # delta_Rct = 1
    # 打开文件
    EIS_path = 'para_need/Iamg_SingleEIS.txt'  # 文件路径
    file_mode = "a"  # 打开模式为追加写入（append mode）
    file = open(EIS_path, file_mode)
    # 写入数据
    file.write("\n" + str(imag_Rct))
    file.close()

    # 附加温度信息
    # Temp = 10
    # 打开文件
    temp_path = 'para_need/Temp_Iamg_SingleEIS.txt'  # 文件路径
    file_mode = "a"  # 打开模式为追加写入（append mode）
    file = open(temp_path, file_mode)
    # 写入数据
    file.write("\n" + str(Temp))
    file.close()

    exp_EIS = np.loadtxt(EIS_path).reshape(-1, 1)
    exp_Temp = np.loadtxt(temp_path).reshape(-1, 1)
    update_quadratic_para(exp_EIS, exp_Temp, 'para_need/Temp_Single_EIS_para.txt')


# 初始化数据
def initial_value():
    # 复杂信息 delta_Rct
    EIS_path = 'para_need/delta_EIS.txt'  # 文件路径
    temp_path = 'para_need/Temp_delta_EIS.txt'  # 文件路径
    exp_EIS = np.loadtxt(EIS_path).reshape(-1, 1)
    exp_Temp = np.loadtxt(temp_path).reshape(-1, 1)
    update_quadratic_para(exp_EIS, exp_Temp, 'para_need/Temp_delta_EIS_para.txt')

    # 单频信息 imag_Rct
    EIS_path = 'para_need/Iamg_SingleEIS.txt'  # 文件路径
    temp_path = 'para_need/Temp_Iamg_SingleEIS.txt'  # 文件路径
    exp_EIS = np.loadtxt(EIS_path).reshape(-1, 1)
    exp_Temp = np.loadtxt(temp_path).reshape(-1, 1)
    update_quadratic_para(exp_EIS, exp_Temp, 'para_need/Temp_Single_EIS_para.txt')


def Temperature_deltaRct_Est(delta_Rct):
    # 输入当前电池阻抗特征值
    exp_delta_EIS0 = np.loadtxt('para_need/delta_EIS.txt').reshape(-1, 1)
    exp_Temp0 = np.loadtxt('para_need/Temp_delta_EIS.txt').reshape(-1, 1)
    exp_delta_EIS1, exp_Temp1 = data_sel(exp_delta_EIS0, exp_Temp0)
    exp_delta_EIS, exp_Temp = sort_sel(exp_delta_EIS1, exp_Temp1)
    f = interp1d(exp_delta_EIS, exp_Temp, kind='linear', bounds_error=False, fill_value=(0, 60))
    Temp = f(delta_Rct)
    return Temp


def Temperature_deltaRct_Est1(delta_Rct):
    # 输入当前电池阻抗特征值
    exp_para = np.loadtxt('para_need/Temp_delta_EIS_para.txt')
    para = np.array(exp_para).reshape(1, -1)
    Temp = para[0, 0] + para[0, 1] * delta_Rct + para[0, 2] * delta_Rct * delta_Rct
    return Temp


def Temperature_SingleRct_Est(imag_Rct):
    # 输入当前电池阻抗特征值
    exp_Single_EIS0 = np.loadtxt('para_need/Iamg_SingleEIS.txt').reshape(-1, 1)
    exp_Single_Temp0 = np.loadtxt('para_need/Temp_Iamg_SingleEIS.txt').reshape(-1, 1)
    exp_Single_EIS1, exp_Single_Temp1 = data_sel(exp_Single_EIS0, exp_Single_Temp0)
    exp_Single_EIS, exp_Single_Temp = sort_sel(exp_Single_EIS1, exp_Single_Temp1)
    f = interp1d(exp_Single_EIS, exp_Single_Temp, kind='linear', bounds_error=False, fill_value=(0, 60))
    Temp = f(imag_Rct)
    return Temp


def Temperature_SingleRct_Est1(imag_Rct):
    # 输入当前电池阻抗特征值
    exp_para = np.loadtxt('para_need/Temp_Single_EIS_para.txt')
    para = np.array(exp_para).reshape(1, -1)
    Temp = para[0, 0] + para[0, 1] * imag_Rct + para[0, 2] * imag_Rct * imag_Rct
    return Temp


def main(delta_Rct, imag_Rct):
    initial_value()
    # 线性插值预测
    Temp1 = Temperature_deltaRct_Est(delta_Rct)
    Temp2 = Temperature_SingleRct_Est(imag_Rct)
    #
    # 复杂信息 不太好用
    Temp11 = Temperature_deltaRct_Est1(delta_Rct)
    # 单频信息 还可以
    Temp21 = Temperature_SingleRct_Est1(imag_Rct)
    # 权重设置 自己随便设
    return Temp1, Temp2, Temp11, Temp21
