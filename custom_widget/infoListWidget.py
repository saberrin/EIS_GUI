from PyQt6.QtWidgets import  QVBoxLayout, QTableView, QWidget,QHeaderView,QHBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class infoListView(QWidget):
    def __init__(self):
        super().__init__()
        self.fontsize = 16
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

        

