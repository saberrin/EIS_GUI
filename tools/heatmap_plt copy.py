import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class HeatMap3DWidget(QWidget):
    def __init__(self, stl_file, num_cells=13, parent=None):
        super().__init__(parent)
        self.stl_file = stl_file
        self.num_cells = num_cells

        # 初始化温度和3D模型数据
        self.cell_temperatures = np.random.uniform(-20, 60, self.num_cells)
        self.mesh = pv.read(self.stl_file)
        self.cell_indices = self.split_cells(self.mesh.n_points, self.num_cells)
        self.temperature_data = self.assign_temperatures_with_transition(self.cell_temperatures)

        # 初始化布局和 QLabel
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        

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

        # 放大渲染尺寸以提高清晰度
        upscale_factor = 2
        render_width *= upscale_factor
        render_height *= upscale_factor

        plotter = pv.Plotter(off_screen=True)
        plotter.set_background("#e8f5e9")
        plotter.enable_anti_aliasing()

        # Assign temperature data to the mesh
        self.mesh["Temperature"] = self.temperature_data

        # Add the mesh
        plotter.add_mesh(
            self.mesh,
            scalars="Temperature",
            cmap="Blues",  # 使用更亮的蓝色颜色映射
            show_edges=False,
            clim=[-20, 60],
        )

        # Compute camera position
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

        # Render and save the image
        plotter.screenshot(save_path, window_size=(render_width, render_height))
        plotter.close()

    def create_responsive_label(self, save_path, ui_width, ui_height):
        """根据布局大小渲染图片，并在 QLabel 中显示。"""
        # 清理已有控件
        self.clear_existing_widgets()

        # 渲染图片
        render_width = int(ui_width // 4)  # 最大宽度为 UI 宽度的一半
        render_height = int(ui_height // 4)  # 最大高度为 UI 高度的一半
        self.render_and_save(save_path, render_width, render_height)

        # 创建 QLabel 显示渲染的图片
        label = QLabel()
        pixmap = QPixmap(save_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(True)  # 确保图片适配 QLabel
        self.layout.addWidget(label)

    def update_heatmap(self, new_temperatures=None):
        """
        更新热力图内容，可以传入新的温度数据，并将每个 cell 的温度随机化在新温度值上下 2 摄氏度范围内。
        """
        if new_temperatures is not None:
            if len(new_temperatures) != self.num_cells:
                raise ValueError(f"Expected {self.num_cells} temperatures, got {len(new_temperatures)}")
            
            # 为每个 cell 的温度生成随机值，在传入温度的上下 1°C 范围内
            self.cell_temperatures = [
                np.random.uniform(temp - 1, temp + 1) for temp in new_temperatures
            ]
            self.temperature_data = self.assign_temperatures_with_transition(self.cell_temperatures)

        # 渲染并显示最新的热力图
        save_path = "heatmap_render.png"
        ui_width = self.parent().width()
        ui_height = self.parent().height()
        self.create_responsive_label(save_path, ui_width, ui_height)
