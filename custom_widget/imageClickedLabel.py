from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import  QSizePolicy

class ImageClickedLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, text, parent = None):
        super().__init__(text, parent)
        # self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # self.image = QPixmap(path)  # 替换为你的图片路径
        # self.text1 = f"电量:  %"
        # self.text2 = f"温度: °C"
        # # self.painter = QPainter(self)
        # # self.painter.drawPixmap(0, 0, self.image)
        # self.update()
        # 设置标签的背景为绿色，文字居中
        self.setStyleSheet("background-color: green; color: white; border: 1px solid black;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
        
        # 设置文字自动换行
        self.setWordWrap(True)
        
        # 设置自适应大小策略，保证标签根据内容大小自适应
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.drawPixmap(0, 0, self.image)
        
    #     # 设置字体和颜色
    #     font = QFont("Arial", 48)
    #     painter.setFont(font)
    #     painter.setPen(QColor(255, 0, 0))

    #     #计算文字位置使其位于图像中心
    #     text_width = max(painter.fontMetrics().boundingRect(self.text1).width(), painter.fontMetrics().boundingRect(self.text2).width())
    #     text_height = painter.fontMetrics().height() * 2
    #     text_x = (self.image.width() - text_width) // 2
    #     text_y = (self.image.height() - text_height) // 2


    #     # 绘制文字
    #     painter.drawText(text_x, text_y, self.text1)
    #     painter.drawText(text_x, text_y + painter.fontMetrics().height(), self.text2)

    # def update_text(self, battery_percent, temperature):
    #     self.text1 = f"电量: {battery_percent}%"
    #     self.text2 = f"温度: {temperature}°C"
    #     self.update()  # 通知窗口重绘