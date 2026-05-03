import sqlite3
import json
import os

DB_PATH = os.path.join("db", "geo.db")

class GeoStorage:

    def __init__(self):
        os.makedirs("db", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL,
            geo_data TEXT,
            nasa_data TEXT
        )
        """)

        self.conn.commit()

    def save_scan(self, lat, lon, geo_data, nasa_data):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO scans (lat, lon, geo_data, nasa_data)
        VALUES (?, ?, ?, ?)
        """, (
            lat,
            lon,
            json.dumps(geo_data),
            json.dumps(nasa_data)
        ))

        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM scans")

        return cursor.fetchall()
