# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_initSetting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_initSetting(object):
    def setupUi(self, initSetting):
        if not initSetting.objectName():
            initSetting.setObjectName(u"initSetting")
        initSetting.resize(600, 400)
        initSetting.setMinimumSize(QSize(450, 235))
        initSetting.setMaximumSize(QSize(600, 450))
        initSetting.setStyleSheet(u"QDialog {\n"
"	background:rgb(51,51,51);\n"
"}")
        self.verticalLayout = QVBoxLayout(initSetting)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(initSetting)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.frame_top = QFrame(self.frame_2)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 55))
        self.frame_top.setMaximumSize(QSize(16777215, 55))
        self.frame_top.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lab_heading = QLabel(self.frame_top)
        self.lab_heading.setObjectName(u"lab_heading")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(14)
        self.lab_heading.setFont(font)
        self.lab_heading.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_heading.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lab_heading)


        self.verticalLayout_2.addWidget(self.frame_top)

        self.frame_bottom = QFrame(self.frame_2)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_bottom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_2 = QComboBox(self.frame_bottom)
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QSize(100, 40))
        self.comboBox_2.setStyleSheet(u"QComboBox {\n"
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

        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)

        self.comboBox = QComboBox(self.frame_bottom)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QSize(100, 40))
        self.comboBox.setStyleSheet(u"QComboBox {\n"
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

        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)

        self.label_16 = QLabel(self.frame_bottom)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QSize(100, 40))
        self.label_16.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_15 = QLabel(self.frame_bottom)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(100, 40))
        self.label_15.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_15, 1, 0, 1, 1)

        self.label = QLabel(self.frame_bottom)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(100, 40))
        self.label.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.frame_bottom)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(100, 40))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
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

        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)

        self.comboBox_3 = QComboBox(self.frame_bottom)
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setMinimumSize(QSize(100, 40))
        self.comboBox_3.setStyleSheet(u"QComboBox {\n"
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

        self.gridLayout.addWidget(self.comboBox_3, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(initSetting)

        QMetaObject.connectSlotsByName(initSetting)
    # setupUi

    def retranslateUi(self, initSetting):
        initSetting.setWindowTitle(QCoreApplication.translate("initSetting", u"Dialog", None))
        self.lab_heading.setText(QCoreApplication.translate("initSetting", u"\u8bf7\u624b\u52a8\u8bbe\u7f6e\u5f53\u524d\u7535\u6c60\u5305\u7f16\u53f7", None))
        self.label_16.setText(QCoreApplication.translate("initSetting", u"\u96c6\u88c5\u7bb1\u7f16\u53f7", None))
        self.label_15.setText(QCoreApplication.translate("initSetting", u"\u7535\u6c60\u67dc\u7f16\u53f7", None))
        self.label.setText(QCoreApplication.translate("initSetting", u"\u7535\u6c60\u5305\u7f16\u53f7", None))
        self.pushButton_2.setText(QCoreApplication.translate("initSetting", u"\u5e94\u7528\u8bbe\u7f6e", None))
    # retranslateUi

