# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1049, 645)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(800, 480))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.centralwidget)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMaximumSize(QSize(16777215, 40))
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_toodle = QFrame(self.frame_top)
        self.frame_toodle.setObjectName(u"frame_toodle")
        self.frame_toodle.setMinimumSize(QSize(50, 40))
        self.frame_toodle.setMaximumSize(QSize(50, 40))
        self.frame_toodle.setStyleSheet(u"background:rgb(0,143,150);")
        self.frame_toodle.setFrameShape(QFrame.NoFrame)
        self.frame_toodle.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_toodle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toodle = QPushButton(self.frame_toodle)
        self.toodle.setObjectName(u"toodle")
        self.toodle.setMinimumSize(QSize(50, 40))
        self.toodle.setMaximumSize(QSize(50, 40))
        self.toodle.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,178,178);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon = QIcon()
        icon.addFile(u"icons/1x/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toodle.setIcon(icon)
        self.toodle.setFlat(True)

        self.horizontalLayout_3.addWidget(self.toodle)


        self.horizontalLayout.addWidget(self.frame_toodle)

        self.frame_top_east = QFrame(self.frame_top)
        self.frame_top_east.setObjectName(u"frame_top_east")
        self.frame_top_east.setMaximumSize(QSize(16777215, 55))
        self.frame_top_east.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_top_east.setFrameShape(QFrame.NoFrame)
        self.frame_top_east.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_east)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_appname = QFrame(self.frame_top_east)
        self.frame_appname.setObjectName(u"frame_appname")
        self.frame_appname.setFrameShape(QFrame.NoFrame)
        self.frame_appname.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_appname)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lab_appname = QLabel(self.frame_appname)
        self.lab_appname.setObjectName(u"lab_appname")
        font = QFont()
        font.setFamilies([u"Segoe UI Light"])
        font.setPointSize(24)
        self.lab_appname.setFont(font)
        self.lab_appname.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_appname.setTextFormat(Qt.AutoText)
        self.lab_appname.setScaledContents(False)

        self.horizontalLayout_10.addWidget(self.lab_appname)

        self.label_11 = QLabel(self.frame_appname)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(80, 40))
        self.label_11.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_10.addWidget(self.label_11)


        self.horizontalLayout_4.addWidget(self.frame_appname)

        self.frame_min = QFrame(self.frame_top_east)
        self.frame_min.setObjectName(u"frame_min")
        self.frame_min.setMinimumSize(QSize(40, 40))
        self.frame_min.setMaximumSize(QSize(40, 40))
        self.frame_min.setFrameShape(QFrame.NoFrame)
        self.frame_min.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_min)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bn_min = QPushButton(self.frame_min)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMinimumSize(QSize(40, 40))
        self.bn_min.setMaximumSize(QSize(40, 40))
        self.bn_min.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"icons/1x/hideAsset 53.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon1)
        self.bn_min.setIconSize(QSize(22, 22))
        self.bn_min.setFlat(True)

        self.horizontalLayout_7.addWidget(self.bn_min)


        self.horizontalLayout_4.addWidget(self.frame_min)

        self.frame_max = QFrame(self.frame_top_east)
        self.frame_max.setObjectName(u"frame_max")
        self.frame_max.setMinimumSize(QSize(40, 40))
        self.frame_max.setMaximumSize(QSize(40, 40))
        self.frame_max.setFrameShape(QFrame.NoFrame)
        self.frame_max.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_max)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.bn_max = QPushButton(self.frame_max)
        self.bn_max.setObjectName(u"bn_max")
        self.bn_max.setMaximumSize(QSize(40, 40))
        self.bn_max.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"icons/1x/max.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_max.setIcon(icon2)
        self.bn_max.setIconSize(QSize(22, 22))
        self.bn_max.setFlat(True)

        self.horizontalLayout_6.addWidget(self.bn_max)


        self.horizontalLayout_4.addWidget(self.frame_max)

        self.frame_close = QFrame(self.frame_top_east)
        self.frame_close.setObjectName(u"frame_close")
        self.frame_close.setMinimumSize(QSize(40, 40))
        self.frame_close.setMaximumSize(QSize(40, 55))
        self.frame_close.setFrameShape(QFrame.NoFrame)
        self.frame_close.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bn_close = QPushButton(self.frame_close)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMaximumSize(QSize(40, 40))
        self.bn_close.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"icons/1x/closeAsset 43.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon3)
        self.bn_close.setIconSize(QSize(22, 22))
        self.bn_close.setFlat(True)

        self.horizontalLayout_5.addWidget(self.bn_close)


        self.horizontalLayout_4.addWidget(self.frame_close)


        self.horizontalLayout.addWidget(self.frame_top_east)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_bottom = QFrame(self.centralwidget)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_bottom_east = QFrame(self.frame_bottom)
        self.frame_bottom_east.setObjectName(u"frame_bottom_east")
        self.frame_bottom_east.setFrameShape(QFrame.NoFrame)
        self.frame_bottom_east.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame_bottom_east)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_menu = QFrame(self.frame_bottom_east)
        self.frame_menu.setObjectName(u"frame_menu")
        sizePolicy.setHeightForWidth(self.frame_menu.sizePolicy().hasHeightForWidth())
        self.frame_menu.setSizePolicy(sizePolicy)
        self.frame_menu.setMinimumSize(QSize(0, 30))
        self.frame_menu.setMaximumSize(QSize(16777215, 20))
        self.frame_menu.setFrameShape(QFrame.StyledPanel)
        self.frame_menu.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_menu)
        self.horizontalLayout_38.setSpacing(5)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_menu)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_38.addWidget(self.frame_14)


        self.verticalLayout_2.addWidget(self.frame_menu)

        self.frame = QFrame(self.frame_bottom_east)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_14 = QHBoxLayout(self.frame)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 55))
        self.stackedWidget.setStyleSheet(u"")
        self.page_top = QWidget()
        self.page_top.setObjectName(u"page_top")
        self.page_top.setStyleSheet(u"background:rgb(91,90,90);")
        self.horizontalLayout_19 = QHBoxLayout(self.page_top)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 5, 0, 5)
        self.vert_divide = QFrame(self.page_top)
        self.vert_divide.setObjectName(u"vert_divide")
        self.vert_divide.setFrameShape(QFrame.VLine)
        self.vert_divide.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_19.addWidget(self.vert_divide)

        self.frame_home_main = QFrame(self.page_top)
        self.frame_home_main.setObjectName(u"frame_home_main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(6)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_home_main.sizePolicy().hasHeightForWidth())
        self.frame_home_main.setSizePolicy(sizePolicy1)
        self.frame_home_main.setMaximumSize(QSize(16777215, 16777215))
        self.frame_home_main.setFrameShape(QFrame.NoFrame)
        self.frame_home_main.setFrameShadow(QFrame.Plain)
        self.verticalLayout_5 = QVBoxLayout(self.frame_home_main)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.frame_4 = QFrame(self.frame_home_main)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setMinimumSize(QSize(618, 0))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.frame_home_main)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(2)
        sizePolicy3.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy3)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")

        self.verticalLayout_5.addWidget(self.frame_3)


        self.horizontalLayout_19.addWidget(self.frame_home_main)

        self.frame_home_stat = QFrame(self.page_top)
        self.frame_home_stat.setObjectName(u"frame_home_stat")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(4)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_home_stat.sizePolicy().hasHeightForWidth())
        self.frame_home_stat.setSizePolicy(sizePolicy4)
        self.frame_home_stat.setMinimumSize(QSize(0, 0))
        self.frame_home_stat.setMaximumSize(QSize(16777215, 16777215))
        self.frame_home_stat.setFrameShape(QFrame.NoFrame)
        self.frame_home_stat.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_home_stat)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.frame_7 = QFrame(self.frame_home_stat)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(8)
        sizePolicy5.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy5)
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_33.setSpacing(5)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_6.addWidget(self.frame_7)

        self.frame_12 = QFrame(self.frame_home_stat)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy3.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy3)
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_32.setSpacing(5)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_6.addWidget(self.frame_12)

        self.textEdit = QTextEdit(self.frame_home_stat)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(4)
        sizePolicy6.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy6)

        self.verticalLayout_6.addWidget(self.textEdit)

        self.frame_13 = QFrame(self.frame_home_stat)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy7)
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_37.setSpacing(5)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.frame_13)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(5)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy8)

        self.horizontalLayout_37.addWidget(self.lineEdit)

        self.pushButton_6 = QPushButton(self.frame_13)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy9)
        self.pushButton_6.setMaximumSize(QSize(60, 16777215))
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")
        self.pushButton_6.setIconSize(QSize(20, 25))

        self.horizontalLayout_37.addWidget(self.pushButton_6)


        self.verticalLayout_6.addWidget(self.frame_13)


        self.horizontalLayout_19.addWidget(self.frame_home_stat)

        self.stackedWidget.addWidget(self.page_top)
        self.page_sub = QWidget()
        self.page_sub.setObjectName(u"page_sub")
        self.page_sub.setStyleSheet(u"background:rgb(91,90,90);")
        self.horizontalLayout_16 = QHBoxLayout(self.page_sub)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_left = QFrame(self.page_sub)
        self.frame_left.setObjectName(u"frame_left")
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_left)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_left)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(6)
        sizePolicy10.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy10)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_5 = QFrame(self.frame_left)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")

        self.verticalLayout_3.addWidget(self.frame_5)


        self.horizontalLayout_16.addWidget(self.frame_left)

        self.frame_right = QFrame(self.page_sub)
        self.frame_right.setObjectName(u"frame_right")
        self.frame_right.setFrameShape(QFrame.StyledPanel)
        self.frame_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_right)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy10.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy10)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_6)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.frame_6)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy7.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy7)
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_15)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_17.addWidget(self.frame_8)

        self.pushButton = QPushButton(self.frame_15)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QSize(60, 16777215))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.horizontalLayout_17.addWidget(self.pushButton)


        self.verticalLayout_7.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.frame_6)
        self.frame_16.setObjectName(u"frame_16")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(15)
        sizePolicy11.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy11)
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_16)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")

        self.verticalLayout_7.addWidget(self.frame_16)


        self.verticalLayout_4.addWidget(self.frame_6)

        self.frame_9 = QFrame(self.frame_right)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy2.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy2)
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.textEdit_2 = QTextEdit(self.frame_9)
        self.textEdit_2.setObjectName(u"textEdit_2")
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_20.addWidget(self.textEdit_2)


        self.verticalLayout_4.addWidget(self.frame_9)


        self.horizontalLayout_16.addWidget(self.frame_right)

        self.stackedWidget.addWidget(self.page_sub)

        self.horizontalLayout_14.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_low = QFrame(self.frame_bottom_east)
        self.frame_low.setObjectName(u"frame_low")
        self.frame_low.setEnabled(True)
        sizePolicy.setHeightForWidth(self.frame_low.sizePolicy().hasHeightForWidth())
        self.frame_low.setSizePolicy(sizePolicy)
        self.frame_low.setMinimumSize(QSize(0, 30))
        self.frame_low.setMaximumSize(QSize(16777215, 30))
        self.frame_low.setStyleSheet(u"")
        self.frame_low.setFrameShape(QFrame.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_low)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.frame_low)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(3)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy12)
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 1, -1, 1)
        self.label_14 = QLabel(self.frame_11)
        self.label_14.setObjectName(u"label_14")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(1)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy13)
        self.label_14.setStyleSheet(u"QLabel {\n"
"    color: white;        \n"
"    font: 16pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"}")
        self.label_14.setTextFormat(Qt.AutoText)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_14)


        self.horizontalLayout_11.addWidget(self.frame_11)

        self.frame_10 = QFrame(self.frame_low)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(2)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy14)
        self.frame_10.setMaximumSize(QSize(16777215, 300))
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 1, -1, 1)
        self.comboBox_4 = QComboBox(self.frame_10)
        self.comboBox_4.setObjectName(u"comboBox_4")
        sizePolicy13.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy13)
        self.comboBox_4.setStyleSheet(u"QComboBox {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"	border: 2px solid rgb(0,143,170);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(0,143,170);\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"	background: rgb(51,51,51);\n"
"}\n"
"\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background:rgb(51,51,51);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 5px; /* same radius as the QComboBox"
                        " */\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(icons/1x/arrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    background:rgb(51,51,51);\n"
"}\n"
"\n"
"")
        self.comboBox_4.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)

        self.horizontalLayout_12.addWidget(self.comboBox_4)

        self.pushButton_3 = QPushButton(self.frame_10)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy13.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy13)
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.horizontalLayout_12.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_10)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy13.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy13)
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.horizontalLayout_12.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.frame_10)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy13.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy13)
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"	font: 10pt \"Adobe \u9ed1\u4f53 Std R\";\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.horizontalLayout_12.addWidget(self.pushButton_5)


        self.horizontalLayout_11.addWidget(self.frame_10)


        self.verticalLayout_2.addWidget(self.frame_low)


        self.horizontalLayout_2.addWidget(self.frame_bottom_east)


        self.verticalLayout.addWidget(self.frame_bottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toodle.setText("")
        self.lab_appname.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">\u9502\u7535\u6c60\u591a\u7ef4\u6570\u636e\u611f\u77e5\u4e0eAI\u8f85\u52a9\u7ba1\u7406\u7cfb\u7edf</span></p></body></html>", None))
        self.label_11.setText("")
#if QT_CONFIG(tooltip)
        self.bn_min.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.bn_min.setText("")
#if QT_CONFIG(tooltip)
        self.bn_max.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.bn_max.setText("")
#if QT_CONFIG(tooltip)
        self.bn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.bn_close.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.label_14.setText("")
        self.comboBox_4.setCurrentText("")
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0", None))
    # retranslateUi

