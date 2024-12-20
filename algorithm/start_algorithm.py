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
    def __init__(self,lists):
        super().__init__()
        self.repository = Repository()
        self.address = lists
        
    def start(self):
        """
        Start the algorithm in a separate thread and generate random data.
        """
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

    def generate_random_generated_info_data(self) -> List[Dict]:
        """
        Generate random generated info data.
        """
        # data = []
        # for cell_id in self.address:
        #     data.append(self.repository.get_cell_measurements(cell_id))
        # result = defaultdict(lambda: ([], []))  
        # for measurements in data:
        #     for measurement in measurements:
        #         cell_id = f"Battery{measurement.cell_id}"  
        #         result[cell_id][0].append(measurement.real_impedance)  
        #         result[cell_id][1].append(measurement.imag_impedance)  
        # result = dict(result)
        ##
        ##这里加入算法
        ##
        list = []
        print(self.address)
        for addr in self.address:  
            list.append({
                'measurement_id': random.randint(1, 100),
                'dispersion_rate': round(random.uniform(0.0, 1.0), 2),
                'temperature': round(random.uniform(15.0, 40.0), 2),
                'real_time_id': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Use current timestamp
                'cell_id':  addr,
                'sei_rate': round(random.uniform(0.0, 1.0), 2),
                'dendrites_rate': round(random.uniform(0.0, 1.0), 2),
                'electrolyte_rate': round(random.uniform(0.0, 1.0), 2),
                'polar_rate': round(random.uniform(0.0, 1.0), 2),
                'conduct_rate': round(random.uniform(0.0, 1.0), 2)
            })
        return list
        


        


            




