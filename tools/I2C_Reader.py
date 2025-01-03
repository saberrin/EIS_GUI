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
from algorithm.EISAnalyzer import EISAnalyzer
from collections import Counter
import json
class I2CReader(QObject):
    new_data_received_SWF = pyqtSignal(int, float, float, float)
    new_data_received_check = pyqtSignal(str)
    new_data_received_finish_list = pyqtSignal(list)
    new_data_received_batterycellInfo = pyqtSignal(int, int, float) #显示序号、cell_id和实部阻抗

    def __init__(self, bus_number,timeout_duration=0.01):
        super().__init__()
        self.device = "/dev/i2c-" + str(bus_number)
        self.bus = bus_number
        self.port = None
        self.address = None
        self.chunk_size = 1
        self.line_ending = b'_end'
        self.timeout_duration = timeout_duration
        self.running = True
        self.data = []
        self.temperature = None
        self.voltage = None
        self.repo = Repository()
        self.confirmed_addresses = []
        self.confirmed_addresses_1 = [] #继电器切换后的电芯地址                                     
        self.failed_addresses = []
        self.finish_list_addr = []
        self.finish_list_cell = []
        self.real_time_id = None
        # User input attributes for container, cluster, and pack
        self.container_number = None
        self.cluster_number = None
        self.pack_number = None

        with open("config.json", "r") as config_file:
            self.config = json.load(config_file)

    def get_port(self,port):
        self.port = port

    def set_user_selection(self, container_number, cluster_number, pack_number):
        """Sets the container, cluster, and pack based on user input."""
        self.container_number = container_number
        self.cluster_number = cluster_number
        self.pack_number = pack_number
        print(f"Identifiers set: Container {container_number}, Cluster {cluster_number}, Pack {pack_number}")


        # Initialize SQLite database connection using the updated database
        self.db_path = "./eis_xjj.db"
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.new_data_received_check.emit("已连接SQLite数据库")
            print("SQLite database connection successful")
        except Exception as e:
            print(f"Error connecting to SQLite database: {e}")
            self.connection = None

    def start_reading(self, address_list):
        print("Starting I2C reading...")
        self.new_data_received_check.emit("I2C总线连接中...")
        thread = threading.Thread(target=self.process_address, args=(address_list,),daemon=True)
        thread.start()
        time.sleep(0.1)  


    def process_address(self, address_list):
        for address in address_list:
            data = "start\n"
            self.write_data(data,address)
            expected_data = f"{hex(address)}_Received I2C_Command_{data}_end"

            if self.verify_data(data, address, expected_data): 
                print(f"Address {hex(address)} confirmed successfully.")
                self.confirmed_addresses.append(address) 
            else:
                print(f"Failed to get confirmation from address {hex(address)}.")
                self.failed_addresses.append(address) 

            if len(self.confirmed_addresses) + len(self.failed_addresses) == len(address_list):
                print("Starting data reading for confirmed addresses...")
                self.new_data_received_check.emit("硬件地址校验完成，开始数据读取...")
                self.confirmed_addresses_1 = [x + 1 for x in self.confirmed_addresses]
                for address in self.confirmed_addresses:
                    self.thread = threading.Thread(target=self.read_data, args=(address,),daemon=True)
                    self.thread.start()


    def stop_reading(self):
        print("Stopping I2C reading...")
        self.new_data_received_check.emit("停止 I2C 数据读取")
        self.running = False
        # if hasattr(self, 'thread') and self.thread.is_alive():
        #     self.thread.join()  

    def read_data(self,address):
        while self.running:
            line = self.read_until_end(address)
            if line:
                line_decoded = line.decode('utf-8', errors='replace').strip()
                print(f"Received line: {line_decoded}")
                self.data.append(line_decoded)
                self.parse_and_insert_data(line_decoded)
                self.parse_and_emit_signals(line_decoded)
        

    def read_until_end(self,address):
        buffer = bytearray()
        I2C_SLAVE = 0x0703 
        while self.running:
            try:
                with open(self.device, 'rb', buffering=0) as f:
                    fcntl.ioctl(f, I2C_SLAVE, address)
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
                time.sleep(0.01)

    def read_overtimedetect(self,address):
        buffer = bytearray()
        I2C_SLAVE = 0x0703 
        start_time = time.time()
        while self.running:
            try:
                with open(self.device, 'rb', buffering=0) as f:
                    fcntl.ioctl(f, I2C_SLAVE, address)
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
                    print(f"Failed to open I2C bus after {self.timeout_duration} seconds.")
                    break
                time.sleep(0.01)

    def write_data(self, data_to_send,address):
        if isinstance(data_to_send, str):
            if not data_to_send.endswith('\n'):
                data_to_send += "\n"
            with SMBus(self.bus) as bus:
                try:
                    self.clear_buffer(address)
                    for char in data_to_send:
                        bus.write_byte(address, ord(char))
                        time.sleep(0.01)
                except Exception as e:
                    print(f"Error sending data: {e}")
        else:
            print("Input must be a string")
            
    def clear_buffer(self, address):
        """
        清空 I2C 从机buffer
        """
        try:
            I2C_SLAVE = 0x0703
            with open(self.device, 'rb', buffering=0) as f:
                fcntl.ioctl(f, I2C_SLAVE, address)
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
        except IOError:
            pass  

    def verify_data(self, data: str, address, expected_data:str, retries: int = 3):
        retries_left = retries
        while retries_left > 0:
            line = self.read_overtimedetect(address)
            if line:
                line_decoded = line.decode('utf-8', errors='replace').strip()
                print(f"Received: {line_decoded}")
                if line_decoded == expected_data:
                    print("Data verified successfully!")
                    return True  # Data is valid and verified
                else:
                    print(f"Unexpected data: {line_decoded}. Retrying...")
                    self.write_data(data,address)
                    retries_left -= 1
                    time.sleep(0.01)
            else:
                retries_left -= 1
                time.sleep(0.01)
        print(f"Failed to verify data after {retries} attempts.")
        return False

                        
    def parse_and_emit_signals(self, line):
        # print(f"Parsing line: {line}")
        if 'SWF' in line:
            try:
                battery_number, frequency, real_imp, imag_imp = self.parse_swf_data(line)
                print(f"Emitting SWF signal with: {battery_number}, {frequency}, {real_imp}, {imag_imp}")
                self.new_data_received_SWF.emit(battery_number, frequency, real_imp, imag_imp)
            except (ValueError, IndexError) as e:
                print(f"Error parsing SWF data: {line}, Error: {e}")

        if 'EIS_data_packet_start' in line:
            # voltage = float(line.split("VOLTAGE_")[1].split("_EIS_data_packet_end")[0])
            
            cell_id = int(line.split('_')[0], 16)
            if '_A' in line:
                cell_id = cell_id
            elif '_B' in line:
                cell_id = cell_id + 1
            else:
                cell_id = None 
            
            segments = line.split(';')
            result = None
            closest_frequency = None
            closest_result = None
            min_diff = float('inf')  # Used to track the closest frequency difference from 1000Hz
            
            for segment in segments:
                parts = segment.split(',')
                for i, part in enumerate(parts):
                    if part.startswith('F'):
                        frequency = float(parts[i + 1])
                        if frequency == 1000.0:
                            # If 1000Hz is found, take the corresponding result
                            for j in range(i, -1, -1):
                                if parts[j].startswith('I'):
                                    result = float(parts[j - 1])
                                    break
                            break
                        elif 500 <= frequency <= 1500:
                            # If the frequency is between 900Hz and 1100Hz, check if it's closer to 1000Hz
                            diff = abs(frequency - 1000)
                            if diff < min_diff:
                                min_diff = diff
                                closest_frequency = frequency
                                for j in range(i, -1, -1):
                                    if parts[j].startswith('I'):
                                        closest_result = float(parts[j - 1])
                                        break
                if result is not None:
                    break
            #硬件地址转ID    
            cell_id = str(cell_id)
            cell_id = self.config["cell_id_dict"].get(cell_id)
            cell_id = int(cell_id)   #显示序号
            cell_id_true = 13*(self.port-1) + cell_id #实际序号
            # If 1000Hz was found and its result is available
            if result is not None:
                self.new_data_received_batterycellInfo.emit(cell_id, cell_id_true,result)
            # If 1000Hz was not found, but a frequency close to 1000Hz in the 900Hz-1100Hz range was found
            elif closest_frequency is not None:
                print(f"Warning: 1000Hz not found, using closest frequency {closest_frequency}Hz with value {closest_result}")
                self.new_data_received_batterycellInfo.emit(cell_id, closest_result)
            else:
                print("Error: Neither 1000Hz nor any frequency in the 500Hz to 1500Hz range found.")



    def parse_swf_data(self, line):
        try:
            # Remove prefix and split the main data section
            if line.startswith("Received line:"):
                line = line[len("Received line: "):].strip()
            
            # Extract battery number from the 0x-prefixed address
            battery_number = int(line.split('_')[0], 16)
            if '_A' in line:
                battery_number  = battery_number
            elif '_B' in line:
                battery_number  = battery_number + 1
            else:
                battery_number = None 

            battery_number = str(battery_number)
            battery_number = self.config["cell_id_dict"].get(battery_number)
            battery_number = int(battery_number)
            battery_number = 13*(self.port-1) + battery_number
            # Extract the frequency, real impedance, and imaginary impedance
            if "SWF" in line:
                freq_start = line.find("Freq") + len("Freq")
                freq_end = line.find("rea")
                frequency = float(line[freq_start:freq_end])

                rea_start = freq_end + len("rea")
                rea_end = line.find("image")
                real_imp = float(line[rea_start:rea_end])

                img_start = rea_end + len("image")
                img_end = line.find("_end")
                imag_imp = float(line[img_start:img_end])

                return battery_number, frequency, real_imp, imag_imp
            else:
                raise ValueError("Invalid SWF data format")
        except (ValueError, IndexError) as e:
            print(f"Error parsing SWF data from line: {line}, Error: {e}")
            raise

    def parse_and_insert_data(self, line: str):
        """
        Parses the incoming data line, creates EisMeasurement objects, and inserts them into the database.
        """

        if self.container_number is None or self.cluster_number is None or self.pack_number is None:
            print("Error: Container, Cluster, or Pack not selected.")
            return
    
        if "EIS_data_packet_start" in line:
            try:
                # Extract the voltage value
                voltage = float(line.split("VOLTAGE_")[1].split("_EIS_data_packet_end")[0])
                
                # Extract data points
                data_points = self.extract_data_points(line)

                # Cell ID (unique identifier for your device, like 0x28)
                addr_id = int(line.split('_')[0], 16)
                if '_A' in line:
                    addr_id  = addr_id
                elif '_B' in line:
                    addr_id  = addr_id + 1
                else:
                    addr_id = None 

                cell_id = str(addr_id)
                cell_id = self.config["cell_id_dict"].get(cell_id)
                cell_id = int(cell_id)
                cell_id = 13*(self.port-1) + cell_id
                # Insert the parsed measurements into the database
                self.insert_measurements(cell_id, addr_id, data_points, voltage)

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

    def insert_measurements(self, cell_id: int, addr_id, data_points: List[tuple], voltage: float):
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
                voltage=voltage,
                container_number=self.container_number,
                cluster_number=self.cluster_number,
                pack_number=self.pack_number
            )
            measurements.append(measurement)

        # Insert into database using Repository
        try:
            print(f"Inserting {len(measurements)} measurements for cell {cell_id}.")
            self.repo.insert_measurements(measurements)
            self.finish_list_addr.append(addr_id)
            self.finish_list_cell.append(cell_id)
            if Counter(self.finish_list_addr) == Counter(self.confirmed_addresses) + Counter(self.confirmed_addresses_1):
                self.new_data_received_finish_list.emit(self.finish_list_cell)
                self.new_data_received_check.emit("数据读取完成,AI智能分析中...")
            print("Data inserted successfully into eis_measurement.")
            
        except Exception as e:
            print(f"Error during data insertion: {e}") 


    def close(self):
        self.stop_reading()
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    
    address_list = [0x26, 0x27, 0x28]
    reader = I2CReader(bus_number=11)
    data = "SET_SweepStartFreq_To_10000"
    for address in address_list:
        reader.write_data(data,address)
