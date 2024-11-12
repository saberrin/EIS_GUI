from PyQt6.QtCore import QObject, pyqtSignal
import sqlite3
from datetime import datetime
import fcntl
import time
import threading
import re
from smbus2 import SMBus
from typing import List, Dict
from database.repository import Repository
from database.entity import EisMeasurement

class I2CReader(QObject):
    new_data_received_UIT = pyqtSignal(int, float, float, float)
    new_data_received_SWF = pyqtSignal(int, float, float, float)
    new_data_received_check = pyqtSignal(str)

    def __init__(self, device, bus_number,timeout_duration=10):
        super().__init__()
        self.device = device
        self.bus = bus_number
        self.address = None
        self.chunk_size = 1
        self.line_ending = b'_end'
        self.timeout_duration = timeout_duration
        self.running = False
        self.data = []
        self.temperature = None
        self.voltage = None
        self.repo = Repository()
        
        # Initialize SQLite database connection using the updated database
        self.db_path = "./eis_xjj.db"
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("SQLite database connection successful")
        except Exception as e:
            print(f"Error connecting to SQLite database: {e}")
            self.connection = None

    def start_reading(self,address):
        self.address = address
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
        # if hasattr(self, 'thread') and self.thread.is_alive():
        #     self.thread.join()  

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
                    self.parse_and_insert_data(line_decoded)
        except IOError as e:
            print(f"Could not open I2C bus: {e}")
            self.new_data_received_check.emit(f"Could not open I2C bus: {e}")
            self.running = False

    def read_until_end(self):
        buffer = bytearray()
        I2C_SLAVE = 0x0703 
        start_time = time.time()
        while self.running:
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
            except IOError as e:
                if time.time() - start_time > self.timeout_duration:
                    print(f"Failed to open I2C bus after {self.timeout_duration} seconds. Stopping read attempts.")
                    self.new_data_received_check.emit(f"Failed to open I2C bus after {self.timeout_duration} seconds.")
                    self.running = False
                    break
                time.sleep(0.01)

    def write_data(self, data_to_send):
        if isinstance(data_to_send, str):
            if not data_to_send.endswith('\n'):
                data_to_send += "\n"
            with SMBus(self.bus) as bus:
                try:
                    for char in data_to_send:
                        bus.write_byte(self.address, ord(char))
                        time.sleep(0.01)
                except Exception as e:
                    print(f"Error sending data: {e}")
        else:
            print("Input must be a string")

    def parse_and_insert_data(self, line: str):
        """
        Parses the incoming data line, creates EisMeasurement objects, and inserts them into the database.
        """
        if "EIS_data_packet_start" in line:
            try:
                # Extract the voltage value
                voltage = float(line.split("VOLTAGE_")[1].split("_EIS_data_packet_end")[0])
                
                # Extract data points
                data_points = self.extract_data_points(line)
                
                # Cell ID (unique identifier for your device, like 0x28)
                cell_id = int(line.split('_')[0], 16)

                # Insert the parsed measurements into the database
                self.insert_measurements(cell_id, data_points, voltage)

            except (ValueError, IndexError) as e:
                print(f"Error parsing data: {line}, Error: {e}")

    def extract_data_points(self, line: str) -> List[tuple]:
        """
        Extracts R, I, and F data points from the line and returns a list of tuples.
        """
        data_points = []
        sections = line.split(";")
        
        for section in sections:
            if section.startswith("R") and "I" in section and "F" in section:
                try:
                    real_imp = float(section.split(",")[1])
                    imag_imp = float(section.split(",")[3])
                    frequency = float(section.split(",")[5])
                    data_points.append((real_imp, imag_imp, frequency))
                except (ValueError, IndexError):
                    continue
        
        return data_points

    def insert_measurements(self, cell_id: int, data_points: List[tuple], voltage: float):
        """
        Converts parsed data into EisMeasurement objects and inserts them into the database.
        """
        real_time_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        measurements = []

        # Create EisMeasurement objects
        for dp in data_points:
            real_impedance, imag_impedance, frequency = dp
            measurement = EisMeasurement(
                cell_id=cell_id,
                real_time_id=real_time_id,
                frequency=frequency,
                real_impedance=real_impedance,
                imag_impedance=imag_impedance,
                voltage=voltage
            )
            measurements.append(measurement)

        # Insert into database using Repository
        self.repo.insert_measurements(measurements)
        print(f"Inserted {len(measurements)} measurements for cell {cell_id}.")

    def close(self):
        self.stop_reading()
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
