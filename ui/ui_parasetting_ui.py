# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_parasetting.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 400)
        Dialog.setMinimumSize(QSize(450, 235))
        Dialog.setMaximumSize(QSize(600, 450))
        Dialog.setStyleSheet(u"QDialog {\n"
"	background:rgb(51,51,51);\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(Dialog)
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

        self.bn_min = QPushButton(self.frame_top)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMinimumSize(QSize(55, 55))
        self.bn_min.setMaximumSize(QSize(55, 55))
        self.bn_min.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(51,51,51);\n"
"}")
        icon = QIcon()
        icon.addFile(u"icons/1x/hideAsset 53.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon)
        self.bn_min.setIconSize(QSize(22, 12))
        self.bn_min.setAutoDefault(False)
        self.bn_min.setFlat(True)

        self.horizontalLayout.addWidget(self.bn_min)

        self.bn_close = QPushButton(self.frame_top)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMinimumSize(QSize(55, 55))
        self.bn_close.setMaximumSize(QSize(55, 55))
        self.bn_close.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(51,51,51);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"icons/1x/closeAsset 43.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon1)
        self.bn_close.setIconSize(QSize(22, 22))
        self.bn_close.setAutoDefault(False)
        self.bn_close.setFlat(True)

        self.horizontalLayout.addWidget(self.bn_close)


        self.verticalLayout_2.addWidget(self.frame_top)

        self.frame_bottom = QFrame(self.frame_2)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_bottom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_16 = QLabel(self.frame_bottom)
        self.label_16.setObjectName(u"label_16")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QSize(0, 25))
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

        self.gridLayout.addWidget(self.label_16, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.frame_bottom)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QSize(75, 25))
        self.lineEdit.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_12 = QLabel(self.frame_bottom)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(0, 25))
        self.label_12.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)

        self.comboBox = QComboBox(self.frame_bottom)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMaximumSize(QSize(75, 16777215))
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
        self.comboBox.setEditable(False)

        self.gridLayout.addWidget(self.comboBox, 0, 3, 1, 1)

        self.label_15 = QLabel(self.frame_bottom)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(0, 25))
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

        self.gridLayout.addWidget(self.label_15, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.frame_bottom)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QSize(75, 25))
        self.lineEdit_2.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frame_bottom)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(0, 25))
        self.label_11.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_11, 1, 2, 1, 1)

        self.lineEdit_6 = QLineEdit(self.frame_bottom)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMaximumSize(QSize(75, 25))
        self.lineEdit_6.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_6, 1, 3, 1, 1)

        self.label_14 = QLabel(self.frame_bottom)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QSize(0, 25))
        self.label_14.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.frame_bottom)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMaximumSize(QSize(75, 25))
        self.lineEdit_3.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_10 = QLabel(self.frame_bottom)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(0, 25))
        self.label_10.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_10, 2, 2, 1, 1)

        self.lineEdit_7 = QLineEdit(self.frame_bottom)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setMaximumSize(QSize(75, 25))
        self.lineEdit_7.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_7, 2, 3, 1, 1)

        self.label_13 = QLabel(self.frame_bottom)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QSize(0, 25))
        self.label_13.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_13, 3, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.frame_bottom)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMaximumSize(QSize(75, 25))
        self.lineEdit_4.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)

        self.label_8 = QLabel(self.frame_bottom)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(0, 25))
        self.label_8.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)

        self.lineEdit_8 = QLineEdit(self.frame_bottom)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setMaximumSize(QSize(75, 25))
        self.lineEdit_8.setSizeIncrement(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_8, 3, 3, 1, 1)

        self.label_9 = QLabel(self.frame_bottom)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(0, 25))
        self.label_9.setStyleSheet(u"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QLabel {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	background-color: rgb(51,51,51);\n"
"}")

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.frame_bottom)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMaximumSize(QSize(75, 16777215))
        self.comboBox_2.setStyleSheet(u"QComboBox {\n"
"	font: 8pt \"Adobe \u9ed1\u4f53 Std R\";\n"
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
"    border-top-right-radius: 5px; /* same radius as the QComboBox "
                        "*/\n"
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

        self.gridLayout.addWidget(self.comboBox_2, 4, 1, 1, 1)

        self.bn_west = QPushButton(self.frame_bottom)
        self.bn_west.setObjectName(u"bn_west")
        self.bn_west.setMinimumSize(QSize(69, 25))
        self.bn_west.setMaximumSize(QSize(75, 25))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        self.bn_west.setFont(font1)
        self.bn_west.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.bn_west.setAutoDefault(False)

        self.gridLayout.addWidget(self.bn_west, 5, 2, 1, 1)

        self.bn_east = QPushButton(self.frame_bottom)
        self.bn_east.setObjectName(u"bn_east")
        self.bn_east.setMinimumSize(QSize(69, 25))
        self.bn_east.setMaximumSize(QSize(75, 25))
        self.bn_east.setFont(font1)
        self.bn_east.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.bn_east.setAutoDefault(False)

        self.gridLayout.addWidget(self.bn_east, 5, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lab_heading.setText(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.bn_min.setText("")
        self.bn_close.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"\u91c7\u6837\u70b9\u6570", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u91c7\u6837\u6a21\u5f0f", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"\u626b\u9891", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"\u5355\u9891", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u8d77\u59cb\u9891\u7387", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u7ec8\u6b62\u9891\u7387", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"\u5355\u9891\u9891\u7387", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u4ea4\u6d41\u5cf0\u503c\u7535\u538b", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u76f4\u6d41\u504f\u7f6e\u7535\u538b", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u6821\u51c6\u7535\u963b\u503c", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u91c7\u6837\u6570\u636e\u95f4\u9694", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Dialog", u"\u7ebf\u6027\u6bd4\u4f8b", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Dialog", u"\u6307\u6570\u6bd4\u4f8b", None))

        self.bn_west.setText(QCoreApplication.translate("Dialog", u"\u5e94\u7528", None))
        self.bn_east.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

