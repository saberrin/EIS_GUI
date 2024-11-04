import random
import sqlite3
from typing import List
from datetime import datetime, timedelta
from entity import EisMeasurement
from repository import insert_measurements
from db_init import init_database
from repository import get_cluster_latest_measurements

DB_PATH = "eis.db"
def generate_random_measurements(num_samples: int) -> List[EisMeasurement]:
    measurements = []
    for _ in range(num_samples):
        cell_id = random.randint(1, 100)  # 随机生成单元 ID
        creation_time = datetime.now() - timedelta(days=random.randint(0, 10))  # 随机生成创建时间（过去 10 天内）
        frequency = random.uniform(1e3, 1e6)  # 随机生成频率 (1 kHz 到 1 MHz)
        real_impedance = random.uniform(0, 100)  # 随机生成实部阻抗
        imag_impedance = random.uniform(-50, 50)  # 随机生成虚部阻抗
        voltage = random.uniform(0, 5)  # 随机生成电压
        measurements.append(EisMeasurement(cell_id, creation_time, frequency, real_impedance, imag_impedance, voltage))
    return measurements

def fetch_measurements():
    try:
        # 连接到数据库
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        # 执行查询
        cursor.execute("SELECT * FROM eis_measurement;")
        rows = cursor.fetchall()  # 获取所有结果
        
        # 打印结果
        for row in rows:
            print(row)  # 或者根据需要格式化输出

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()  # 确保连接关闭
if __name__ == "__main__":
    init_database()
    random_measurements = generate_random_measurements(10)  # 生成 10 个随机测量数据
    insert_measurements(random_measurements)  # 插入数据到数据库
    # fetch_measurements()  # 查询并打印测量数据
    get_cluster_latest_measurements(0)