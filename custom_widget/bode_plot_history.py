import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
import sys
from PyQt6.QtGui import QColor, QPen
from math import sqrt
from collections import defaultdict
from database.repository import Repository

class BodePlotHistory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.repo = Repository()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the plot widget for Bode Plot (Magnitude and Phase)
        self.plot_widget = pg.PlotWidget(title="单电芯短期内阻抗演变趋势（Bode图）")
        self.plot_widget.setLabel('left', '幅度(dB)', units='dB')
        self.plot_widget.setLabel('bottom', '频率 (Hz)', units='Hz')
        self.plot_widget.setBackground('#e8f5e9')

        # Add the plot widget to the layout
        self.layout.addWidget(self.plot_widget)

        self.legend = pg.LegendItem(offset=(30, 30))  # Legend to identify different batteries
        self.legend.setParentItem(self.plot_widget.getViewBox())  

        # Dictionary to store data and plot objects for each battery
        self.battery_plots = {}

    def update_data(self,cell_id):
        data = self.repo.get_cell_history(cell_id, index=10)
        
        # 用来存储处理后的频率、实部和虚部数据
        result = defaultdict(lambda: ([], [], []))  # 用频率、实部、虚部的列表初始化
        
        # 处理每一条数据
        for real_time_id, measurements in data.items():
            for measurement in measurements:
                # 将频率、实部阻抗和虚部阻抗分别添加到各自的列表
                result[real_time_id][0].append(measurement.frequency)
                result[real_time_id][1].append(measurement.real_impedance)
                result[real_time_id][2].append(measurement.imag_impedance)
        
        # 将处理后的数据添加到历史 Bode 图中
        for real_time_id, data in result.items():
            self.add_data(real_time_id, data[0], data[1], data[2])

    def add_data(self, battery_number, frequency, magnitude, phase):
        """
        Add data for the specified battery and update its plot.
        """
        # frequency = np.array(frequency)  # 转换为 numpy 数组
        # magnitude = np.array(magnitude)  # 转换为 numpy 数组
        # phase = np.array(phase)  # 转换为 numpy 数组

        print (frequency, magnitude, phase)
        # Use Golden Ratio method for better hue distribution

        golden_ratio_conjugate = (1 + sqrt(5)) / 2  # Golden Ratio
        base_hue = 137.508  # A widely used base for visually pleasing separation

        if isinstance(battery_number, str):
            hue = (hash(battery_number) % 360) + base_hue  # Use hash to vary the input
        else:
            hue = (battery_number * base_hue) % 360

        # Ensure hue wraps within 0-360
        hue = int(hue % 360)

        # Create the color from the hue value, and vary saturation and brightness for distinction
        color = QColor.fromHsv(hue, 200 + (hue % 50), 230)
        # Create a QPen object to set the line width and color
        pen = QPen(color)
        pen.setWidth(6)  # Set line width to 3 pixels (adjust as needed)
        # Check if a curve for this battery exists
        if battery_number not in self.battery_plots:
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

        # Update the plot
        self.battery_plots[battery_number]["plot_magnitude"].setData(
            self.battery_plots[battery_number]["frequency"][0],
            self.battery_plots[battery_number]["magnitude"][0]
        )
        self.battery_plots[battery_number]["plot_phase"].setData(
            self.battery_plots[battery_number]["frequency"][0],
            self.battery_plots[battery_number]["phase"][0]
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
        self.legend.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BodePlotHistory()
    win.show()
    sys.exit(app.exec())
