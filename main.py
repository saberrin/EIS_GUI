import sys
import os
import time
import sqlite3



#IMPORTING ALL THE NECESSERY PYSIDE2 MODULES FOR OUR APPLICATION.
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import ( QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent) 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QBrush, QPixmap, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
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
from custom_widget.nyquist_plot import NyquistPlot
from tools.heatmap_plt import HeatMap3DWidget
from custom_widget.infoListWidget import infoListView
from database.repository import Repository
from collections import defaultdict
from algorithm.EISAnalyzer import EISAnalyzer
from custom_widget.nyquist_plot_history import NyquistPlotHistory
import json
# OUR APPLICATION MAIN WINDOW :
#-----> MAIN APPLICATION CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.repo = Repository()
        # Initialize database
        self.conn, self.cursor = init_database()
        UIFunction.constantFunction(self)
        UIFunction.maximize_restore(self)
        
        # Initialize menu and layout
        self.menu = MenuWidget()
        self.ui.horizontalLayout_21.addWidget(self.menu)

        self.infoList = infoListView()
        self.ui.horizontalLayout_32.addWidget(self.infoList)

        self.NyquistPageHistory = NyquistPlotHistory()
        self.ui.verticalLayout_8.addWidget(self.NyquistPageHistory)
        # Setup buttons and signal connections
        self.ui.pushButton.clicked.connect(lambda: self.switchPage(0))
        self.ui.pushButton.clicked.connect(lambda: self.NyquistPageHistory.clear_all_plots())
        self.ui.pushButton_3.clicked.connect(self.start_loop)
        self.ui.pushButton_4.clicked.connect(self.stop_loop)
        self.ui.pushButton_4.setEnabled(False)

        # Delay reader initialization until identifiers are set
        self.reader = None
        self.container_number = None
        self.cluster_number = None
        self.pack_number = None

        # Load configuration and initialize I2C reader
        with open("config.json", "r") as config_file:
            self.config = json.load(config_file)

        # Initialize battery cell display
        self.init_batterycell()

        self.init_Nyquist()

        self.init_heatmap()

    def init_heatmap(self):
        # Define the STL file path and save path for the heatmap
        stl_file = "3d_pack_model/1x13_battery_pack_model.STL"
        save_path = "3d_pack_model/heatmap_render.png"

        # Create and render the heatmap directly in the layout
        from tools.heatmap_plt import HeatMap3DWidget
        heatmap = HeatMap3DWidget(stl_file, num_cells=13)
        heatmap.create_responsive_label(save_path, self.ui.horizontalLayout_15)

    def init_batterycell(self):
        self.ui.batteryList = []
        for row in range(2):
            for col in range(7):
                label = ImageClickedLabel()
                self.ui.batteryList.append(label)
                self.ui.gridLayout.addWidget(label, row, col)
        
        for i in range(14):
            self.ui.batteryList[i].clicked.connect(lambda: self.switchPage(1))
            self.ui.batteryList[i].clicked.connect(lambda i=i: self.update_NyquistHistory(i+1))
            
    def update_battertcell(self,battery_number, real_imp, voltage):
        self.ui.batteryList[battery_number-1].update_text(voltage, real_imp)

    def switchPage(self, index):
        print(f"Switching to page {index}")
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def start_loop(self):
        # Ensure identifiers are set before reading starts
        self.settingId = initSetting()
        self.settingId.identifier.connect(self.identifier_setting)
        self.settingId.exec()

        # Check if identifiers are set
        if not all([self.container_number, self.cluster_number, self.pack_number]):
            print("Error: Please set container, cluster, and pack identifiers before starting.")
            self.ui.pushButton_3.setEnabled(True)
            return
        
        bus_number = self.config.get("bus_number", 1)
        address_list = [int(address, 16) for address in self.config.get("address_list", [])]

        # Initialize I2C Reader with identifiers and configuration
        self.reader = I2CReader(bus_number=bus_number)
        self.reader.set_user_selection(self.container_number, self.cluster_number, self.pack_number)

        self.reader.new_data_received_SWF.connect(self.update_Nyquist)
        self.reader.new_data_received_finish_list.connect(self.update_infoList)
        self.reader.new_data_received_batterycellInfo.connect(self.update_battertcell)
        
        # Start I2C reading
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.reader.start_reading(address_list)

    def stop_loop(self):
        if self.reader:
            self.reader.close()
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(False)

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
      
    def identifier_setting(self, container_number, cluster_number, pack_number):
        # Set identifiers and update display
        self.container_number = container_number
        self.cluster_number = cluster_number
        self.pack_number = pack_number
        self.ui.label_14.setText(f"Container {container_number} - Cluster {cluster_number} - Pack {pack_number}")
        print(f"Identifiers set: Container {container_number}, Cluster {cluster_number}, Pack {pack_number}")
    
    def init_Nyquist(self):
        self.NyquistPage = NyquistPlot()  
        self.ui.horizontalLayout_33.addWidget(self.NyquistPage)
        
    def update_Nyquist(self, battery_number, freq, real_impedance, negative_imaginary_impedance):
        self.NyquistPage.add_data(battery_number, real_impedance, negative_imaginary_impedance)
    
    def update_NyquistHistory(self, cell_id):
        data =  self.repo.get_cell_history(cell_id,index=10)
        result = defaultdict(lambda: ([], []))  
        for real_time_id, measurements in data.items():
            for measurement in measurements:
                result[real_time_id][0].append(measurement.real_impedance)  
                result[real_time_id][1].append(measurement.imag_impedance) 
        for real_time_id, data in result.items():
            self.NyquistPageHistory.add_data(real_time_id,data[0],data[1])

    def update_infoList(self,lists):
        data = []
        for cell_id in lists:
            data.append(self.repo.get_cell_measurements(cell_id))
        print(data)
        result = defaultdict(lambda: ([], []))  
        for measurements in data:
            for measurement in measurements:
                cell_id = f"Battery{measurement.cell_id}"  
                result[cell_id][0].append(measurement.real_impedance)  
                result[cell_id][1].append(measurement.imag_impedance)  
        result = dict(result)
        analyzer = EISAnalyzer(result)
        discrepancy = analyzer.calculate_dispersion(result)
        print(f"Discrepancy: {discrepancy}")
        consistency = analyzer.calculate_consistency(result)
        print(f"Consistency: {consistency}")
        outliers_method2 = analyzer.detect_outliers_method2()
        print(f"Outliers (Method 2): {outliers_method2}")
        self.infoList.populate_data(discrepancy,consistency,outliers_method2)
        



if __name__ == "__main__":
  
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

