import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
import sys
from PyQt6.QtGui import QColor

class BodePlot(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget(title="Bode Plot - Real-Time")
        self.plot_widget.setLabel('left', 'Magnitude (dB)', units='dB')
        self.plot_widget.setLabel('bottom', 'Frequency (Hz)', units='Hz')
        self.plot_widget.setBackground('w')

        # Add the plot widget to the layout
        self.layout.addWidget(self.plot_widget)
        
        self.legend = pg.LegendItem(offset=(30, 30))  
        self.legend.setParentItem(self.plot_widget.getViewBox())  

        # Dictionary to store data and plot objects for each battery
        self.battery_plots = {}

    def add_data(self, battery_number, frequency, magnitude, phase):
        """
        Add data for the specified battery and update its plot.
        """
        # Check if a curve for this battery exists
        if battery_number not in self.battery_plots:
            hue = (battery_number * 37) % 360  # Adjust the hue for each battery
            color = QColor.fromHsv(hue, 255, 230)  # Convert hue to RGB color

            plot_data_magnitude = self.plot_widget.plot([], [], pen=color, name=f"Battery {battery_number} Magnitude")
            plot_data_phase = self.plot_widget.plot([], [], pen=color, name=f"Battery {battery_number} Phase")

            self.legend.addItem(plot_data_magnitude, f"Battery {battery_number} Magnitude")
            self.legend.addItem(plot_data_phase, f"Battery {battery_number} Phase")

            self.battery_plots[battery_number] = {
                "frequency": [],
                "magnitude": [],
                "phase": [],
                "plot_magnitude": plot_data_magnitude,
                "plot_phase": plot_data_phase
            }

        # Add new data to the battery's data list
        self.battery_plots[battery_number]["frequency"].append(frequency)
        self.battery_plots[battery_number]["magnitude"].append(magnitude)
        self.battery_plots[battery_number]["phase"].append(phase)

        # Update the plot for magnitude and phase
        self.battery_plots[battery_number]["plot_magnitude"].setData(
            self.battery_plots[battery_number]["frequency"],
            self.battery_plots[battery_number]["magnitude"]
        )
        self.battery_plots[battery_number]["plot_phase"].setData(
            self.battery_plots[battery_number]["frequency"],
            self.battery_plots[battery_number]["phase"]
        )

    def clear_battery_plot(self, battery_number):
        """
        Clear data and remove the plot for a specific battery.
        """
        if battery_number in self.battery_plots:
            self.plot_widget.removeItem(self.battery_plots[battery_number]["plot_magnitude"])
            self.plot_widget.removeItem(self.battery_plots[battery_number]["plot_phase"])
            del self.battery_plots[battery_number]

    def clear_all_plots(self):
        """
        Clear all battery plots.
        """
        for battery_number in list(self.battery_plots.keys()):
            self.clear_battery_plot(battery_number)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BodePlot()
    win.show()
    sys.exit(app.exec())
