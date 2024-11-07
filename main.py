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

        self.ui.pushButton_3.clicked.connect(lambda: self.start_loop())

        

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
        self.settingId = initSetting()
        self.settingId.identifier.connect(self.identifier_setting)
        self.settingId.exec()
        
        self.reader = I2CReader(device='/dev/i2c-11', bus_number=11,address=0x28)
        self.reader.start_reading()
        
        
    # Example usage of the cursor to fetch the recently inserted IDs
        if self.cursor:
            # Fetch the latest container ID
            self.cursor.execute("SELECT container_id FROM container ORDER BY container_id DESC LIMIT 1")
            container_id = self.cursor.fetchone()
            
            if container_id is not None:
                print("Latest container_id:", container_id[0])
                
                # Fetch the latest cabinet ID related to the container
                self.cursor.execute("SELECT cabinet_id FROM battery_cabinet WHERE container_id = ? ORDER BY cabinet_id DESC LIMIT 1", (container_id[0],))
                cabinet_id = self.cursor.fetchone()
                
                if cabinet_id is not None:
                    print("Latest cabinet_id:", cabinet_id[0])
                    
                    # Fetch the latest cluster ID related to the cabinet
                    self.cursor.execute("SELECT cluster_id FROM battery_cluster WHERE cabinet_id = ? ORDER BY cluster_id DESC LIMIT 1", (cabinet_id[0],))
                    cluster_id = self.cursor.fetchone()
                    
                    if cluster_id is not None:
                        print("Latest cluster_id:", cluster_id[0])
                    else:
                        print("No cluster_id found for the latest cabinet.")
                else:
                    print("No cabinet_id found for the latest container.")
            else:
                print("No container_id found in the container table.")

    def closeEvent(self, event):
        # Close the database connection on exit
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        event.accept()
        # self.ui = uic.loadUi("./ui/ui_main.ui", self)
        

        
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

