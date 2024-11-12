import sys
import time
import sqlite3


#IMPORTING ALL THE NECESSERY PYSIDE2 MODULES FOR OUR APPLICATION.
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import ( QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent) 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt6 import uic
from ui.ui_function import * # A FILE WHERE ALL THE FUNCTION LIKE BUTTON PRESSES, SILDER, PROGRESS BAR E.T.C ARE DONE.
from ui.ui_main import Ui_MainWindow # MAINWINDOW CODE GENERATED BY THE QT DESIGNER AND pyside2-uic.
from custom_widget.menuWidget import MenuWidget
from custom_widget.imageClickedLabel import ImageClickedLabel
from database.db_init import init_database
from custom_widget.initSetting import initSetting
from tools.I2C_Reader import I2CReader

# OUR APPLICATION MAIN WINDOW :
#-----> MAIN APPLICATION CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn, self.cursor = init_database()
        UIFunction.constantFunction(self) 
        UIFunction.maximize_restore(self)
        
        
        #菜单栏
        self.menu = MenuWidget() 
        self.ui.horizontalLayout_21.addWidget(self.menu)

        self.init_batterycell()
        self.ui.pushButton.clicked.connect(lambda: self.switchPage(0))
        self.reader = None
        self.ui.pushButton_3.clicked.connect(lambda: self.start_loop())
        self.ui.pushButton_4.clicked.connect(lambda:self.stop_loop())
        self.ui.pushButton_4.setEnabled(False)

    def init_batterycell(self):
        self.ui.batteryList = []
        for row in range(4):
            for col in range(13):
                label = ImageClickedLabel(f"Label {row+1},{col+1}", self)
                self.ui.batteryList.append(label)
                self.ui.gridLayout.addWidget(label, row, col)  # 添加到布局中
        for i in range(52):
            self.ui.batteryList[i].clicked.connect(lambda: self.switchPage(1))

    def switchPage(self, index):
        print(f"clicked by{index}")
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def start_loop(self):
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)

        self.settingId = initSetting()
        self.settingId.identifier.connect(self.identifier_setting)
        self.settingId.exec()
        address_list = [0x26,0x27,0x28,0x29]
        
        for address in (address_list):
            self.reader = I2CReader(device='/dev/i2c-11', bus_number=11)
            self.reader.start_reading(address)

    def stop_loop(self):
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(False)
        if self.reader is not None:
            self.reader.close()
         
    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
      
    def identifier_setting(self,container_number,cabinet_number,cluster_number):
        self.ui.label_14.setText(f"集装箱-{container_number}-电池柜-{cabinet_number}-电池包-{cluster_number}")

        # Insert the values into the database
        try:
            # Insert into container table
            self.cursor.execute("INSERT OR IGNORE INTO container (container_id) VALUES (?)", (container_number,))

            # Insert into battery_cabinet table
            self.cursor.execute("INSERT OR IGNORE INTO battery_cabinet (cabinet_id, container_id) VALUES (?, ?)", (cabinet_number, container_number))

            # Insert into battery_cluster table
            self.cursor.execute("INSERT OR IGNORE INTO battery_cluster (cluster_id, cabinet_id) VALUES (?, ?)", (cluster_number, cabinet_number))

            # Commit the changes to save the data
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

