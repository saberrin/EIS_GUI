import sqlite3
from config import DB_PATH

def init_database():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Create tables with foreign key constraints
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS container (
            "container_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "location" TEXT,
            "description" TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS battery_cabinet (
            "cabinet_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "container_id" INTEGER,
            "description" TEXT,
            CONSTRAINT "fk_cabinet_container" FOREIGN KEY ("container_id") REFERENCES "container" ("container_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS battery_cluster (
            "cluster_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "cabinet_id" INTEGER,
            "description" TEXT,
            CONSTRAINT "fk_cluster_cabinet" FOREIGN KEY ("cabinet_id") REFERENCES "battery_cabinet" ("cabinet_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS battery_cell (
            "cell_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "cluster_id" INTEGER,
            "serial_number" TEXT,
            "description" TEXT,
            CONSTRAINT "fk_cell_cluster" FOREIGN KEY ("cluster_id") REFERENCES "battery_cluster" ("cluster_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cell_cluster_id ON battery_cell(cluster_id)")

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
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cell_id_creation_time ON eis_measurement(cell_id, creation_time)")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_info (
            "generated_info_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "measurement_id" INTEGER,
            "coefficient_of_variation" REAL,
            "predicted_temperature" REAL,
            "real_time_id" TEXT,
            CONSTRAINT "fk_info_measurement" FOREIGN KEY ("measurement_id") REFERENCES "eis_measurement" ("measurement_id") ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        """)

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
