from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton,QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer
from ui.ui_initSetting import Ui_initSetting
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import  QFont
from PyQt6 import uic
CONTAINER_NUMBER = 2
CABINET_NUMBER = 20
CLUSTER_NUMBER = 8
class initSetting(QDialog):
    identifier = pyqtSignal(int, int, int)
    def __init__(self):
        super().__init__()
        self.d = Ui_initSetting()
        self.d.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # REMOVING WINDOWS TOP BAR AND MAKING IT FRAMELESS (AS WE HAVE AMDE A CUSTOME FRAME IN THE WINDOW ITSELF)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # MAKING THE WINDOW TRANSPARENT SO THAT TO GET A TRUE FLAT UI

        self.d.comboBox_2.addItem("请选择")
        self.d.comboBox_3.addItem("请选择")
        self.d.comboBox.addItem("请选择")
        self.d.comboBox_2.addItems([str(i) for i in range(1, CONTAINER_NUMBER + 1)])
        self.d.comboBox_3.addItems([str(i) for i in range(1, CABINET_NUMBER + 1)])
        self.d.comboBox.addItems([str(i) for i in range(1, CLUSTER_NUMBER + 1)])

        self.d.pushButton_2.clicked.connect(self.update_para)
    def update_para(self):
        container = self.d.comboBox_2.currentText()
        cabinet = self.d.comboBox_3.currentText()
        cluster = self.d.comboBox.currentText()

        if container != "请选择" and cabinet != "请选择" and cluster != "请选择":
            try:
                container_int = int(container)
                cabinet_int = int(cabinet)
                cluster_int = int(cluster)
                self.identifier.emit(container_int,cabinet_int,cluster_int)
                self.close()
                QMessageBox.about(self, '提示', '编号设置完成！')
            except ValueError:
                QMessageBox.about(self, '提示', '编号必须是有效的数字！')
        else:
            QMessageBox.about(self, '提示', '请完成所有编号设置！')
    