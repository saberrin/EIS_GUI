from PyQt6.QtWidgets import  QVBoxLayout, QTableView, QWidget,QHeaderView,QHBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from collections import defaultdict
from algorithm.EISAnalyzer import EISAnalyzer
import numpy as np
from database.repository import Repository

class infoListView(QWidget):
    def __init__(self):
        super().__init__()

        self.repo = Repository()
        self.fontsize = 12
        # 创建一个垂直布局
        self.layout = QHBoxLayout(self)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 创建一个列表视图
        self.tableView = QTableView()
        self.layout.addWidget(self.tableView)
        self.layout.setStretch(0, 1)  
        # 创建一个标准项目模型
        self.model = QStandardItemModel(1,6)

        # 将模型设置到列表视图中
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().hide()
        self.tableView.verticalHeader().hide()
        self.tableView.setShowGrid(False)

        # self.tableView.verticalHeader().setDefaultSectionSize(65) 
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # 列宽自适应
        for col in range(6):
            self.tableView.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        
        # 添加一些数据项到模型中
        lists = ["平均离散度:", "平均一致性:", "离散最大电芯:"]
        for col,list in enumerate(lists):
            item = QStandardItem(list)
            item.setForeground(QColor(255, 255, 255))  # 设置文本颜色为白色
            font = item.font()
            font = QFont("Arial", self.fontsize)
            font.setBold(True)                  # 设置字体加粗
            item.setFont(font)             # 应用字体
            self.model.setItem(0, 2*col, item)

    def update_data(self,lists):
        data = []
        for cell_id in lists:
            data.append(self.repo.get_cell_measurements(cell_id))
        result = defaultdict(lambda: ([], []))  
        for measurements in data:
            for measurement in measurements:
                cell_id = f"Battery{measurement.cell_id}"  
                result[cell_id][0].append(measurement.real_impedance)  
                result[cell_id][1].append(measurement.imag_impedance)  
        result = dict(result)
        analyzer = EISAnalyzer(result)
        discrepancy = analyzer.calculate_dispersion(result)
        discrepancy = np.mean(np.array(list(discrepancy.values())))
        consistency = analyzer.calculate_consistency(result)
        consistency = np.mean(np.array(list(consistency.values())))
        outliers,max_dispersion = analyzer.detect_max_dispersion()
        self.populate_data(discrepancy, consistency, outliers, max_dispersion)

    def populate_data(self,dispersion, consistency, outliers,max_dispersion):
        dispersion = round(dispersion,2)
        consistency = round(consistency,2)
        lists = [str(dispersion)+"%", str(consistency)+"%", str(outliers)] 
        # 将数据添加到模型中
        for col, list in enumerate(lists):
            item = QStandardItem(str(list))
            item.setForeground(QColor(255, 255, 255))  # 设置文本颜色为白色
            font = item.font()
            font = QFont("Arial", self.fontsize)
            font.setBold(True)                  # 设置字体加粗
            item.setFont(font)  
            self.model.setItem(0, 2*col+1, item)

    def clear_all(self):
        for col in range(1, 6, 2):  # Only clearing the columns where data is populated (1, 3, 5)
            self.model.setItem(0, col, QStandardItem(''))  # Reset to empty item

