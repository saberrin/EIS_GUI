from PyQt6.QtCore import QObject, pyqtSignal
import sqlite3
from datetime import datetime
import fcntl
import time
import threading
import re
from smbus2 import SMBus
from repository import Repository

class I2CReader(QObject):
    new_data_received_UIT = pyqtSignal(int, float, float, float)
    new_data_received_SWF = pyqtSignal(int, float, float, float)
    new_data_received_check = pyqtSignal(str)

    def __init__(self, device, bus_number, address):
        super().__init__()
        self.device = device
        self.bus = bus_number
        self.address = address
        self.chunk_size = 1
        self.line_ending = b'_end'
        self.running = False
        self.data = []
        self.temperature = None
        self.voltage = None
        
        # Initialize SQLite database connection using the updated database
        self.db_path = "./eis_xjj.db"
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("SQLite database connection successful")
        except Exception as e:
            print(f"Error connecting to SQLite database: {e}")
            self.connection = None

    def start_reading(self):
        print("Starting I2C reading...")
        if self.connection is None:
            print("Cannot start reading as database connection is not established.")
            return
        self.running = True
        self.thread = threading.Thread(target=self.read_data, daemon=True)
        self.thread.start()
        self.new_data_received_check.emit("Starting I2C reading...")

    def stop_reading(self):
        print("Stopping I2C reading...")
        self.new_data_received_check.emit("Stopping I2C reading...")
        self.running = False

    def read_data(self):
        print("Attempting to open I2C bus...")
        self.new_data_received_check.emit("Attempting to open I2C bus...")
        self.write_data("start\n")
        try:
            while self.running:
                line = self.read_until_end()
                if line:
                    line_decoded = line.decode('utf-8', errors='replace').strip()
                    print(f"Received line: {line_decoded}")
                    self.data.append(line_decoded)
                    self.parse_and_emit_signals(line_decoded)
        except IOError as e:
            print(f"Could not open I2C bus: {e}")
            self.new_data_received_check.emit(f"Could not open I2C bus: {e}")
            self.running = False

    def read_until_end(self):
        buffer = bytearray()
        I2C_SLAVE = 0x0703
        while True:
            try:
                with open(self.device, 'rb', buffering=0) as f:
                    fcntl.ioctl(f, I2C_SLAVE, self.address)
                    while True:
                        chunk = f.read(self.chunk_size)
                        if not chunk:
                            break
                        buffer.extend(chunk)
                        if self.line_ending in buffer:
                            line_end_index = buffer.index(self.line_ending) + len(self.line_ending)
                            line = buffer[:line_end_index]
                            del buffer[:line_end_index]
                            return line
            except IOError:
                time.sleep(0.01)

    def write_data(self, data_to_send):
        if isinstance(data_to_send, str):
            if not data_to_send.endswith('\n'):
                data_to_send += "\n"
            with SMBus(self.bus) as bus:
                try:
                    for char in data_to_send:
                        bus.write_byte(self.address, ord(char))
                        time.sleep(0.1)
                except Exception as e:
                    print(f"Error sending data: {e}")
        else:
            print("Input must be a string")

    def parse_and_emit_signals(self, line):
        """
        Parses the incoming I2C line and emits the appropriate signals.
        """
        print(f"Parsing line: {line}")

        # Extract the unique cell ID from the line (e.g., 0x28)
        board_id_match = re.match(r'(\w+)_EIS_data_packet_start', line)
        if not board_id_match:
            print("Invalid data packet format")
            return
        cell_id = int(board_id_match.group(1), 16)

        # Extract voltage
        voltage_match = re.search(r'VOLTAGE_([\d.]+)', line)
        voltage = float(voltage_match.group(1)) if voltage_match else None
        if voltage is None:
            print("Voltage not found in the data packet.")
            return

        # Extract data points (R, I, F)
        data_pattern = r'R(\d+),([-\d.]+),I\1,([-\d.]+),F\1,([\d.]+)'
        data_points = re.findall(data_pattern, line)

        if not data_points:
            print("No valid data points found in the packet.")
            return

        # Insert data into the database
        self.insert_measurements(cell_id, data_points, voltage)

    def insert_measurements(self, cell_id, data_points, voltage):
        """
        Inserts parsed data into the database using the Repository class.
        """
        repo = Repository()
        real_time_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        measurements = []
        for dp in data_points:
            real_impedance = float(dp[1])
            imag_impedance = float(dp[2])
            frequency = float(dp[3])
            
            # Create an EisMeasurement object
            measurement = {
                "cell_id": cell_id,
                "real_time_id": real_time_id,
                "frequency": frequency,
                "real_impedance": real_impedance,
                "imag_impedance": imag_impedance,
                "voltage": voltage
            }
            measurements.append(measurement)

        # Insert all measurements
        repo.insert_measurements(measurements)
        print(f"Inserted {len(measurements)} measurements for cell {cell_id}.")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
