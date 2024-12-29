import numpy as np
from scipy.spatial.distance import euclidean
from scipy.stats import zscore
from fastdtw import fastdtw
import json
import os

class EISAnalyzer:
    def __init__(self,distances={}):
        
        self.json_file = "./algorithm/data.json"
        self.distances = distances
        self.history_max = self.load_history_max()
        
    def load_history_max(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                return data.get('max_value', -float('inf'))  
        else:
            return -float('inf')  
        
    def save_history_max(self):
        with open(self.json_file, 'w') as f:
            json.dump({'max_value': self.history_max}, f)

    def normalize_results(self, results):
        values = np.array(list(results.values()))
        current_max = np.max(values)
        
        if current_max > self.history_max:
            self.history_max = current_max
            self.save_history_max()  

        min_val, max_val = 0, self.history_max 
        
        normalized = {key: (val - min_val) / (max_val - min_val) for key, val in results.items()}
        return normalized

    def normalize_curve(self, curve):
        """
        自定义归一化方法，将每个电池的实部和虚部归一化到 [0, 1]。
        """
        real, imag = curve
        # 对实部和虚部单独归一化
        real_normalized = (np.array(real) - np.min(real)) / (np.max(real) - np.min(real))
        imag_normalized = (np.array(imag) - np.min(imag)) / (np.max(imag) - np.min(imag))
        return real_normalized, imag_normalized


    def calculate_dtw_distance(self, curve1, curve2):
        """
        计算两个曲线的DTW距离
        """
        real1, imag1 = self.normalize_curve(curve1)
        real2, imag2 = self.normalize_curve(curve2)
        # real1, imag1 = curve1
        # real2, imag2 = curve2
        data1 = np.column_stack((real1, imag1))  # 归一化后合并
        data2 = np.column_stack((real2, imag2))
        dtw_distance, _ = fastdtw(data1, data2, dist=euclidean)
        return dtw_distance

    def calculate_consistency(self, epsilon=1e-6, scale_factor=5):
        """
        计算每个电池的一致性（归一化后）。
        """
        distances = self.distances
        for battery1, value in distances.items():
            if value !=0 :
                distances[battery1] = 1/(value+1)
            else:
                distances[battery1] = 1
        return distances

    def calculate_dispersion(self, curves):
        """
        计算每个电池的离散性（归一化后）。
        """
        distances = {}
        for battery1, curve1 in curves.items():
            all_distances = []
            for battery2, curve2 in curves.items():
                if battery1 != battery2:
                    dtw_distance = self.calculate_dtw_distance(curve1, curve2)
                    all_distances.append(dtw_distance)
            if len(all_distances) != 0:
                dispersion = np.mean(all_distances)  # 离散性定义为DTW距离的标准差
                distances[battery1] = dispersion
        self.distances = self.normalize_results(distances)
        return self.distances


    def detect_max_dispersion(self):
        distances = self.distances
        
        max_battery = max(distances, key=distances.get)
        max_dispersion = distances[max_battery]
    
        return max_battery, max_dispersion


if __name__ == '__main__':
    # 示例电池数据（实部和虚部阻抗）
    curves = {
    1: ([195, 194, 193], [-512, -511, -510]),  # Battery 1
    2: ([198, 197, 196], [-515, -514, -513]),  # Battery 2
    3: ([400, 401, 402], [-800, -801, -802]),  # Battery 3
    4: ([202, 201, 200], [-510, -509, -508]),  # Battery 4
    5: ([210, 209, 208], [-520, -519, -518]),  # Battery 5
    6: ([180, 179, 178], [-500, -501, -502]),  # Battery 6
    7: ([215, 214, 213], [-530, -529, -528]),  # Battery 7
    8: ([205, 204, 203], [-515, -514, -513]),  # Battery 8
    9: ([190, 189, 188], [-505, -504, -503]),  # Battery 9
    10: ([210, 211, 212], [-522, -521, -520]),  # Battery 10
    }

    # 创建分析器对象
    analyzer = EISAnalyzer(curves)

    # 计算离散性
    discrepancy = analyzer.calculate_dispersion(curves)
    print(f"Discrepancy: {discrepancy}")

    # 计算一致性
    consistency = analyzer.calculate_consistency(curves)
    print(f"Consistency: {consistency}")

    # 检测异常（方法1：基于z-score）
    # outliers = analyzer.detect_outliers()
    # print(f"Outliers (Method 1): {outliers}")

    # 检测异常（方法2：基于DTW相似度）
    outliers_method2 = analyzer.detect_outliers_method2()
    print(f"Outliers (Method 2): {outliers_method2}")
