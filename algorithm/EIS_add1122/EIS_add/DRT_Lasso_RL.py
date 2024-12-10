import numpy as np
from scipy import optimize
import scipy.integrate as integrate
from numpy import exp
import cvxpy as cp
import os
import time


## 高斯函数
def rbf_gaussian_4_FWHM(x):
    y = np.exp(-x[0] ** 2) - 1 / 2
    return y


def cal_A(freq, epsilon, label):
    freq = np.array(freq)
    N = len(freq)
    freq_log = np.log10(freq)
    num_mag = np.round(1 / ((freq_log[0] - freq_log[-1]) / (N - 1)))
    ### 该值不要随意改动
    add_num = 0
    num = add_num * num_mag
    freq_add = freq[0:int(num[0])] * 10
    freq_M = np.append(freq_add, freq)
    freq_add = freq[N - int(num[0]):] / 10
    freq_M = np.append(freq_M, freq_add)
    len2 = N + add_num * num_mag * 2
    A_temp = np.zeros((N, int(len2[0])))
    # print(np.size(A_temp, 0))
    A = np.zeros((N, int(len2[0]) + 3))
    #  查看是否保存矩阵相关数据，若保存，直接调用
    # 查看文件夹是否存在
    if not os.path.exists('save_matrix_A'):
        os.mkdir('save_matrix_A')
    save_label = np.zeros(5).reshape(1, 5)
    save_label[0, 0] = np.round(freq[0])
    save_label[0, 1] = np.round(freq[-1])
    save_label[0, 2] = N
    save_label[0, 3] = label
    save_label[0, 4] = int(time.time())
    path = './save_matrix_A/freq_gather.txt'
    if not os.path.exists(path):
        ## compute using brute force
        for iter_freq_n in range(N):
            for iter_freq_m in range(int(len2[0])):
                freq_n = freq[iter_freq_n]
                freq_m = freq_M[iter_freq_m]
                a = g_i(freq_n, freq_m, epsilon, label)
                # print(a)
                A_temp[iter_freq_n, iter_freq_m] = g_i(freq_n, freq_m, epsilon, label)

        path_A = './save_matrix_A/' + str(int(save_label[0, 4])) + '.txt'
        with open(path_A, mode='x') as f:
            np.savetxt(f, A_temp, fmt='%.15f', delimiter=' ')
            f.close()

        with open(path, mode='x') as f:
            np.savetxt(f, save_label, fmt='%d', delimiter=' ')
            f.close()
    ## 如文件存在 则判断是否存在相同的结果
    else:
        flag_A = 0
        freq_gather_data = np.loadtxt(path)
        for row in freq_gather_data:
            data_row = row.reshape(1, -1)
            data_delta = np.abs(data_row[0, 0:4] - save_label[0, 0:4])
            data_delta_sum = np.sum(data_delta)
            if data_delta_sum < 1:
                path_A = './save_matrix_A/' + str(int(data_row[0, 4])) + '.txt'
                A_temp = np.loadtxt(path_A)
                flag_A = 1
                break

        ## compute using brute force
        if flag_A == 0:
            for iter_freq_n in range(N):
                for iter_freq_m in range(int(len2[0])):
                    freq_n = freq[iter_freq_n]
                    freq_m = freq_M[iter_freq_m]
                    a = g_i(freq_n, freq_m, epsilon, label)
                    # print(a)
                    A_temp[iter_freq_n, iter_freq_m] = g_i(freq_n, freq_m, epsilon, label)

            path_A = './save_matrix_A/' + str(int(save_label[0, 4])) + '.txt'
            with open(path_A, mode='x') as f:
                np.savetxt(f, A_temp, fmt='%.15f', delimiter=' ')
                f.close()

            with open(path, mode='a') as f:
                np.savetxt(f, save_label, fmt='%d', delimiter=' ')
                f.close()

    A[:, 3:] = A_temp
    return A, freq_M


