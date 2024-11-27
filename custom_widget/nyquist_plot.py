
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
import sys
from PyQt6.QtGui import QColor

class NyquistPlot(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget(title="Nyquist Plot - Real-Time")
        self.plot_widget.setLabel('left', 'Negative Imaginary Impedance', units='m\u03A9')
        self.plot_widget.setLabel('bottom', 'Real Impedance', units='m\u03A9')
        # self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setBackground('w')

        # Add the plot widget to the layout
        self.layout.addWidget(self.plot_widget)
        
        self.legend = pg.LegendItem(offset=(30, 30))  
        self.legend.setParentItem(self.plot_widget.getViewBox())  

        # Dictionary to store data and plot objects for each battery
        self.battery_plots = {}

    def add_data(self, battery_number, real_impedance, negative_imaginary_impedance):
        """
        Add data for the specified battery and update its plot.
        """
        # Check if a curve for this battery exists
        if battery_number not in self.battery_plots:
            hue = (battery_number * 37) % 360  
            color = QColor.fromHsv(hue, 255, 230)  

    
            plot_data = self.plot_widget.plot([], [], pen=None,
                                            symbol='o',
                                            symbolSize=10,
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




        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NyquistPlot()
    win.show()
    sys.exit(app.exec())
