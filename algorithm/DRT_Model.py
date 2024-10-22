import numpy as np
from Algorithm  import DRT_function
from PyQt6.QtCore import QObject
import threading
# import DRT_function
import matplotlib.pyplot as plt
import datetime as dt

class DRT_Model(QObject):
    # def __init__(self,data):
    #     self.data = data
    #     # super.__init__()
        
    # def DRT_start(self):
    #     self.thread = threading.Thread(target=self.run, daemon=True)
    #     self.thread.start()
    def run(self,data):
        # data = np.loadtxt('20.txt')
        data = np.array(data)
        data = data[:-1]
        # np.savetxt('data_float.txt', data)
        data = np.flipud(data)
        # data = np.round(data, 2)
    
        # print(data)

        coeff = 0.5
        lambda0 = 10 ** -3
        Reg_type = "Lasso"
        realpart, imagpart, mu_Z_re, mu_Z_im, freq_fine, gamma_ridge_fine = DRT_function.main(data, lambda0, coeff,Reg_type)

        fig = plt.figure(num=1, figsize=(12, 10))
        # ax1 = fig.add_subplot(121)
        # ax1.plot(mu_Z_re, -mu_Z_im, "r-.d", label="Simu")
        ax2 = fig.add_subplot(111)

        # realpart = np.flipud(realpart)
        # imagpart = np.flipud(imagpart)
        # ax1.plot(realpart, -imagpart, "b-.d", label="Exp")

        ax2.set_xscale("log")
        ax2.plot(1/freq_fine, gamma_ridge_fine, "r-.d", label="Exp")

        # ax1.set_xlabel('Real Impedance(mΩ)', fontsize=14)
        # ax1.set_ylabel('Negative Imaginary Impedance(mΩ)', fontsize=14) 
        # ax1.tick_params(axis='both', which='major', labelsize=12)

        ax2.set_xlabel(r'$\tau$ (s)', fontsize=22)
        ax2.set_ylabel(r'$g(\tau)$', fontsize=22) 

        ax2.tick_params(axis='both', which='major', labelsize=18)
        plt.legend()
        # plt.show()


        # Reg_type = "L2"
        # realpart, imagpart, mu_Z_re, mu_Z_im, freq_fine, gamma_ridge_fine = DRT_function.main(data, lambda0, coeff,Reg_type)
        

        # fig = plt.figure(num=1, figsize=(4, 4))
        # ax1 = fig.add_subplot(121)
        # ax1.plot(mu_Z_re, -mu_Z_im, "r-.d", label="Simu")
        # ax2 = fig.add_subplot(122)
        # ax1.plot(realpart, -imagpart, "b-.d", label="Exp")

        # ax2.set_xscale("log")
        # ax2.plot(1/freq_fine, gamma_ridge_fine, "r-.d", label="Exp")

        save_time = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        img_path = './result/DRT/{}.jpg'.format(save_time)
        # img_path = '../result/DRT/DRT.jpg'
        plt.savefig(img_path)
        return img_path

if __name__ == "__main__":
    data = np.loadtxt('array.txt')
    
    model = DRT_Model()
    model.run(data)