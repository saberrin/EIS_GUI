from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenuBar, QMessageBox
from PyQt6.QtGui import QAction, QFont
from custom_widget.paraSetting import paraSetting
from PyQt6.QtWidgets import QFileDialog
import shutil
from database.config import DB_PATH
from database.repository import Repository
class MenuWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.main_window = parent  
        # 创建一个垂直布局
        layout = QVBoxLayout(self)

        # 创建一个菜单栏
        menu_bar = QMenuBar(self)

        # 设置菜单栏的字体
        menu_font = QFont("Arial", 20)  # 字体和大小
        menu_bar.setFont(menu_font)

        # 使用样式表改变菜单栏的背景颜色
        
        menu_bar.setStyleSheet("""
            QMenuBar { color: white; }
            QMenu { min-width: 200px; 
                    color: white;}
            QMenu::item { padding: 10px; }  
        """)




        # # 添加"文件"菜单
        # file_menu = menu_bar.addMenu('文件')

        # # 创建"退出"操作并添加到"文件"菜单
        # exit_action = QAction('退出', self)
        # exit_action.setFont(menu_font)  # 设置操作的字体
        # exit_action.triggered.connect(self.close)  # 当点击"退出"时关闭窗口
        # file_menu.addAction(exit_action)

        # 添加"设置"菜单
        setting_menu = menu_bar.addMenu(' 设置 ')
        setting_menu.setFont(menu_font)  # 设置菜单字体

        # 创建"参数设置"操作并添加到"设置"菜单
        para_action = QAction('参数设置', self)
        para_action.setFont(menu_font)  # 设置操作的字体
        para_action.triggered.connect(self.para_setting)
        setting_menu.addAction(para_action)
        self.settingWidget = paraSetting()

        # 添加"设置"菜单
        data_menu = menu_bar.addMenu(' 数据管理 ')
        data_menu.setFont(menu_font)  # 设置菜单字体

        # 创建"参数设置"操作并添加到"设置"菜单
        para_action = QAction('数据导出', self)
        para_action.setFont(menu_font)  # 设置操作的字体
        para_action.triggered.connect(self.data_export)
        data_menu.addAction(para_action)

        # 创建"参数设置"操作并添加到"设置"菜单
        para_action = QAction('数据删除', self)
        para_action.setFont(menu_font)  # 设置操作的字体
        para_action.triggered.connect(self.data_delete)
        data_menu.addAction(para_action)
        
        # 添加"帮助"菜单
        help_menu = menu_bar.addMenu(' 帮助 ')
        help_menu.setFont(menu_font)  # 设置菜单字体

        # 创建"关于"操作并添加到"帮助"菜单
        about_action = QAction('关于', self)
        about_action.setFont(menu_font)  # 设置操作的字体
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        file_menu = menu_bar.addMenu(' 退出 ')

        # 创建"退出"操作并添加到"文件"菜单
        exit_action = QAction('回到主界面', self)
        exit_action.setFont(menu_font)  # 设置操作的字体
        exit_action.triggered.connect(self.update_main_window_ui)  # 当点击"退出"时关闭窗口
        file_menu.addAction(exit_action)

        # 将菜单栏添加到布局中
        layout.setMenuBar(menu_bar)

        # 设置主窗口布局
        self.setLayout(layout)

    def show_about(self):
        # 显示关于信息
        QMessageBox.about(self, '关于', '这是一个关于对话框')

    def para_setting(self):
        # 显示参数设置信息
        # self.showFullScreen()
        self.settingWidget.exec()

    def update_main_window_ui(self):
        self.main_window.switchPage(0)
        self.main_window.NyquistPageHistory.clear_all_plots()
        self.main_window.BodePageHistory.clear_all_plots()
    
    def data_export(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择保存路径", "", "SQLite Database (*.db)")
        if file_path:
            if not file_path.lower().endswith('.db'):
                file_path += '.db'
            try:
                shutil.copy(DB_PATH, file_path)
                QMessageBox.information(self, "导出成功", "数据库已成功导出到 " + file_path)
            except Exception as e:
                QMessageBox.warning(self, "导出失败", f"导出数据库失败: {str(e)}")

    def data_delete(self):
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            "你确认要删除所有数据吗？", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
    
        if reply == QMessageBox.StandardButton.Yes:
            repo = Repository()
            repo.delete_all_data()
            QMessageBox.information(self, "删除成功", "所有数据已成功删除")

if __name__ == '__main__':
    app = QApplication([])
    window = MenuWidget()
    window.show()
    app.exec()
