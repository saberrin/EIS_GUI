from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton,QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer
import serial
from serial_reader import SerialReader
from ui_parasetting import Ui_Dialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import  QFont
class paraSetting(QDialog):
    def __init__(self):
        super().__init__()
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # REMOVING WINDOWS TOP BAR AND MAKING IT FRAMELESS (AS WE HAVE AMDE A CUSTOME FRAME IN THE WINDOW ITSELF)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # MAKING THE WINDOW TRANSPARENT SO THAT TO GET A TRUE FLAT UI

        #############################################################################################                        -------(C1)
        #SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        #DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        #-----> MINIMIZE BUTTON OF DIALOGBOX
        self.d.bn_min.clicked.connect(lambda: self.showMinimized())

        #-----> CLOSE APPLICATION FUNCTION BUTTON
        self.d.bn_close.clicked.connect(lambda: self.close())
        
        self.serial_reader = None
        self.d.bn_west.clicked.connect(self.update_para)
    def get_reader(self, reader):
        self.serial_reader = reader

    def update_para(self):
        try:
            if self.serial_reader and self.serial_reader.isOpen():
                command_SweepPoints = self.d.lineEdit.text().strip()
                if command_SweepPoints:
                    command_SweepPoints = 'SET_SweepPoints_To_'+ command_SweepPoints + "\n"
                    self.serial_reader.write_data(command_SweepPoints)   

                command_SweepModeEn = self.d.comboBox.currentText().strip()
                if command_SweepModeEn == '单频':
                    command_SweepModeEn = 'SET_SweepModeEn_To_0' + "\n"
                    
                else:
                    command_SweepModeEn = 'SET_SweepModeEn_To_1' + "\n"
                self.serial_reader.write_data(command_SweepModeEn)  

                command_SweepStartFreq = self.d.lineEdit_2.text().strip()
                if command_SweepStartFreq:
                    command_SweepStartFreq = 'SET_SweepStartFreq_To _'+ command_SweepStartFreq + "\n"
                    self.serial_reader.write_data(command_SweepStartFreq) 

                command_SweepStopFreq = self.d.lineEdit_6.text().strip()
                if command_SweepStopFreq:
                    command_SweepStopFreq = 'SET_SweepStopFreq_To_'+ command_SweepStopFreq + "\n"
                    self.serial_reader.write_data(command_SweepStopFreq)   
                
                command_SET_SinFreq = self.d.lineEdit_3.text().strip()
                if command_SET_SinFreq:
                    command_SET_SinFreq = 'SET_SinFreq_To_'+ command_SET_SinFreq + "\n"
                    self.serial_reader.write_data(command_SET_SinFreq) 

                command_SET_ACVoltPP = self.d.lineEdit_7.text().strip()
                if command_SET_ACVoltPP:
                    command_SET_ACVoltPP = 'SET_ACVoltPP_To_'+ command_SET_ACVoltPP + "\n"
                    self.serial_reader.write_data(command_SET_ACVoltPP) 

                command_SET_DCVolt = self.d.lineEdit_4.text().strip()
                if command_SET_DCVolt:
                    command_SET_DCVolt = 'SET_DCVolt_To_'+ command_SET_DCVolt + "\n"
                    self.serial_reader.write_data(command_SET_DCVolt) 

                command_SET_RcalVal = self.d.lineEdit_8.text().strip()
                if command_SET_RcalVal:
                    command_SET_RcalVal = 'SET_ RcalVal_To_'+ command_SET_RcalVal + "\n"
                    self.serial_reader.write_data(command_SET_RcalVal)

                command_SET_SweepLog = self.d.comboBox_2.currentText().strip()
                if command_SET_SweepLog == '线性比例':
                    command_SET_SweepLog = 'SET_SweepLog_To_0' + "\n"    
                else:
                    command_SET_SweepLog = 'SET_SweepLog_To_1' + "\n"
                self.serial_reader.write_data(command_SET_SweepLog) 

                QMessageBox.about(self, '提示', '参数设置完成')        
        except(AttributeError):
            QMessageBox.about(self, '提示', '请先建立端口连接！')
            print("Attempted to write to a closed serial port.") 
        
                

        
    



