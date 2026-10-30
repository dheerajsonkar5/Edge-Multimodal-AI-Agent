"""
database/schema.py

Creates the SQLite database schema for
Edge Multimodal AI Agent.
"""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path("database/workspace.db")


class DatabaseSchema:

    def __init__(self):

        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.cursor = self.connection.cursor()

    def create_tables(self):

        # -------------------------------
        # Security Events
        # -------------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            event_type TEXT,

            confidence REAL,

            camera_id INTEGER,

            image_path TEXT,

            description TEXT

        )
        """)

        # -------------------------------
        # Generated Reports
        # -------------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_name TEXT,

            created_at TEXT,

            report_path TEXT

        )
        """)

        # -------------------------------
        # Application Settings
        # -------------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            setting_key TEXT UNIQUE,

            setting_value TEXT

        )
        """)

        self.connection.commit()

    def close(self):

        self.connection.close()


if __name__ == "__main__":

    db = DatabaseSchema()

    db.create_tables()

    db.close()

    print("Database schema created successfully.")