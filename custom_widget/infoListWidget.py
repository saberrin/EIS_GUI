from PyQt6.QtWidgets import  QVBoxLayout, QTableView, QWidget,QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class infoListView(QWidget):
    def __init__(self):
        super().__init__()
        self.fontsize = 8
        # 创建一个垂直布局
        self.layout = QVBoxLayout(self)

        # 创建一个列表视图
        self.tableView = QTableView()
        self.layout.addWidget(self.tableView)

        # 创建一个标准项目模型
        self.model = QStandardItemModel(1,6)

        # 将模型设置到列表视图中
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().hide()
        self.tableView.verticalHeader().hide()
        self.tableView.setShowGrid(False)

        # self.tableView.verticalHeader().setDefaultSectionSize(30) 
        

        self.tableView.horizontalHeader().setDefaultSectionSize(40)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 列0：固定大小
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # 列1：固定大小
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # 列2：自动调整大小
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 列3：固定大小
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # 列2：自动调整大小
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 列3：固定大小
        # self.tableView.horizontalHeader().setMaximumSectionSize(24)
        
        # 添加一些数据项到模型中
        lists = ["离散度:", "一致性:", "异常电芯:"]
        for col,list in enumerate(lists):
            item = QStandardItem(list)
            item.setForeground(QColor(255, 255, 255))  # 设置文本颜色为白色
            font = item.font()
            font = QFont("Arial", self.fontsize)
            font.setBold(True)                  # 设置字体加粗
            item.setFont(font)             # 应用字体
            self.model.setItem(0, 2*col, item)
        

    def populate_data(self,dispersion, consistency, outliers):
        # 一些示例数据
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

        

