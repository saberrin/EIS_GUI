from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton,QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer
from tools.I2C_Reader import I2CReader
from ui.ui_parasetting import Ui_Dialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import  QFont
import json
import threading
from PyQt6.QtGui import QFont, QColor

class paraSetting(QDialog):
    update_ui_signal = pyqtSignal(str, str)  
    def __init__(self):
        super().__init__()
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # REMOVING WINDOWS TOP BAR AND MAKING IT FRAMELESS (AS WE HAVE AMDE A CUSTOME FRAME IN THE WINDOW ITSELF)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # MAKING THE WINDOW TRANSPARENT SO THAT TO GET A TRUE FLAT UI

        #-----> MINIMIZE BUTTON OF DIALOGBOX
        self.d.bn_min.clicked.connect(lambda: self.showMinimized())

        #-----> CLOSE APPLICATION FUNCTION BUTTON
        self.d.bn_close.clicked.connect(lambda: self.close())
        
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        
        self.bus_number = config.get("bus_number")
        self.address_list = [int(address, 16) for address in config.get("address_list", [])]
        self.I2C_Reader = I2CReader(bus_number=self.bus_number)
        self.confirmed_addresses = []
        self.failed_addresses = []
        self.d.bn_west.clicked.connect(self.start_thread)
        self.update_ui_signal.connect(self.show_message_box)
        self.current_msg_box = None
        
    def start_thread(self):
        result_message = ("参数配置中，请等待。。。" )
        self.update_ui_signal.emit('提示', result_message)
        thread = threading.Thread(target=self.update_para)
        thread.start()
        
    def send_data(self,data,address):
        self.I2C_Reader.write_data(data,address)
        expected_data = f"{hex(address)}_Received I2C_Command_{data}_end"
        if self.I2C_Reader.verify_data(data, address, expected_data): 
            print(f"Address {hex(address)} setting successfully.")
            self.confirmed_addresses.append(address) 
        else:
            print(f"Address {hex(address)} setting failed.")
            self.failed_addresses.append(address)
            
    def update_para(self):
        try:
            if self.I2C_Reader:
                for address in self.address_list:
                    command_SweepPoints = self.d.lineEdit.text().strip()
                    if command_SweepPoints:
                        command_SweepPoints = 'SET_SweepPoints_To_'+ command_SweepPoints + "\n"
                        self.send_data(command_SweepPoints,address)   

                    command_SweepModeEn = self.d.comboBox.currentText().strip()
                    if command_SweepModeEn == '单频':
                        command_SweepModeEn = 'SET_SweepModeEn_To_0' + "\n"
                        
                    else:
                        command_SweepModeEn = 'SET_SweepModeEn_To_1' + "\n"
                    self.send_data(command_SweepModeEn,address)  

                    command_SweepStartFreq = self.d.lineEdit_2.text().strip()
                    if command_SweepStartFreq:
                        command_SweepStartFreq = 'SET_SweepStartFreq_To_'+ command_SweepStartFreq + "\n"
                        self.send_data(command_SweepStartFreq,address) 

                    command_SweepStopFreq = self.d.lineEdit_6.text().strip()
                    if command_SweepStopFreq:
                        command_SweepStopFreq = 'SET_SweepStopFreq_To_'+ command_SweepStopFreq + "\n"
                        self.send_data(command_SweepStopFreq,address)   
                    
                    command_SET_SinFreq = self.d.lineEdit_3.text().strip()
                    if command_SET_SinFreq:
                        command_SET_SinFreq = 'SET_SinFreq_To_'+ command_SET_SinFreq + "\n"
                        self.send_data(command_SET_SinFreq,address) 

                    command_SET_ACVoltPP = self.d.lineEdit_7.text().strip()
                    if command_SET_ACVoltPP:
                        command_SET_ACVoltPP = 'SET_ACVoltPP_To_'+ command_SET_ACVoltPP + "\n"
                        self.send_data(command_SET_ACVoltPP,address) 

                    command_SET_DCVolt = self.d.lineEdit_4.text().strip()
                    if command_SET_DCVolt:
                        command_SET_DCVolt = 'SET_DCVolt_To_'+ command_SET_DCVolt + "\n"
                        self.send_data(command_SET_DCVolt,address) 

                    command_SET_RcalVal = self.d.lineEdit_8.text().strip()
                    if command_SET_RcalVal:
                        command_SET_RcalVal = 'SET_ RcalVal_To_'+ command_SET_RcalVal + "\n"
                        self.send_data(command_SET_RcalVal,address)

                    command_SET_SweepLog = self.d.comboBox_2.currentText().strip()
                    if command_SET_SweepLog == '线性比例':
                        command_SET_SweepLog = 'SET_SweepLog_To_0' + "\n"    
                    else:
                        command_SET_SweepLog = 'SET_SweepLog_To_1' + "\n"
                    self.send_data(command_SET_SweepLog,address) 
                result_message = (
                    f"参数设置完成\n\n"
                    f"成功地址{', '.join(hex(addr) for addr in self.confirmed_addresses)}\n"
                    f"失败地址{', '.join(hex(addr) for addr in self.failed_addresses)}"
                )
                self.update_ui_signal.emit('提示', result_message)        
        except AttributeError:
            self.update_ui_signal.emit('提示', 'I2C总线未连接')
            print("Attempted to write to a closed port.") 

    def show_message_box(self, title, message):
        # If a message box is already being displayed, close it first
        if self.current_msg_box:
            self.current_msg_box.close()

        # Create a new message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Set font size and color
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
        """)

        # Show the message box without blocking the thread
        msg_box.show()  # Use show() to display the message box without blocking

        # Save the current message box instance
        self.current_msg_box = msg_box

        
                

        
    



