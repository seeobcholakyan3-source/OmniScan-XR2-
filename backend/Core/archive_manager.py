# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
# ==============================================================================

import os
import sqlite3
from cryptography.fernet import Fernet

class SecureArchive:
    def __init__(self):
        key_str = os.getenv("HIT_ENCRYPTION_KEY")
        if not key_str:
            self.key = Fernet.generate_key()
        else:
            self.key = key_str.encode()

        self.cipher = Fernet(self.key)
        self.db_path = os.path.join(os.path.dirname(__file__), 'exploration.db')
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS hits
                         (id INTEGER PRIMARY KEY, encrypted_coords TEXT, mineral TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def log_hit(self, lat, lon, mineral):
        coords = f"{lat},{lon}"
        encrypted = self.cipher.encrypt(coords.encode()).decode()
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO hits (encrypted_coords, mineral) VALUES (?, ?)", (encrypted, mineral))
        conn.commit()
        conn.close()
