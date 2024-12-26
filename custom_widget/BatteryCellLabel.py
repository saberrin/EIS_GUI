from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import  QSizePolicy
from PyQt6.QtGui import QFont
class BatteryCellLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
        text1 = f"电芯号:  "
        text2 = f"1KHz阻抗: \nm\u03A9"
        self.setText(f"{text1}\n{text2}")

        # 设置标签的背景为绿色，文字居中
        self.setStyleSheet("background-color: green; color: white; border: 1px solid black;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
        
        # 设置文字自动换行
        self.setWordWrap(True)
        
        # 设置自适应大小策略，保证标签根据内容大小自适应
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setFont(QFont("Arial", 12))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


    def update_text(self, cell_id, real_impedence):
        real_impedence = round(real_impedence,1)
        text1 = f"电芯号: {cell_id}"
        text2 = f"1KHz阻抗: \n{real_impedence}m\u03A9"
        self.setText(f"{text1}\n{text2}")
        self.update()  # 通知窗口重绘

    def clear_all(self):
        text1 = f"电芯号:  "
        text2 = f"1KHz阻抗: \nm\u03A9"
        self.setText(f"{text1}\n{text2}")
        self.update()  # 通知窗口重绘
