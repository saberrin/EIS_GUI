import numpy as np
from scipy.interpolate import interp1d


def SOC_OCV_Est(U):
    # 输入当前电池电压即可
    exp_OCVd = np.loadtxt('para_need/OCVd.txt')
    exp_SOCd = np.loadtxt('para_need/SOCd.txt')
    exp_OCVc = np.loadtxt('para_need/OCVc.txt')
    exp_SOCc = np.loadtxt('para_need/SOCc.txt')
    fd = interp1d(exp_OCVd, exp_SOCd, kind='linear', bounds_error=False,fill_value=(0, 1))
    fc = interp1d(exp_OCVc, exp_SOCc, kind='linear', bounds_error=False,fill_value=(0, 1))
    SOCd = fd(U)
    SOCc = fc(U)
    SOC = (SOCd + SOCc) / 2
    return SOC
