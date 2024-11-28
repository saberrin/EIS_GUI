import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy

class SingleBattery3DWidget:
    def __init__(self, stl_file, layout, battery_id=None):
        self.stl_file = stl_file
        self.layout = layout
        self.battery_id = battery_id

    def clear_existing_widgets(self):
        """Clear any existing widgets in the layout."""
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

    def assign_random_temperature(self):
        """Assign a random temperature to the battery model."""
        return np.random.uniform(-20, 60)  # Random temperature between -20 and 60°C

    def render_and_save(self, save_path, render_width, render_height):
        """Render the single battery visualization and save it as an image."""
        # Load the 3D model from the STL file
        mesh = pv.read(self.stl_file)
        
        # Assign a random temperature to the mesh (or use another method if available)
        temperature = self.assign_random_temperature()
        
        # Create an array for temperature (make sure it's the same length as the number of points in the mesh)
        temperature_values = np.full(mesh.n_points, temperature)  # This will assign the temperature to each point

        # Add the temperature array to the mesh
        mesh.point_data["Temperature"] = temperature_values

        plotter = pv.Plotter(off_screen=True)
        plotter.set_background("white")

        # Add the mesh to the plotter, using the 'Temperature' array to color the mesh
        plotter.add_mesh(mesh, scalars="Temperature", cmap="coolwarm", show_edges=True, clim=[-20, 60],)
        
        # plotter.add_scalar_bar(title="Temperature (°C)", vertical=True)
        
        
        # Set the window size
        plotter.window_size = (render_width, render_height)

        # Rotate the mesh to give it a 3D effect (adjust the angle as needed)
        plotter.view_isometric()  # Optionally, you can specify an angle: plotter.view_xy(), view_xz(), etc.
           
        # Render and save the image
        plotter.screenshot(save_path)

        # Close the plotter after rendering
        plotter.close()

    def create_responsive_label(self, save_path):
        """Render the 3D image and create a responsive label for the layout."""
        # Get layout dimensions to adjust rendering size
        layout_width = self.layout.geometry().width()
        layout_height = self.layout.geometry().height()

        # Render the image
        render_width = int(layout_width * 1.2)  # Optional scaling factor for the rendered image
        render_height = int(layout_height * 1.2)
        
        self.render_and_save(save_path, render_width, render_height)

        # Load and display the rendered image in a label
        label = QLabel()
        pixmap = QPixmap(save_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(True)
        self.layout.addWidget(label)

    def update_battery_render(self, save_path):
        """Main method to update battery details and render 3D image."""
        # Clear any existing widgets in the layout
        self.clear_existing_widgets()

        # Generate the path to save the rendered image
        if self.battery_id:
            save_path = f"3d_battery_model/single_battery_render_{self.battery_id}.png"
        else:
            save_path = "3d_battery_model/single_battery_render_default.png"

        # Create and render the 3D battery visualization
        self.create_responsive_label(save_path)