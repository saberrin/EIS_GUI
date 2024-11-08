from PyQt6.QtCore import QObject, pyqtSignal
# import smbus2
import sqlite3
from datetime import datetime
import fcntl
import time
import threading
from smbus2 import SMBus
import re

class I2CReader(QObject):
    new_data_received_UIT = pyqtSignal(int, float, float, float)
    new_data_received_SWF = pyqtSignal(int, float, float, float)
    new_data_received_check = pyqtSignal(str)

    def __init__(self, device, bus_number,address):
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
        
        # Initialize SQLite database connection
        try:
            self.connection = sqlite3.connect("bms01.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS eis_001 (
                    real_imp REAL,
                    imag_imp REAL,
                    frequency REAL,
                    temperature REAL,
                    voltage REAL,
                    real_time_id TEXT
                )
            """)
            self.connection.commit()
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
        # self.thread_write = threading.Thread(target=self.write_data, daemon=True)       
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

                # 检查数据地址是否正确
                    if not line_decoded.startswith(self.address):
                        match = re.search(r"0x[0-9A-Fa-f]+_Received I2C_Command_(.+?)_end", line_decoded)
                        if match:
                            command_to_resend = match.group(1)
                            print(f"Incorrect address in line: {line_decoded}. Resending command: {command_to_resend}")
                            self.write_data(f"{command_to_resend}\n")  
                        else:
                            print(f"Format error in line: {line_decoded}")
                        continue  

                    print(f"Received line: {line_decoded}")
                    self.data.append(line_decoded)
                    # self.parse_and_emit_signals(line_decoded)
                    # self.parse_and_insert_data(line_decoded)
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
                            print("No more data available from device.")
                            break

                        buffer.extend(chunk)

                        if self.line_ending in buffer:
                            line_end_index = buffer.index(self.line_ending) + len(self.line_ending)
                            line = buffer[:line_end_index]
                            del buffer[:line_end_index]
                            # print("Line received:", line.decode('utf-8').strip()) 
                            return line     
            except IOError as e:
                # print(f"Error: {e}")
                time.sleep(0.01)  
                

    def write_data(self,data_to_send):
        if isinstance(data_to_send, str):
            if not (data_to_send.endswith('\n')):
                data_to_send = data_to_send + "\n"
            with SMBus(self.bus) as bus:  
                try:                                                                            
                    for char in data_to_send:
                        bus.write_byte(self.address, ord(char))
                        print(f"Sent: 0x{ord(char):X} ('{char}')")
                        time.sleep(0.1) 
                except Exception as e:
                        print(f"Error sending data: {e}")
        else:
            print("Input must be a string")

    def parse_and_emit_signals(self, line):
        print(f"Parsing line: {line}")
        if 'QGKJ_DATA_UIT' in line:
            try:
                battery_number, voltage, current, temperature = self.parse_uit_data(line)
                print(f"Emitting UIT signal with: {battery_number}, {voltage}, {current}, {temperature}")
                self.new_data_received_UIT.emit(battery_number, voltage, current, temperature)
            except (ValueError, IndexError) as e:
                print(f"Error parsing UIT data: {line}, Error: {e}")
        elif 'QGKJ_DATA_SWF' in line:
            try:
                battery_number, frequency, real_imp, imag_imp = self.parse_swf_data(line)
                print(f"Emitting SWF signal with: {battery_number}, {frequency}, {real_imp}, {imag_imp}")
                self.new_data_received_SWF.emit(battery_number, frequency, real_imp, imag_imp)
            except (ValueError, IndexError) as e:
                print(f"Error parsing SWF data: {line}, Error: {e}")
        elif 'RcalVolt' in line:
            self.new_data_received_check.emit(line)

    def parse_uit_data(self, line):
        parts = line.split('_')
        if len(parts) >= 4: 
            battery_number = int(parts[3].split('@')[1])
            voltage = float(parts[4].split('U')[1])
            current = float(parts[5].split('I')[1])
            temperature = float(parts[6].split('T')[1].split('_end')[0])
            self.voltage = voltage
            return battery_number, voltage, current, temperature
        raise ValueError("Invalid UIT data format")

    def parse_swf_data(self, line):
        parts = line.split('_')
        if len(parts) >= 4:
            battery_number = int(parts[3].split('@')[1])
            freq = float(parts[4].split('Freq')[1].split('rea')[0])
            real_imp = float(parts[4].split('rea')[1].split('image')[0])
            imag_imp = float(parts[4].split('image')[1].split('_end')[0])
            return battery_number, freq, real_imp, imag_imp
        raise ValueError("Invalid SWF data format")

    def parse_and_insert_data(self, line):
        if 'QGKJ_DATA_UIT' in line:
            if '_T' in line and '_end' in line:
                self.temperature = float(line.split('_T')[1].split('_end')[0])
            if 'U' in line and '_end' in line:
                self.voltage = float(line.split('1_U')[1].split('_I')[0])

        elif 'QGKJ_DATA_SWF' in line and self.temperature is not None:
            try:
                frequency = float(line.split('Freq')[1].split('rea')[0])
                real_imp = float(line.split('rea')[1].split('image')[0])
                imag_imp = float(line.split('image')[1].split('_end')[0])
                real_time_id = datetime.now()

                self.insert_data(real_imp, imag_imp, frequency, self.temperature, real_time_id, self.voltage)
            except (ValueError, IndexError) as e:
                print(f"Error parsing SWF data: {line}, Error: {e}")

    def insert_data(self, real_imp, imag_imp, frequency, temperature, real_time_id, voltage):
        if self.connection is None:
            print("Database connection is not available. Data insertion aborted.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO eis_001 (real_imp, imag_imp, frequency, temperature, voltage, real_time_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (real_imp, imag_imp, frequency, temperature, voltage, real_time_id))
            self.connection.commit()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()     
