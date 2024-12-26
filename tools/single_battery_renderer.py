import os
import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy
import sqlite3

class SingleBattery3DWidget(QWidget):
    def __init__(self, stl_file, battery_id=None, database_path=None, parent=None):
        super().__init__(parent)
        self.stl_file = stl_file
        self.battery_id = battery_id
        self.database_path = database_path

        # 初始化温度值，默认值为10°C
        self.temperature = 10

        # 创建内部布局和 QLabel 用于显示渲染图像
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)

        # 设置渲染目录
        self.save_dir = "3d_battery_model"
        os.makedirs(self.save_dir, exist_ok=True)

        # 设置定时器用于延迟渲染，避免在快速调整大小时频繁渲染
        self.render_timer = QTimer(self)
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self.update_render)

    def fetch_latest_temperature(self):
        """从数据库中获取最新的 temperature 数据。"""
        if not self.database_path:
            return self.temperature  # 如果没有数据库路径，则返回默认温度

        default_temperature = 10  # 默认温度值
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 根据 cell_id 获取最新的 temperature 值
            query = """
                SELECT temperature
                FROM generated_info
                WHERE cell_id = ? AND real_time_id = (
                    SELECT MAX(real_time_id)
                    FROM generated_info
                    WHERE cell_id = ?
                )
            """
            cursor.execute(query, (self.battery_id , self.battery_id ))
            result = cursor.fetchone()

            if result and result[0] is not None:
                return result[0]
            else:
                return default_temperature
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            return default_temperature
        finally:
            if conn:
                conn.close()

    def showEvent(self, event):
        super().showEvent(event)
        # 控件显示后延迟渲染，确保 QLabel 已经有正确的尺寸
        self.render_timer.start(100)  # 延迟100ms

    def resizeEvent(self, event):
        # 获取当前 QLabel 的尺寸
        label_size = self.label.size()
        self.render_width = label_size.width()
        self.render_height = label_size.height()

        # 启动或重置定时器
        self.render_timer.start(200)  # 延迟200ms后渲染
        super().resizeEvent(event)

    def set_temperature(self, temperature):
        """设置温度并更新渲染。"""
        self.temperature = temperature
        print(f"设置温度为: {self.temperature}°C")
        self.update_render()

    def render_and_save(self, save_path, render_width, render_height):
        """渲染单个电池的可视化并保存为图像。"""
        if render_width <= 0 or render_height <= 0:
            print("无效的渲染尺寸:", render_width, render_height)
            return

        print(f"使用分辨率渲染: {render_width}x{render_height}")

        # 从 STL 文件加载 3D 模型
        mesh = pv.read(self.stl_file)
        
        # 获取最新的温度数据
        temperature = self.fetch_latest_temperature()

        # 创建温度数组，确保其长度与网格点数相同
        temperature_values = np.full(mesh.n_points, temperature)

        # 将温度数组添加到网格数据
        mesh.point_data["Temperature"] = temperature_values

        # 创建 Plotter 对象进行渲染
        plotter = pv.Plotter(off_screen=True)
        plotter.set_background("#e8f5e9")

        # 将网格添加到 Plotter，使用 'Temperature' 数组进行着色
        plotter.add_mesh(mesh, scalars="Temperature", cmap="coolwarm", show_edges=False, clim=[-20, 60])
        
        # 设置渲染窗口大小
        plotter.window_size = (render_width, render_height)

        # 设置等角视图
        plotter.view_isometric()
           
        # 渲染并保存图像
        plotter.screenshot(save_path)

        # 渲染完成后关闭 Plotter
        plotter.close()

    def create_responsive_label(self, save_path):
        """渲染 3D 图像并在 QLabel 中显示。"""
        # 渲染图像
        self.render_and_save(save_path, self.render_width, self.render_height)

        # 加载并显示渲染的图像
        pixmap = QPixmap(save_path)
        self.label.setPixmap(pixmap)

    def update_render(self):
        """根据当前尺寸更新渲染的图像。"""
        # 生成保存渲染图像的路径
        if self.battery_id is not None:
            save_path = os.path.join(self.save_dir, f"single_battery_render_{self.battery_id}.png")
        else:
            save_path = os.path.join(self.save_dir, "single_battery_render_default.png")

        # 渲染并更新 QLabel 中的图像
        self.create_responsive_label(save_path)
