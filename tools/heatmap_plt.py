import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy, QApplication
from PIL import Image, ImageOps

class HeatMap3DWidget:
    def __init__(self, stl_file, num_cells=13):
        self.stl_file = stl_file
        self.num_cells = num_cells

        # Generate random temperature data for the cells
        self.cell_temperatures = np.random.uniform(-20, 60, self.num_cells)

        # Load the 3D mesh from the STL file
        self.mesh = pv.read(self.stl_file)
        self.cell_indices = self.split_cells(self.mesh.n_points, self.num_cells)
        self.temperature_data = self.assign_temperatures_with_transition(self.cell_temperatures)

    def split_cells(self, num_points, num_cells):
        """Divide the mesh points into sections for each battery cell."""
        points_per_cell = num_points // num_cells
        cell_indices = []
        for i in range(num_cells):
            start = i * points_per_cell
            end = (i + 1) * points_per_cell if i != num_cells - 1 else num_points
            cell_indices.append(np.arange(start, end))
        return cell_indices

    def assign_temperatures_with_transition(self, cell_temperatures):
        """Assign temperatures to the mesh with smooth transitions."""
        temperature_data = np.zeros(self.mesh.n_points)
        for i, indices in enumerate(self.cell_indices):
            temperature_data[indices] = cell_temperatures[i]

        # Smooth the temperature transitions at boundaries
        for i in range(len(self.cell_indices) - 1):
            current_indices = self.cell_indices[i]
            next_indices = self.cell_indices[i + 1]
            boundary_points = np.intersect1d(current_indices[-10:], next_indices[:10])
            transition_value = (cell_temperatures[i] + cell_temperatures[i + 1]) / 2
            temperature_data[boundary_points] = transition_value

        return temperature_data


    def render_and_save(self, save_path, render_width, render_height):
        """
        Render the 3D heatmap and save it as an image.

        Args:
            save_path (str): Path to save the rendered image.
            render_width (int): Width of the rendered image in pixels.
            render_height (int): Height of the rendered image in pixels.
        """
        plotter = pv.Plotter(off_screen=True)
        plotter.set_background("white")

        # Assign temperature data to the mesh
        self.mesh["Temperature"] = self.temperature_data

        # Add the mesh and scalar bar
        plotter.add_mesh(
            self.mesh,
            scalars="Temperature",
            cmap="coolwarm",
            show_edges=False,
            clim=[-20, 60],
        )
        plotter.add_scalar_bar(title="Temperature (C)", shadow=True)

        # Compute the center and bounds of the model
        model_bounds = self.mesh.bounds
        center_x = (model_bounds[0] + model_bounds[1]) / 2
        center_y = (model_bounds[2] + model_bounds[3]) / 2
        center_z = (model_bounds[4] + model_bounds[5]) / 2

        # Position the camera to focus on the model
        camera_position = [
            (center_x - 250, center_y + 700, center_z - 700),  # Camera position
            (center_x, center_y, center_z),                   # Focal point
            (-0.21, 0.69, -0.69),                             # View up direction
        ]
        plotter.camera_position = camera_position
        

        # Render and save the image at the specified resolution
        plotter.screenshot(save_path, window_size=(render_width*2, render_height*2))
        plotter.close()


    def create_responsive_label(self, save_path, layout):
        """
        Create a QLabel with the rendered image, ensuring it fits slightly larger than the widget
        and is centered within the layout.

        Args:
            save_path (str): Path to save the rendered image.
            layout (QLayout): Layout to add the QLabel to.
        """
        # Get the layout dimensions
        layout_width = layout.geometry().width()
        layout_height = layout.geometry().height()

        # Render the heatmap slightly larger than the layout
        render_width = int(layout_width * 1.2)
        render_height = int(layout_height * 1.2)
        self.render_and_save(save_path, render_width, render_height)

        # Load the rendered image
        label = QLabel()
        pixmap = QPixmap(save_path)

        # Center the pixmap in the QLabel
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Configure QLabel to fit within the layout
        label.setScaledContents(False)  # No scaling, maintain original resolution
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Add the QLabel to the layout
        layout.addWidget(label)



    # def render_and_save(self, save_path, render_width=3840, render_height=2160):
    #     """Render the 3D heatmap and save it as an image."""
    #     plotter = pv.Plotter(off_screen=True)
    #     plotter.set_background("black")

    #     # Set temperature data
    #     self.mesh["Temperature"] = self.temperature_data

    #     # Add the mesh and scalar bar
    #     plotter.add_mesh(
    #         self.mesh,
    #         scalars="Temperature",
    #         cmap="coolwarm",
    #         show_edges=False,
    #         clim=[-20, 60],
    #     )
    #     plotter.add_scalar_bar(title="Temperature (C)", shadow=True)

    #     # Compute the center and bounds of the model
    #     model_bounds = self.mesh.bounds
    #     center_x = (model_bounds[0] + model_bounds[1]) / 2
    #     center_y = (model_bounds[2] + model_bounds[3]) / 2
    #     center_z = (model_bounds[4] + model_bounds[5]) / 2

    #     # Position the camera far enough to capture the full model
    #     camera_position = [
    #         (center_x - 300, center_y + 1000, center_z - 1000),  # Camera position
    #         (center_x, center_y, center_z),              # Focal point
    #         (-0.21, 0.69, -0.69),                                   # View up direction
    #     ]
    #     plotter.camera_position = camera_position

    #     # Save the image
    #     plotter.screenshot(save_path, window_size=(render_width, render_height))
    #     plotter.close()

    # def create_responsive_label(self, save_path, layout, crop_values=None):
    #     """
    #     Create a QLabel with the rendered image, crop it using adjustable crop values, 
    #     and add it to the layout.

    #     Args:
    #         save_path (str): Path to the saved rendered image.
    #         layout (QLayout): Layout to add the QLabel to.
    #         crop_values (dict): Dictionary with crop values for each edge. Example:
    #                             {"left": 50, "right": 50, "top": 20, "bottom": 20}
    #     """
    #     # Set default crop values if not provided
    #     if crop_values is None:
    #         crop_values = {"left": 200, "right": 200, "top": 20, "bottom": 20}

    #     # Render and save the heatmap at a high resolution to preserve details
    #     render_width, render_height = 3840, 2160  # 4K resolution
    #     self.render_and_save(save_path, render_width, render_height)

    #     # Load the rendered image using PIL
    #     image = Image.open(save_path)

    #     # Crop the image using the specified crop values
    #     left = crop_values.get("left", 100)
    #     right = crop_values.get("right", 100)
    #     top = crop_values.get("top", 20)
    #     bottom = crop_values.get("bottom", 20)
    #     cropped_image = image.crop((
    #         left,  # Left edge
    #         top,   # Top edge
    #         image.width - right,  # Right edge
    #         image.height - bottom  # Bottom edge
    #     ))

    #     # Ensure the aspect ratio matches the QLabel's layout while keeping the entire model visible
    #     layout_width = layout.geometry().width()
    #     layout_height = layout.geometry().height()
    #     aspect_ratio_layout = layout_width / layout_height
    #     aspect_ratio_image = cropped_image.width / cropped_image.height

    #     if aspect_ratio_image > aspect_ratio_layout:
    #         # Add padding vertically to match layout aspect ratio
    #         new_height = int(cropped_image.width / aspect_ratio_layout)
    #         padding = (new_height - cropped_image.height) // 2
    #         cropped_image = ImageOps.expand(cropped_image, border=(0, padding), fill="black")
    #     else:
    #         # Add padding horizontally to match layout aspect ratio
    #         new_width = int(cropped_image.height * aspect_ratio_layout)
    #         padding = (new_width - cropped_image.width) // 2
    #         cropped_image = ImageOps.expand(cropped_image, border=(padding, 0), fill="black")

    #     # Save the cropped and padded image
    #     processed_path = save_path.replace(".png", "_processed.png")
    #     cropped_image.save(processed_path)

    #     # Load the processed image into a QLabel
    #     label = QLabel()
    #     pixmap = QPixmap(processed_path)

    #     # Resize the pixmap to fit 1/4th of the layout, keeping aspect ratio
    #     target_width = layout.geometry().width() 
    #     target_height = layout.geometry().height() 
    #     resized_pixmap = pixmap.scaled(
    #         target_width,
    #         target_height,
    #         Qt.AspectRatioMode.KeepAspectRatio
    #     )
    #     label.setPixmap(resized_pixmap)

    #     # Configure QLabel to fit into the layout
    #     label.setScaledContents(True)
    #     label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    #     # Add the QLabel to the layout
    #     layout.addWidget(label)

    # def create_responsive_label(self, save_path, layout):
    #     """Create a QLabel with the rendered image and add it to the layout."""
    #     # Render and save the heatmap with its original resolution
    #     self.render_and_save(save_path, 1920, 1080)  # Specify fixed resolution for clarity

    #     # Create a QLabel and load the original image
    #     label = QLabel()
    #     pixmap = QPixmap(save_path)

    #     # Set the original pixmap without scaling or modification
    #     label.setPixmap(pixmap)

    #     # Optional: Set QLabel to allow contents to scale if necessary
    #     label.setScaledContents(False)

    #     # Add the QLabel to the provided layout
    #     layout.addWidget(label)





