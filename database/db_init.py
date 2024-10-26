import sqlite3

def init_database():
    try:
        connection = sqlite3.connect("eis.db")
        cursor = connection.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE if not exists container (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "location" TEXT,
            "description" TEXT
            )
        """)
        cursor.execute("""
        CREATE TABLE if not exists battery_cabinet (
            "id" integer PRIMARY KEY AUTOINCREMENT,
            "container_id" integer,
            "description" text
            )
        """)
        cursor.execute("""
        CREATE TABLE if not exists battery_cluster (
            "id" integer PRIMARY KEY AUTOINCREMENT,
            "cabinet_id" integer,
            "description" TEXT
            )
        """)
        cursor.execute("""
        CREATE TABLE if not exists battery_cell (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "cluster_id" integer,
            "serial_number" text,
            "description" text
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cell_cluster_id ON battery_cell(cluster_id)")
        cursor.execute("""
        CREATE TABLE if not exists eis_measurement (
            "id" integer PRIMARY KEY AUTOINCREMENT,
            "cell_id" integer,
            "creation_time" integer,
            "frequency" real,
            "real_impedance" real,
            "imag_impedance" real,
            "voltage" real
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cell_id_creation_time ON eis_measurement(cell_id, creation_time)")

        # Commit the changes and close the connection
        connection.commit()
    finally:
        if connection:
            connection.close()