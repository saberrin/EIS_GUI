import numpy as np
from scipy.spatial.distance import euclidean
from scipy.stats import zscore
from fastdtw import fastdtw

class EISAnalyzer:
    def __init__(self, curves):
        self.curves = curves
        self.frequency_points = len(next(iter(curves.values()))[0])  # 获取数据的频率点数量

    def normalize_curve(self, curve):
        """
        自定义归一化方法，将每个电池的实部和虚部归一化到 [0, 1]。
        """
        real, imag = curve
        # 对实部和虚部单独归一化
        real_normalized = (np.array(real) - np.min(real)) / (np.max(real) - np.min(real))
        imag_normalized = (np.array(imag) - np.min(imag)) / (np.max(imag) - np.min(imag))
        return real_normalized, imag_normalized
    
    def normalize_results(self, results):
        values = np.array(list(results.values()))
        min_val, max_val = np.min(values), np.max(values)
        normalized = {key: (val - min_val) / (max_val - min_val) for key, val in results.items()}
        return normalized

    def calculate_dtw_distance(self, curve1, curve2):
        """
        计算两个曲线的DTW距离（在归一化后）。
        """
        real1, imag1 = self.normalize_curve(curve1)
        real2, imag2 = self.normalize_curve(curve2)
        # real1, imag1 = curve1
        # real2, imag2 = curve2
        data1 = np.column_stack((real1, imag1))  # 归一化后合并
        data2 = np.column_stack((real2, imag2))
        dtw_distance, _ = fastdtw(data1, data2, dist=euclidean)
        return dtw_distance

    def calculate_consistency(self, curves):
        """
        计算每个电池的一致性（归一化后）。
        """
        distances = {}
        for battery1, curve1 in curves.items():
            total_distance = 0
            for battery2, curve2 in curves.items():
                if battery1 != battery2:
                    dtw_distance = self.calculate_dtw_distance(curve1, curve2)
                    total_distance += dtw_distance
            consistency = 1 / (total_distance / (len(curves) - 1))  # 一致性定义为DTW距离的倒数
            distances[battery1] = consistency
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
            dispersion = np.mean(all_distances)  # 离散性定义为DTW距离的标准差
            distances[battery1] = dispersion
        return distances

    def detect_outliers(self, threshold=3.0):
        """
        基于z-score进行异常检测（归一化后）。
        """
        all_real = np.array([self.normalize_curve(curve)[0] for curve in self.curves.values()])
        all_imag = np.array([self.normalize_curve(curve)[1] for curve in self.curves.values()])
        real_zscore = zscore(all_real, axis=0)
        imag_zscore = zscore(all_imag, axis=0)

        outlier_indices = np.unique(np.where((np.abs(real_zscore) > threshold) | (np.abs(imag_zscore) > threshold))[0])
        return [list(self.curves.keys())[i] for i in outlier_indices]

    def detect_outliers_method2(self, threshold=-0.1):
        """
        基于DTW距离的相似度进行异常检测（归一化后）。
        """
        keys = list(self.curves.keys())
        similarity_scores = {key: [] for key in keys}

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                curve1 = self.curves[keys[i]]
                curve2 = self.curves[keys[j]]
                dtw_distance = self.calculate_dtw_distance(curve1, curve2)
                similarity = -dtw_distance  # 使用负DTW距离作为相似度
                similarity_scores[keys[i]].append(similarity)
                similarity_scores[keys[j]].append(similarity)

        mean_similarity = {key: np.mean(similarities) for key, similarities in similarity_scores.items()}
        outliers = [key for key, mean_sim in mean_similarity.items() if mean_sim < threshold]
        return outliers

if __name__ == '__main__':
    # 示例电池数据（实部和虚部阻抗）
    curves = {
        1: ([195, 194, 193], [-512, -511, -510]),  # Battery 1
        2: ([198, 197, 196], [-515, -514, -513]),  # Battery 2
        3: ([400, 401, 402], [-800, -801, -802]),  # Battery 3 
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
    outliers = analyzer.detect_outliers()
    print(f"Outliers (Method 1): {outliers}")

    # 检测异常（方法2：基于DTW相似度）
    outliers_method2 = analyzer.detect_outliers_method2()
    print(f"Outliers (Method 2): {outliers}")
