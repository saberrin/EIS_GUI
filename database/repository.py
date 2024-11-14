import sqlite3
from typing import List, Dict
from database.entity import EisMeasurement
from datetime import datetime
from database.config import DB_PATH

class Repository:
    def __init__(self):
        super().__init__()
        # self.connection = sqlite3.connect(DB_PATH)
        # self.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        # self.cursor = self.connection.cursor()



    def insert_measurements(self, measurements: List[EisMeasurement]):
        """
        Insert multiple measurements into the database.
        """
        try:
            # Confirm that the table exists
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eis_measurement'")
            if not cursor.fetchone():
                print("Table 'eis_measurement' does not exist.")
                return
        
            cursor.executemany("""
            INSERT INTO eis_measurement (cell_id, real_time_id, frequency, real_impedance, imag_impedance, voltage, 
                                         container_number, cluster_number, pack_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (m.cell_id, m.real_time_id, m.frequency, m.real_impedance, m.imag_impedance, m.voltage,
             m.container_number, m.cluster_number, m.pack_number)
            for m in measurements
        ])
            connection.commit()
            print("Measurements inserted successfully.")
        except Exception as e:
            print(f"Error inserting measurements: {e}")
            connection.rollback()


    def insert_generated_info(self, generated_info_list: List[Dict]):
        """
        Inserts generated info data into the database.
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.executemany("""
                INSERT INTO generated_info (measurement_id, dispersion_rate, temperature, real_time_id, cell_id,
                                            sei_rate, dendrites_rate, electrolyte_rate, polar_rate, conduct_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, generated_info_list)
            connection.commit()
        finally:
            if connection:
                connection.close()

    def get_battery_pack_info(self, cluster_id: int, limit: int = 10) -> List[dict]:
        """
        Fetches the latest information for all battery packs within a given cluster.
        
        Returns a list of dictionaries containing information about each battery pack.
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            # rows = cursor.execute("SELECT id from battery_cell WHERE cluster_id = ?;", (cluster_id,)).fetchall()
            # cursor = self.connection.cursor()
            # Fetch data from battery_pack table based on cluster_id
            cursor.execute("""
                SELECT pack_id, cluster_id, description, dispersion_rate, pack_saftety_rate, real_time_id
                FROM battery_pack
                WHERE cluster_id = ?
                ORDER BY real_time_id DESC
                LIMIT ?;
            """, (cluster_id, limit))
            
            rows = cursor.fetchall()

            # Convert the rows into a list of dictionaries for easier access
            result = [
                {
                    "pack_id": row[0],
                    "cluster_id": row[1],
                    "description": row[2],
                    "dispersion_rate": row[3],
                    "pack_saftety_rate": row[4],
                    "real_time_id": row[5]
                }
                for row in rows
            ]
            return result

        finally:
            if connection:
                connection.close()


    def get_cell_measurements(self, cell_id: int, limit: int = 50) -> List[EisMeasurement]:
        """
        Fetches the latest measurements for a specific cell.
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            # cursor.execute("SELECT * FROM eis_measurement WHERE cell_id = ? ORDER BY creation_time DESC LIMIT ?;", (cell_id, limit))
            # cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM eis_measurement 
                WHERE cell_id = ? 
                ORDER BY real_time_id DESC 
                LIMIT ?;
            """, (cell_id, limit))
            rows = cursor.fetchall()
            return [
                EisMeasurement(
                    cell_id=row[1], 
                    real_time_id=row[2], 
                    frequency=row[3], 
                    real_impedance=row[4], 
                    imag_impedance=row[5], 
                    voltage=row[6]
                ) for row in rows
            ]
        finally:
            if connection:
                connection.close()