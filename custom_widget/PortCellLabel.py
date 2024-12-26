from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import  QSizePolicy
from PyQt6.QtGui import QFont
class PortCellLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
        text1 = f"模组号:  "
        self.setText(f"{text1}")

        # 设置标签的背景为绿色，文字居中
        self.setStyleSheet("background-color: gray; color: white; border: 1px solid black;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
        
        # 设置文字自动换行
        self.setWordWrap(True)
        
        # 设置自适应大小策略，保证标签根据内容大小自适应
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setFont(QFont("Arial", 14))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def update_text(self, port_number):
        print(f"设置模组号{port_number}")
        text1 = f"模组号: \n {port_number}号"
        self.setText(f"{text1}")
        self.repaint()  # 通知窗口重绘

    def clear_all(self):
        text1 = f"模组号:  "
        self.setText(f"{text1}")
        self.update()  # 通知窗口重绘