def g_i(freq_n, freq_m, epsilon, label):
    alpha = 2 * np.pi * freq_n / freq_m
    # print(type(alpha))
    if label == 0:
        integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * exp(2 * x)) * exp(-(epsilon * x) ** 2)
        # integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * np.exp(2 * x))
    else:
        integrand_g_i = lambda x: -alpha / (1 / exp(x) + alpha ** 2 * exp(x)) * exp(-(epsilon * x) ** 2)
        # integrand_g_i = lambda x: 1 / (1 + alpha ** 2 * np.exp(2 * x))
    out_val = integrate.quad(integrand_g_i, -50, +50, epsabs=float(1E-9), epsrel=float(1E-9))
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


def cvxpy_solve_qp(H0, c):
    """
       This function uses cvxpy to minimize the quadratic problem 0.5*x^T*H*x + c^T*x under the non-negativity constraint.
       Inputs:
           H: matrix
           c: vector
        Output:
           Vector solution of the aforementioned problem
    """

    H = cp.psd_wrap(H0)
    N_out = c.shape[1]
    x = cp.Variable(shape=N_out, value=np.zeros(N_out), pos=True)
    h = np.zeros(N_out)
    G = np.eye(N_out)
    objective = cp.Minimize((1 / 2) * cp.quad_form(x, H) + c @ x)
    prob = cp.Problem(cp.Minimize((1 / 2) * cp.quad_form(x, H) + c @ x))
    prob.solve(verbose=False, eps_abs=1E-10, eps_rel=1E-10, sigma=1.00e-08,
               max_iter=200000, eps_prim_inf=1E-5, eps_dual_inf=1E-5, solver=cp.PROXQP)

    gamma = x.value

    return gamma


def main(data, lambda0, coeff, Reg_type):
    freq = data[:, 0].reshape(-1, 1)
    realpart = data[:, 1].reshape(-1, 1)
    imagpart = -data[:, 2].reshape(-1, 1)
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
    Are[::, [0]] = (2 * np.pi * freq) ** 2
    Are[::, [2]] = 1
    Aim[::, [1]] = 2 * np.pi * freq

    if Reg_type == "Lasso":
        M_temp = np.eye(len(freq), len(freq))
        M = np.zeros((len(freq) + 3, len(freq) + 3))
        M[3:, 3:] = M_temp
    else:
        M_temp = np.eye(len(freq_M), len(freq_M))
        M = np.zeros((len(freq_M) + 3, len(freq_M) + 3))
        M[3:, 3:] = M_temp

    H_combined, f_combined = quad_format_combined(Are, Aim, realpart, imagpart, M, lambda0, Reg_type)
    # print(H_combined)
    # print(f_combined)
    lb = np.zeros((len(freq_M) + 3, 1))
    ub = np.inf * np.ones((len(freq_M) + 3, 1))
    x_ridge = cvxpy_solve_qp(H_combined, f_combined)
    mu_Z_re = Are @ x_ridge.reshape(-1, 1)
    mu_Z_im = Aim @ x_ridge.reshape(-1, 1)
    x_ridge2 = x_ridge.reshape(-1, 1)
    x_ridge2[0, 0] = 0
    x_ridge2[0, 0] = 0
    x_ridge2[1, 0] = 0
    x_ridge2[1, 0] = 0
    mu_Z_re2 = Are @ x_ridge2
    mu_Z_im2 = Aim @ x_ridge2

    tau0max = np.ceil(max(np.log10(1. / freq_M))) + 0.5
    tau0min = np.floor(min(np.log10(1. / freq_M))) - 0.5
    freq_fine = np.logspace(-tau0min, -tau0max, 10 * len(freq_M))
    gamma_ridge_fine = map_array_to_gamma(freq_fine, freq_M, x_ridge[3:], epsilon)
    return realpart, imagpart, freq, mu_Z_re, mu_Z_im, mu_Z_re2, mu_Z_im2, freq_fine, gamma_ridge_fine, epsilon, x_ridge.reshape(
        -1, 1)
