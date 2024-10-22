from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenuBar, QMessageBox
from PyQt6.QtGui import QAction, QFont
from paraSetting import paraSetting
class MenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个垂直布局
        layout = QVBoxLayout(self)

        # 创建一个菜单栏
        menu_bar = QMenuBar(self)

        # 设置菜单栏的字体
        menu_font = QFont("Arial", 12)  # 字体和大小
        menu_bar.setFont(menu_font)

        # 使用样式表改变菜单栏的背景颜色
        
        # menu_bar.setStyleSheet("QMenuBar { background-color: #A9A9A9; }")  # 灰色背景


        # 添加"文件"菜单
        file_menu = menu_bar.addMenu('文件')

        # 创建"退出"操作并添加到"文件"菜单
        exit_action = QAction('退出', self)
        exit_action.setFont(menu_font)  # 设置操作的字体
        exit_action.triggered.connect(self.close)  # 当点击"退出"时关闭窗口
        file_menu.addAction(exit_action)

        # 添加"设置"菜单
        setting_menu = menu_bar.addMenu('设置')
        setting_menu.setFont(menu_font)  # 设置菜单字体

        # 创建"参数设置"操作并添加到"设置"菜单
        para_action = QAction('参数设置', self)
        para_action.setFont(menu_font)  # 设置操作的字体
        para_action.triggered.connect(self.para_setting)
        setting_menu.addAction(para_action)
        self.settingWidget = paraSetting()
        # 添加"帮助"菜单
        help_menu = menu_bar.addMenu('帮助')
        help_menu.setFont(menu_font)  # 设置菜单字体

        # 创建"关于"操作并添加到"帮助"菜单
        about_action = QAction('关于', self)
        about_action.setFont(menu_font)  # 设置操作的字体
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # 将菜单栏添加到布局中
        layout.setMenuBar(menu_bar)

        # 设置主窗口布局
        self.setLayout(layout)
    def get_reader(self, reader):
        self.reader = reader
        self.settingWidget.get_reader(self.reader)

    def show_about(self):
        # 显示关于信息
        QMessageBox.about(self, '关于', '这是一个关于对话框')

    def para_setting(self):
        # 显示参数设置信息
        self.settingWidget.exec()

if __name__ == '__main__':
    app = QApplication([])
    window = MenuWidget()
    window.show()
    app.exec()
