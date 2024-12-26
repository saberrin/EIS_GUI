import pyvista as pv
import numpy as np
import os
import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
from database.config import DB_PATH  # 假设 DB_PATH 定义了数据库路径

class HeatMap3DWidget(QWidget):
    def __init__(self, stl_file, num_cells=13, parent=None):
        super().__init__(parent)
        self.stl_file = stl_file
        self.num_cells = num_cells

        # 初始化温度和3D模型数据
        self.mesh = pv.read(self.stl_file)
        self.cell_indices = self.split_cells(self.mesh.n_points, self.num_cells)

        # 初始化布局和 QLabel
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # # 从数据库获取温度值
        # self.temperature_data = None
        # self.update_temperature_from_db()

        # # 如果 self.temperature_data 仍为空，设置默认数据
        # if self.temperature_data is None:
        #     default_temperature = 25.0
        #     cell_temperatures = [default_temperature] * self.num_cells
        #     self.temperature_data = self.assign_temperatures_with_transition(cell_temperatures)

    def split_cells(self, num_points, num_cells):
        """将模型的点分配到每个电池（cell）"""
        points_per_cell = num_points // num_cells
        cell_indices = []
        for i in range(num_cells):
            start = i * points_per_cell
            end = (i + 1) * points_per_cell if i != num_cells - 1 else num_points
            cell_indices.append(np.arange(start, end))
        return cell_indices

    def assign_temperatures_with_transition(self, cell_temperatures):
        """
        分配温度值到 mesh 的每个点，并在 cell 边界处平滑过渡。
        """
        temperature_data = np.zeros(self.mesh.n_points)
        for i, indices in enumerate(self.cell_indices):
            temperature_data[indices] = cell_temperatures[i]

        # 平滑边界温度过渡
        for i in range(len(self.cell_indices) - 1):
            current_indices = self.cell_indices[i]
            next_indices = self.cell_indices[i + 1]
            boundary_points = np.intersect1d(current_indices[-10:], next_indices[:10])
            transition_value = (cell_temperatures[i] + cell_temperatures[i + 1]) / 2
            temperature_data[boundary_points] = transition_value

        return temperature_data

    def clear_existing_widgets(self):
        """清理布局中已有的控件，避免重复累积。"""
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

    def render_and_save(self, save_path, render_width, render_height):
        """
        渲染热力图并保存为图片。
        """
        upscale_factor = 2
        render_width *= upscale_factor
        render_height *= upscale_factor

        plotter = pv.Plotter(off_screen=True)
        plotter.set_background("#e8f5e9")
        plotter.enable_anti_aliasing()

        # 将温度数据分配到 mesh
        self.mesh["Temperature"] = self.temperature_data

        # 创建自定义颜色映射函数：蓝色 (低于 70°C)，红色 (高于 70°C)
        def custom_colormap(temp):
            if temp < 70:
                # 温度小于 70°C，使用从深蓝到浅蓝的颜色渐变
                return [0, 0, 1]  # 蓝色（深蓝到浅蓝）
            else:
                # 温度大于 70°C，使用从浅红到深红的颜色渐变
                return [1, 0, 0]  # 红色（浅红到深红）

        # 创建自定义颜色映射（这里按温度数据的范围进行逐点映射）
        colors = np.array([custom_colormap(temp) for temp in self.temperature_data])

        # 将网格添加到 Plotter，并使用 'Temperature' 数组进行着色
        plotter.add_mesh(
            self.mesh,
            scalars="Temperature",  # 使用 'Temperature' 数据来着色
            cmap="coolwarm",  # 默认的颜色映射作为背景
            show_edges=False,
            clim=[-20, 100],  # 设置温度范围从 -20 到 100
        )

        # 为了避免 'rgb' 参数报错，我们不在这里传递 `rgb=colors`
        # 在这里我们通过 `scalars` 参数来进行颜色映射，`rgb` 被去掉

        # 计算相机位置
        model_bounds = self.mesh.bounds
        center_x = (model_bounds[0] + model_bounds[1]) / 2
        center_y = (model_bounds[2] + model_bounds[3]) / 2
        center_z = (model_bounds[4] + model_bounds[5]) / 2
        camera_position = [
            (center_x - 250, center_y + 700, center_z - 700),
            (center_x, center_y, center_z),
            (-0.21, 0.69, -0.685),
        ]
        plotter.camera_position = camera_position

        # 渲染并保存图片
        plotter.screenshot(save_path, window_size=(render_width, render_height))
        plotter.close()



    def create_responsive_label(self, save_path, ui_width, ui_height):
        """根据布局大小渲染图片，并在 QLabel 中显示。"""
        self.clear_existing_widgets()

        render_width = int(ui_width // 4)
        render_height = int(ui_height // 4)
        self.render_and_save(save_path, render_width, render_height)

        label = QLabel()
        pixmap = QPixmap(save_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(True)
        self.layout.addWidget(label)

    def update_temperature_from_db(self):
        """从数据库获取最新温度值，并更新热力图"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            # 查询最新 real_time_id 的 temperature
            cursor.execute(
                """
                SELECT temperature FROM generated_info 
                WHERE real_time_id = (SELECT MAX(real_time_id) FROM generated_info)
                """
            )
            result = cursor.fetchone()
            if result:
                latest_temperature = result[0]
                print(f"Latest temperature from database: {latest_temperature}")

                # 第一个 cell 使用最新温度值
                cell_temperatures = [latest_temperature]

                # 其他 cells 的温度随机分布在上下 0.5°C 范围内
                for _ in range(1, self.num_cells):
                    random_temperature = np.random.uniform(latest_temperature - 0.5, latest_temperature + 0.5)
                    cell_temperatures.append(random_temperature)

                # 更新温度数据并渲染
                self.temperature_data = self.assign_temperatures_with_transition(cell_temperatures)
                save_path = "heatmap_render.png"
                ui_width = self.parent().width()
                ui_height = self.parent().height()
                self.create_responsive_label(save_path, ui_width, ui_height)
            else:
                print("No temperature data found in the database.")

                # 设置默认温度数据（例如全部为 25°C）
                default_temperature = 0
                cell_temperatures = [default_temperature] * self.num_cells
                self.temperature_data = self.assign_temperatures_with_transition(cell_temperatures)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
