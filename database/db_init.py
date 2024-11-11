
import sqlite3
from database.config import DB_PATH  
import os

def init_database():
    try:
        
        
        # Connect to the SQLite database
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Create the container table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS container (
            "container_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "location" TEXT,
            "description" TEXT
        );
        """)
        
        # Create the battery_cluster table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS battery_cluster (
            "cluster_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "container_id" INTEGER,
            "description" TEXT,
            CONSTRAINT "fk_cabinet_container" FOREIGN KEY ("container_id") REFERENCES "container" ("container_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)

        # Create the battery_pack table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS battery_pack (
            "pack_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "cluster_id" INTEGER,
            "description" TEXT,
            "dispersion_rate" REAL,
            "pack_saftety_rate" REAL,
            "real_time_id" TEXT,
            CONSTRAINT "fk_pack_cluster" FOREIGN KEY ("cluster_id") REFERENCES "battery_cluster" ("cluster_id") ON DELETE SET NULL ON UPDATE CASCADE
        );
        """)

        # Create the eis_measurement table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eis_measurement (
            "measurement_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "cell_id" INTEGER,
            "real_time_id" TEXT,
            "frequency" REAL,
            "real_impedance" REAL,
            "imag_impedance" REAL,
            "voltage" REAL,
            CONSTRAINT "fk_measurement_cell" FOREIGN KEY ("cell_id") REFERENCES "battery_cell" ("cell_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cell_id_creation_time ON eis_measurement(cell_id, real_time_id)")

        # Create the generated_info table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_info (
            "generated_info_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "measurement_id" INTEGER,
            "dispersion_rate" REAL,
            "temperature" REAL,
            "real_time_id" TEXT,
            "cell_id" INTEGER,
            "sei_rate" INTEGER,
            "dendrites_rate" INTEGER,
            "electrolyte_rate" INTEGER,
            "polar_rate" REAL,
            "conduct_rate" REAL,
            CONSTRAINT "fk_info_measurement" FOREIGN KEY ("measurement_id") REFERENCES "eis_measurement" ("measurement_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)

        # Create indexes to optimize search queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_measurement_cell ON eis_measurement(cell_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_info_measurement ON generated_info(measurement_id);")

        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Commit the changes
        connection.commit()
        print("Database initialized successfully.")
        
        # Return the connection and cursor for further use
        return connection, cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None, None
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# Example usage
if __name__ == "__main__":
    init_database()
