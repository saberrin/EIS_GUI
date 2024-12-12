import requests
import random
from datetime import datetime, timedelta

# Create the transmit data request
request = {}

# Generate EisMeasurements
measurements = []
creation_time = datetime.now()
frequencies = [1000.0, 2000.0, 3000.0]

# 3 days
for _ in range(3):
    creation_time += timedelta(days=1)
    # 2 clusters
    for b in range(2):
        # 8 packs
        for c in range(8):
            # 52 cells
            for d in range(52):
                for frequency in frequencies:
                    measurement = {
                        "containerId": str(b + 1),
                        "clusterId": str(b + 1),
                        "packId": str(8 * b + c + 1),
                        "cellId": str(d + 1),
                        "temperature": random.uniform(10, 60),
                        "voltage": random.uniform(1, 10),
                        "frequency": frequency,
                        "realImpedance": random.uniform(100, 200),
                        "imaginaryImpedance": random.uniform(1, 10),
                        "creationTime": creation_time.isoformat() + 'Z'
                    }
                    measurements.append(measurement)

request["eisMeasurements"] = measurements

# Generate GeneratedRecords
generated_records = []
creation_time = datetime.now()

# 3 days
for _ in range(3):
    creation_time += timedelta(days=1)
    for b in range(2):
        for c in range(8):
            for d in range(52):
                record = {
                    "containerId": str(b + 1),
                    "clusterId": str(b + 1),
                    "packId": str(8 * b + c + 1),
                    "cellId": str(d + 1),
                    "temperature": random.uniform(10, 60),
                    "dispersionCoefficient": random.uniform(0.1, 0.9),
                    "seiParameter": random.randint(1, 10),
                    "dendritesParameter": random.randint(1, 10),
                    "electrolyteParameter": random.randint(1, 10),
                    "polarizationPotential": random.uniform(0.1, 0.9),
                    "conductivity": random.uniform(0.1, 0.9),
                    "creationTime": creation_time.isoformat() + 'Z'
                }
                generated_records.append(record)

request["generatedRecords"] = generated_records

# Generate PackMetricsRecords
pack_metrics_records = []
creation_time = datetime.now()

# 3 days
for _ in range(3):
    creation_time += timedelta(days=1)
    for b in range(2):
        for c in range(8):
            record = {
                "containerId": str(b + 1),
                "clusterId": str(b + 1),
                "packId": str(8 * b + c + 1),
                "dispersionCoefficient": random.uniform(0.1, 0.9),
                "safetyRate": random.uniform(0.1, 0.9),
                "creationTime": creation_time.isoformat() + 'Z'
            }
            pack_metrics_records.append(record)

request["packMetricsRecords"] = pack_metrics_records

# Send the request
url = "http://192.168.198.88:8080/api/v1/transmit-data"
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=request, headers=headers)

# Print the response status code
print(response.status_code)