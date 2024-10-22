import numpy as np
import math
from scipy import optimize
import scipy.integrate as integrate
from qpsolvers import solve_qp


## 高斯函数
def rbf_gaussian_4_FWHM(x):
    y = math.exp(-x[0] ** 2) - 1 / 2
    return y


def cal_A(freq, epsilon, label):
    freq = np.array(freq)
    N = len(freq)
    freq_log = np.log10(freq)
    num_mag = np.round(1 / ((freq_log[0] - freq_log[-1]) / (N - 1)))
    add_num = 1
    num = add_num * num_mag
    freq_add = freq[0:int(num[0])] * 10
    freq_M = np.append(freq_add, freq)
    freq_add = freq[N - int(num[0]):] / 10
    freq_M = np.append(freq_M, freq_add)
    len2 = N + add_num * num_mag * 2
    A_temp = np.zeros((N, int(len2[0])))
    # print(np.size(A_temp, 0))
    A = np.zeros((N, int(len2[0]) + 2))
    # compute using brute force
    for iter_freq_n in range(N):
        for iter_freq_m in range(int(len2[0])):
            freq_n = freq[iter_freq_n]
            freq_m = freq_M[iter_freq_m]
            a = g_i(freq_n, freq_m, epsilon, label)
            # print(a)
            A_temp[iter_freq_n, iter_freq_m] = g_i(freq_n, freq_m, epsilon, label)

        A[:, 2:] = A_temp

    return A, freq_M


def g_i(freq_n, freq_m, epsilon, label):
    alpha = 2 * math.pi * freq_n / freq_m
    # print(type(alpha))
    if label == 0:
        integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * np.exp(2 * x)) * np.exp(-(epsilon * x) ** 2)
        # integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * np.exp(2 * x))
    else:
        integrand_g_i = lambda x: -alpha / (1 / np.exp(x) + alpha ** 2 * np.exp(x)) * np.exp(-(epsilon * x) ** 2)
        # integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * np.exp(2 * x))
    out_val = integrate.quad(integrand_g_i, -np.inf, +np.inf, epsabs=float(1E-9), epsrel=float(1E-9))
    return out_val[0]


def quad_format_combined(A_re, A_im, b_re, b_im, M, lambda0, Reg_type):
    if Reg_type == "Lasso":
        H = 2 * (np.dot(A_re.T, A_re) + np.dot(A_im.T, A_im))
        H = (H.T + H) / 2
        c = -2 * (b_im.T @ A_im + b_re.T @ A_re) + lambda0 * np.ones((1, np.size(H, 1)))
    elif Reg_type == "L2":
        H = 2 * (np.dot(A_re.T, A_re) + np.dot(A_im.T, A_im) + lambda0 * M)
        H = (H.T + H) / 2
        c = -2 * (b_im.T @ A_im + b_re.T @ A_re)
    else:
        print("无类型选项，使用L2回归")
        H = 2 * (np.dot(A_re.T, A_re) + np.dot(A_im.T, A_im) + lambda0 * M)
        H = (H.T + H) / 2
        c = -2 * (b_im.T @ A_im + b_re.T @ A_re)
    return H, c


def map_array_to_gamma(freq_fine, freq, x_ridge, epsilon):
    rbf = lambda y, y0: np.exp(-(epsilon * (y - y0)) ** 2)
    y0 = -np.log(freq.T)
    gamma_ridge_fine = np.zeros(len(freq_fine))
    for iter_freq_map in range(len(freq_fine)):
        freq_loc = freq_fine[iter_freq_map]
        y = -np.log(freq_loc)
        gamma_ridge_fine[iter_freq_map] = x_ridge.T @ rbf(y, y0)
    return gamma_ridge_fine


def main(data, lambda0, coeff, Reg_type):
    freq = data[:, 0].reshape(-1, 1)
    realpart = data[:, 1].reshape(-1, 1)
    imagpart = data[:, 2].reshape(-1, 1)
    a = np.mat([1, 2])
    ## 定义高斯函数类型

    FWHM_coeff = 2 * optimize.fsolve(rbf_gaussian_4_FWHM, np.array([1]))
    delta = np.average(np.diff(np.log(1. / freq), 1, axis=0))
    # print(delta)
    epsilon = coeff * FWHM_coeff / delta
    # print(epsilon)


    Are, freq_M = cal_A(freq, epsilon, 0)
    Aim, _ = cal_A(freq, epsilon, 1)
    # print(Are.shape)
    Are[::, [1]] = 1
    Aim[::, [0]] = 2 * math.pi * freq

    if Reg_type == "Lasso":
        M_temp = np.eye(len(freq), len(freq))
        M = np.zeros((len(freq) + 2, len(freq) + 2))
        M[2:, 2:] = M_temp
    else:
        M_temp = np.eye(len(freq_M), len(freq_M))
        M = np.zeros((len(freq_M) + 2, len(freq_M) + 2))
        M[2:, 2:] = M_temp

    H_combined, f_combined = quad_format_combined(Are, Aim, realpart, imagpart, M, lambda0, Reg_type)
    # print(H_combined)
    # print(f_combined)
    lb = np.zeros((len(freq_M) + 2, 1))
    ub = np.inf * np.ones((len(freq_M) + 2, 1))
    x_ridge = solve_qp(H_combined, f_combined, None, None, None, None, lb, ub, solver="proxqp")
    # print(f"QP solution: {x_ridge = }")
    mu_Z_re = Are @ x_ridge
    mu_Z_im = Aim @ x_ridge

    tau0max = np.ceil(max(np.log10(1. / freq_M))) + 0.5
    tau0min = np.floor(min(np.log10(1. / freq_M))) - 0.5
    freq_fine = np.logspace(-tau0min, -tau0max, 10 * len(freq_M))
    gamma_ridge_fine = map_array_to_gamma(freq_fine, freq_M, x_ridge[2:], epsilon)
    return realpart, imagpart, mu_Z_re, mu_Z_im, freq_fine, gamma_ridge_fine
