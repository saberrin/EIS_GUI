import sqlite3
import requests
import os
import sys
import json

from datetime import datetime

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 将项目根目录添加到 Python 模块搜索路径
sys.path.insert(0, BASE_DIR)

from database.config import DB_PATH  # 从 database.config 导入 DB_PATH

# 获取EIS数据
def get_eis_data_from_db():
    try:
        # 连接到SQLite数据库
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # 查询eis_measurement表中的数据
        query = """
        SELECT measurement_id, cell_id, real_time_id, frequency, real_impedance, imag_impedance, voltage,
               container_number, cluster_number, pack_number
        FROM eis_measurement
        ORDER BY real_time_id DESC
        LIMIT 000
        
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if connection:
            connection.close()

# 格式化数据为API请求所需的格式
def format_data(rows):
    measurements = []
    generated_records = []
    pack_metrics_records = []

    for row in rows:
        (measurement_id, cell_id, real_time_id, frequency, real_imp, imag_imp, voltage,
         container_number, cluster_number, pack_number) = row

        # 将 real_time_id 转换为 datetime 对象
        creation_time = datetime.strptime(real_time_id, "%Y-%m-%d %H:%M:%S")

        measurement = {
            "containerId": str(container_number),
            "clusterId": str(cluster_number),
            "packId": str(pack_number),
            "cellId": str(cell_id),
            "temperature": 25.0,  # 如果有温度数据，可以从数据库中获取，否则设置一个默认值
            "voltage": voltage,
            "frequency": frequency,
            "realImpedance": real_imp,
            "imaginaryImpedance": imag_imp,
            "creationTime": creation_time.isoformat() + 'Z'
        }
        measurements.append(measurement)

        # 生成的记录（根据需求填写实际数据或从数据库获取）
        generated_record = {
            "containerId": str(container_number),
            "clusterId": str(cluster_number),
            "packId": str(pack_number),
            "cellId": str(cell_id),
            "temperature": 25.0,  # 如果有温度数据，可以从数据库中获取，否则设置一个默认值
            "dispersionCoefficient": 0.5,  # 根据实际数据填写
            "seiParameter": 5,             # 根据实际数据填写
            "dendritesParameter": 5,       # 根据实际数据填写
            "electrolyteParameter": 5,     # 根据实际数据填写
            "polarizationPotential": 0.5,  # 根据实际数据填写
            "conductivity": 0.5,           # 根据实际数据填写
            "creationTime": creation_time.isoformat() + 'Z'
        }
        generated_records.append(generated_record)

        # 包的度量记录（根据需求填写实际数据或从数据库获取）
        pack_metrics_record = {
            "containerId": str(container_number),
            "clusterId": str(cluster_number),
            "packId": str(pack_number),
            "dispersionCoefficient": 0.5,  # 根据实际数据填写
            "safetyRate": 0.5,             # 根据实际数据填写
            "creationTime": creation_time.isoformat() + 'Z'
        }
        pack_metrics_records.append(pack_metrics_record)

    return {
        "eisMeasurements": measurements,
        "generatedRecords": generated_records,
        "packMetricsRecords": pack_metrics_records
    }

# 发送数据到Docker服务器
def send_data_to_docker(data):
    url = "http://192.168.98.104:8080/api/v1/transmit-data"
    headers = {"Content-Type": "application/json"}

    try:
        print(f"Sending {len(data['eisMeasurements'])} records to server...")
        # 可选：打印发送的数据进行调试
        print(json.dumps(data, indent=4, ensure_ascii=False))
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:  # 接受 200 和 201 作为成功
            print(f"Data sent successfully. Status code: {response.status_code}")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response content: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")



# 主函数
def main():
    # 从数据库获取数据
    eis_data = get_eis_data_from_db()

    if not eis_data:
        print("No data found in the database.")
        return

    # 格式化数据
    request_data = format_data(eis_data)

    # 发送数据到Docker服务器
    send_data_to_docker(request_data)

if __name__ == "__main__":
    main()
