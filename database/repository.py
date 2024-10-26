import sqlite3
from typing import List
from entity import EisMeasurement
from datetime import datetime

DB_PATH = "eis.db"

def insert_measurements(measurements: List[EisMeasurement]):
    measurements = [(m.cell_id, int(m.creation_time.timestamp()), m.frequency, m.real_impedance, m.imag_impedance, m.voltage) for m in measurements]
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.executemany("""
        INSERT INTO eis_measurement (cell_id, creation_time, frequency, real_impedance, imag_impedance, voltage)
        VALUES (?, ?, ?, ?, ?, ?);
        """, measurements)
        connection.commit()
    finally:
        if connection:
            connection.close()

def get_cluster_latest_measurements(cluster_id: int, limit: int = 50) -> dict[int, List[EisMeasurement]]:
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        rows = cursor.execute("SELECT id from battery_cell WHERE cluster_id = ?;", (cluster_id,)).fetchall()

        cell_ids = [row[0] for row in rows]

        query = f"""
        SELECT *
        FROM (
            SELECT *, 
                ROW_NUMBER() OVER (PARTITION BY cell_id ORDER BY creation_time DESC) AS row_num
            FROM eis_measurement
            WHERE cell_id IN ({','.join(['?'] * len(cell_ids))})
        ) AS subquery
        WHERE row_num <= ?
        ORDER BY cell_id, creation_time DESC
        """
        
        cursor.execute(query, tuple(cell_ids) + (limit,))

        result = {}
        
        # Fetch all matching rows
        rows = cursor.fetchall()
        for row in rows:
            cell_id = row[1]
            measurement = EisMeasurement(
                cell_id=cell_id,
                creation_time=datetime.fromtimestamp(row[2]),
                frequency=row[3],
                real_impedance=row[4],
                imag_impedance=row[5],
                voltage=row[6]
            )
            if cell_id not in result:
                result[cell_id] = []
            result[cell_id].append(measurement)
        return result
    finally:
        if connection:
            connection.close()
    

def get_cell_measurements(cell_id: int, limit: int = 50) -> List[EisMeasurement]:
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM eis_measurement WHERE cell_id = ? ORDER BY creation_time DESC LIMIT ?;", (cell_id, limit))
        rows = cursor.fetchall()
        return [EisMeasurement(cell_id=row[1], creation_time=datetime.fromtimestamp(row[2]), frequency=row[3], real_impedance=row[4], imag_impedance=row[5], voltage=row[6]) for row in rows]
    finally:
        if connection:
            connection.close()