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
import random
from collections import defaultdict
class StartAlgorithm(QObject):
    task_done = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.repository = Repository()
        
        
    def start(self,lists):
        """
        Start the algorithm in a separate thread and generate random data.
        """
        self.lists = lists
        thread = threading.Thread(target=self.start_analyzer, daemon=True)
        thread.start()
        time.sleep(0.1)  # Ensure the thread has enough time to start

    def start_analyzer(self):
        """
        Generate random data and insert it into the database.
        """
        battery_pack_data = self.generate_random_battery_pack_data()
        self.repository.insert_battery_pack(battery_pack_data)

        generated_info_data = self.generate_random_generated_info_data()
        self.repository.insert_generated_info(generated_info_data)
        self.task_done.emit(self.lists)

    def generate_random_battery_pack_data(self) -> List[Dict]:


        """
        Generate random battery pack data.
        """
        data = []
        for _ in range(10):  # Generate 10 random records
            data.append({
                'cluster_id': random.randint(1, 5),
                'description': f"Pack {random.randint(1, 1000)}",
                'dispersion_rate': round(random.uniform(0.0, 1.0), 2),
                'pack_saftety_rate': round(random.uniform(0.0, 1.0), 2),
                'real_time_id': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use current timestamp as real_time_id
            })
        return data

    # def generate_random_generated_info_data(self) -> List[Dict]:
    #     """
    #     Generate random generated info data.
    #     """
    #     data = []
    #     for cell_id in self.lists:
    #         data.append(self.repository.get_cell_measurements(cell_id))
    #     result = defaultdict(lambda: ([], []))  
    #     for measurements in data:
    #         for measurement in measurements:
    #             cell_id = f"Battery{measurement.cell_id}"  
    #             result[cell_id][0].append(measurement.real_impedance)  
    #             result[cell_id][1].append(measurement.imag_impedance)  
    #     result = dict(result)
    #     analyzer = EISAnalyzer(result)
    #     dispersion_rate = analyzer.calculate_dispersion(result)
        
    #     print(f"dispersion_rate:{dispersion_rate}")
    #     print(f"lists:{self.lists}")
    #     list = []
    #     for addr in self.lists:  
    #         list.append({
    #             'measurement_id': random.randint(1, 100),
    #             'dispersion_rate': dispersion_rate[f"Battery{addr}"],
    #             'temperature': round(random.uniform(15.0, 40.0), 2),
    #             'real_time_id': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Use current timestamp
    #             'cell_id':  addr,
    #             'sei_rate': round(random.uniform(0.0, 1.0), 2),
    #             'dendrites_rate': round(random.uniform(0.0, 1.0), 2),
    #             'electrolyte_rate': round(random.uniform(0.0, 1.0), 2),
    #             'polar_rate': round(random.uniform(0.0, 1.0), 2),
    #             'conduct_rate': round(random.uniform(0.0, 1.0), 2)
    #         })
    #     return list

    def generate_random_generated_info_data(self) -> List[Dict]:
        """
        Generate random generated info data, including temperature and other parameters.
        """
        
        data = []
        latest_temp_dict = {}
        for cell_id in self.lists:
            data.append(self.repository.get_cell_measurements(cell_id))
            latest_temp_dict[cell_id] = self.repository.get_latest_temperature(cell_id)

        result = defaultdict(lambda: ([], []))  # 用于存储电池的阻抗数据
        
        for measurements in data:
            for measurement in measurements:
                cell_id = f"Battery{measurement.cell_id}"  
                result[cell_id][0].append(measurement.real_impedance)  
                result[cell_id][1].append(measurement.imag_impedance) 
                

        result = dict(result)
        analyzer = EISAnalyzer(result)
        dispersion_rate = analyzer.calculate_dispersion(result)

        print(f"dispersion_rate:{dispersion_rate}")
        print(f"lists:{self.lists}")
        print(f"latest_temp_dict:{latest_temp_dict}")
        

        list = []
        last_temp = 25 #默认值
        for addr in self.lists:
            temperature = latest_temp_dict.get(addr)
            if temperature != None and temperature > 0:
                last_temp = temperature
                break
            
        for addr in self.lists:  
            # 基于从数据库获取的温度，生成随机温度
            temperature = latest_temp_dict.get(addr)
            if temperature == None or temperature < 0:
                temperature = round(random.uniform(last_temp - 0.5, last_temp + 0.5), 2)

            # 插入数据库所需的数据
            list.append({
                'measurement_id': random.randint(1, 100),
                'dispersion_rate': dispersion_rate.get(f"Battery{addr}", 0.0),  # 获取 dispersion_rate
                'temperature': temperature,  # 将计算得到的温度值传入
                'real_time_id': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 当前时间戳
                'cell_id': addr,  # 插入对应的 cell_id
                'sei_rate': round(random.uniform(0.0, 1.0), 2),
                'dendrites_rate': round(random.uniform(0.0, 1.0), 2),
                'electrolyte_rate': round(random.uniform(0.0, 1.0), 2),
                'polar_rate': round(random.uniform(0.0, 1.0), 2),
                'conduct_rate': round(random.uniform(0.0, 1.0), 2)
            })
        
        return list


        


        


            




