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
import numpy as np
from ui.ui_function import * # A FILE WHERE ALL THE FUNCTION LIKE BUTTON PRESSES, SILDER, PROGRESS BAR E.T.C ARE DONE.
from ui.ui_main import Ui_MainWindow # MAINWINDOW CODE GENERATED BY THE QT DESIGNER AND pyside2-uic.
from custom_widget.menuWidget import MenuWidget
from custom_widget.BatteryCellLabel import BatteryCellLabel
from custom_widget.PortCellLabel import PortCellLabel
from database.db_init import init_database
from custom_widget.initSetting import initSetting
from tools.I2C_Reader import I2CReader
from custom_widget.nyquist_plot import NyquistPlot
from tools.heatmap_plt import HeatMap3DWidget
from tools.single_battery_renderer import SingleBattery3DWidget
from custom_widget.infoListWidget import infoListView
from database.repository import Repository
from custom_widget.nyquist_plot_history import NyquistPlotHistory
from custom_widget.bode_plot_history import BodePlotHistory
from custom_widget.bode_plot import BodePlot
from custom_widget.PackAdviceTextEdit import PackAdviceTextEdit
from custom_widget.CellAdviceTextEdit import CellAdviceTextEdit
import json
from algorithm.start_algorithm import StartAlgorithm
# from tools.transmit_data import DataTransmitter
from PyQt6.QtCore import QTimer

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
        UIFunction.logoTitle(self)
        self.showFullScreen() 
        # Initialize menu and layout
        self.menu = MenuWidget(self)
        self.ui.horizontalLayout_38.addWidget(self.menu)

        self.infoList = infoListView()
        self.ui.horizontalLayout_32.addWidget(self.infoList)

        self.NyquistPageHistory = NyquistPlotHistory()
        self.ui.verticalLayout_8.addWidget(self.NyquistPageHistory)

        self.BodePageHistory = BodePlotHistory()  # 创建 BodePlotHistory 实例
        self.ui.horizontalLayout_8.addWidget(self.BodePageHistory)

        self.PackTextEdit = PackAdviceTextEdit()
        self.ui.horizontalLayout_18.addWidget(self.PackTextEdit)

        self.CellTextEdit = CellAdviceTextEdit()
        self.ui.horizontalLayout_20.addWidget(self.CellTextEdit)
        # Setup buttons and signal connections
        self.ui.pushButton_3.clicked.connect(self.start_loop)
        self.ui.pushButton_4.clicked.connect(self.stop_loop)
        self.ui.pushButton_4.setEnabled(False)

        # Delay reader initialization until identifiers are set
        self.reader = None
        self.container_number = None
        self.cluster_number = None
        self.pack_number = None

        # # 创建 DataTransmitter 实例
        # self.data_transmitter = DataTransmitter()

        # # 创建定时器，每5分钟调用一次上传功能
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.data_transmitter.upload_data)  # 直接调用 upload_data 方法
        # self.timer.start(5 * 60 * 1000)  # 每五分钟（300,000毫秒）触发一次

        # Load configuration and initialize I2C reader
        with open("config.json", "r") as config_file:
            self.config = json.load(config_file)

        # Initialize battery cell display
        self.init_batterycell()
        self.init_Nyquist()
        self.init_heatmap()


    def init_heatmap(self):
        """
        Initialize the heatmap widget, render it, and add it to the layout.
        """
        stl_file = "3d_pack_model/1x13_battery_pack_model.STL"
        self.heatmap_widget = HeatMap3DWidget(stl_file, num_cells=13, parent=self)
        self.ui.horizontalLayout_15.addWidget(self.heatmap_widget)

    def update_heatmap(self):
        if hasattr(self, "heatmap_widget"):
            self.heatmap_widget.update_heatmap()
            
        self.repaint()


    def init_single_battery_renderer(self):
        # Define the STL file path and save path for the single battery render
        stl_file = "3d_battery_model/single_battery_model.STL"
        save_path = "3d_battery_model/single_battery_render.png"

        # Create and render the single battery directly in the layout
        from tools.single_battery_renderer import SingleBattery3DWidget
        single_battery = SingleBattery3DWidget(stl_file)
        single_battery.create_responsive_label(save_path, self.ui.horizontalLayout_9)

    def init_batterycell(self):
        self.ui.batteryList = []
        for row in range(2):
            col_count = 7 if row == 0 else 6  
            for col in range(col_count):
                label = BatteryCellLabel()
                self.ui.batteryList.append(label)
                self.ui.gridLayout.addWidget(label, row, col)

        for i in range(13):
            self.ui.batteryList[i].clicked.connect(lambda i=i: self.switchPage(1, i + (self.port_number-1)*13))
            self.ui.batteryList[i].clicked.connect(lambda i=i: self.update_NyquistHistory(i + (self.port_number-1)*13))
            self.ui.batteryList[i].clicked.connect(lambda i=i: self.update_BodeHistory(i + (self.port_number-1)*13))
            self.ui.batteryList[i].clicked.connect(lambda i=i: self.update_textEdit_celladvice(i + (self.port_number-1)*13))
        
        self.ui.port_cell = PortCellLabel()
        self.ui.gridLayout.addWidget(self.ui.port_cell, 1, 6)
            
    def update_battertcell(self,battery_number, cell_id, real_imp):
        self.ui.batteryList[battery_number].update_text(cell_id, real_imp)


    def switchPage(self, index, displayed_battery_id=None):
        print(f"Switching to page {index}, Displayed Battery ID: {displayed_battery_id}")
        self.ui.stackedWidget.setCurrentIndex(index)
        # If moving to page 2 (battery details page), update the corresponding battery info
        if index == 1 and displayed_battery_id is not None:
            self.update_battery_details(displayed_battery_id)


    def update_battery_details(self, displayed_battery_id):
        """
        Update the detailed battery page with new data and render the 3D image.
        """
        print(f"Updating details for battery {displayed_battery_id}")

        # 固定使用同一个 STL 文件，而非根据电池ID动态生成
        stl_file = "3d_battery_model/single_battery_model.STL"
        if not os.path.exists(stl_file):
            print(f"STL 文件不存在: {stl_file}")
            return

        # 清除布局中已有的 widgets
        self.clear_existing_widgets_in_layout(self.ui.horizontalLayout_9)

        # 创建 SingleBattery3DWidget 实例，传递正确的参数
        single_battery_renderer = SingleBattery3DWidget(
            stl_file=stl_file,
            battery_id=displayed_battery_id,  # battery_id 仍可传递，用于渲染温度或其他逻辑
            parent=self
        )

        # 将 SingleBattery3DWidget 添加到布局中
        self.ui.horizontalLayout_9.addWidget(single_battery_renderer)

        # 保存引用，以便后续更新温度
        self.single_battery_renderer = single_battery_renderer

        # 更新其他 UI 组件（如 Nyquist 历史记录）
        self.update_NyquistHistory(displayed_battery_id)



        
    def clear_existing_widgets_in_layout(self, layout):
        """Utility method to clear all widgets from a given layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def start_loop(self):
        # Ensure identifiers are set before reading starts
        self.settingId = initSetting()
        self.settingId.identifier.connect(self.identifier_setting)
        self.settingId.exec()
        
        self.clear_all()
        
        # Check if identifiers are set
        if not all([self.container_number, self.cluster_number, self.pack_number]):
            print("Error: Please set container, cluster, and pack identifiers before starting.")
            self.ui.pushButton_3.setEnabled(True)
            return
        
        bus_number = self.config.get("bus_number", 1)
        address_list = [int(address, 16) for address in self.config.get("address_list", [])]

        # Initialize I2C Reader with identifiers and configuration
        self.reader = I2CReader(bus_number=bus_number)
        self.reader.get_port(self.port_number)
        self.reader.set_user_selection(self.container_number, self.cluster_number, self.pack_number)

        self.reader.new_data_received_SWF.connect(self.update_Nyquist)
        self.reader.new_data_received_finish_list.connect(self.start_algorithm)
        self.reader.new_data_received_batterycellInfo.connect(self.update_battertcell)
        self.reader.new_data_received_check.connect(self.update_textEdit)

        self.algo = StartAlgorithm()
        self.algo.task_done.connect(self.update_textEdit_packadvice)
        self.algo.task_done.connect(self.update_infoList)
        self.algo.task_done.connect(self.stop_loop)
        self.algo.task_done.connect(self.update_3dheatmap)
        # Start I2C reading
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.reader.start_reading(address_list)

    def stop_loop(self):
        if self.reader:
            self.reader.close()
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(False)

    def clear_all(self):
        self.NyquistPage.clear_all_plots()
        self.infoList.clear_all()
        self.PackTextEdit.clear_all()
        self.ui.textEdit.clear()
        for batterty in self.ui.batteryList:
            batterty.clear_all()
        self.heatmap_widget.clear_existing_widgets()

    def start_algorithm(self,lists):
        self.algo.start(lists)
        

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
      
    def identifier_setting(self, container_number, cluster_number, pack_number,port_number):
        # Set identifiers and update display
        self.container_number = container_number
        self.cluster_number = cluster_number
        self.pack_number = pack_number
        self.port_number = port_number
        self.ui.label_14.setText(f"电池柜 {cluster_number} - 电池包 {pack_number} - 端口号 {port_number}")
        self.ui.port_cell.update_text(port_number)
    
    def init_Nyquist(self):
        self.NyquistPage = NyquistPlot()  
        self.ui.horizontalLayout_33.addWidget(self.NyquistPage)
        
    def update_Nyquist(self, battery_number, freq, real_impedance, negative_imaginary_impedance):
        self.NyquistPage.add_data(battery_number, real_impedance, negative_imaginary_impedance)
    
    def update_NyquistHistory(self, cell_id):
        self.NyquistPageHistory.update_data(cell_id)

    def update_Bode(self, battery_number, freq, real_impedance, negative_imaginary_impedance):
        # 调用 Bode 图实例并添加数据
        self.BodePage.add_data(battery_number, freq, real_impedance, negative_imaginary_impedance)

    def update_BodeHistory(self, cell_id):
        self.BodePageHistory.update_data(cell_id)

    def update_infoList(self,lists):
        self.infoList.update_data(lists)

    def update_textEdit(self,line):
        font = QFont('Arial', 12)  
        self.ui.textEdit.setFont(font)
        self.ui.textEdit.setStyleSheet("color: white")
        self.ui.textEdit.append(line)

    def update_textEdit_packadvice(self,list):
        self.PackTextEdit.update_textedit(list)
    
    def update_textEdit_celladvice(self,cell_id):
        self.CellTextEdit.update_textedit(cell_id)

    def update_subtextEdit(self,line):
        self.ui.textEdit_2.append(line) 
    
    def update_3dheatmap(self):
        self.heatmap_widget.update_temperature_from_db()
    
    # def update_temperature(self,temperature):
    #     self.temperature = temperature
    #     print(f"received tem:{self.temperature}")


    #     if hasattr(self, "single_battery_renderer"):
    #         self.single_battery_renderer.set_temperature(self.temperature)

if __name__ == "__main__":
  
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

