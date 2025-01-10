
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication,QGestureEvent, QPinchGesture
import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QColor
import matplotlib.pyplot as plt

class NyquistPlot(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget(title="实时阻抗数据采集")
        self.plot_widget.setLabel('left', '负虚部阻抗', units='m\u03A9')
        self.plot_widget.setLabel('bottom', '实部阻抗', units='m\u03A9')
        # self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setBackground('#e8f5e9')
        
        # Add the plot widget to the layout
        self.layout.addWidget(self.plot_widget)
        
        self.legend = pg.LegendItem(offset=(5, 5))  
        self.legend.setParentItem(self.plot_widget.getViewBox())  
        
        # Dictionary to store data and plot objects for each battery
        self.battery_plots = {}
        self.cmap = plt.get_cmap('tab20') 

        # Enable gesture recognition
        # self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        # self.grabGesture(Qt.GestureType.PinchGesture)

        # self.scale_factor = 1  # Initial scale factor

    # def gestureEvent(self, event: QGestureEvent) -> bool:
    #     if event.gesture(Qt.GestureType.PinchGesture):
    #         pinch = event.gesture(Qt.GestureType.PinchGesture)

    #         # Update scale factor based on pinch movement
    #         scale_delta = pinch.scaleFactor()

    #         # Apply zoom effect
    #         if scale_delta != 1:
    #             self.scale_factor *= scale_delta
    #             self.scale_factor = max(0.1, min(self.scale_factor, 10))  # Limit zoom range
    #             self.apply_scale()

    #         return True
    #     return False

    # def apply_scale(self):
    #     # Apply scaling to all plots (you can apply zoom effect in your data or plot ranges here)
    #     for battery_number, data in self.battery_plots.items():
    #         real_scaled = [x * self.scale_factor for x in data["real"]]
    #         imag_scaled = [y * self.scale_factor for y in data["imag"]]
    #         data["plot"].setData(real_scaled, imag_scaled)

    def add_data(self, battery_number, real_impedance, negative_imaginary_impedance):
        """
        Add data for the specified battery and update its plot.
        """
        # Check if a curve for this battery exists
        if battery_number not in self.battery_plots:
            color = self.cmap(battery_number % 13)  # Get color from the colormap
            
            # Convert the color to QColor
            color = QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))  

    
            plot_data = self.plot_widget.plot([], [], pen=None,
                                            symbol='o',
                                            symbolSize=5,
                                            symbolBrush=color)
            self.legend.addItem(plot_data, f"Battery {battery_number}")

            self.battery_plots[battery_number] = {
                "real": [],
                "imag": [],
                "plot": plot_data
            }
        # Add new data to the battery's data list
        self.battery_plots[battery_number]["real"].append(real_impedance)
        self.battery_plots[battery_number]["imag"].append(negative_imaginary_impedance)

        # Update the plot
        self.battery_plots[battery_number]["plot"].setData(
            self.battery_plots[battery_number]["real"],
            self.battery_plots[battery_number]["imag"]
        )

    def clear_battery_plot(self, battery_number):
        """
        Clear data and remove the plot for a specific battery.
        """
        if battery_number in self.battery_plots:
            self.plot_widget.removeItem(self.battery_plots[battery_number]["plot"])
            del self.battery_plots[battery_number]

    def clear_all_plots(self):
        """
        Clear all battery plots.
        """
        for battery_number in list(self.battery_plots.keys()):
            self.clear_battery_plot(battery_number)
        # Clear the legend
        self.legend.clear()



        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NyquistPlot()
    win.show()
    sys.exit(app.exec())
