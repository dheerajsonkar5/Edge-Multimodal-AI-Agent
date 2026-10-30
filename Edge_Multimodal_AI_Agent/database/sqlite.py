import sqlite3
from pathlib import Path
from datetime import datetime

from core.logger import logger


class Database:

    def __init__(self):

        self.db_path = Path("workspace.db")

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            faces INTEGER,

            persons INTEGER,

            eyes INTEGER,

            objects INTEGER,

            posture TEXT,

            alert TEXT

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            report TEXT
        )
        """)

        self.connection.commit()

        logger.info("Database initialized.")

    def insert_monitor_log(
        self,
        faces,
        persons,
        eyes,
        objects,
        posture,
        alert
    ):

        self.cursor.execute("""

        INSERT INTO monitoring_logs(

        timestamp,

        faces,

        persons,

        eyes,

        objects,

        posture,

        alert

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            faces,

            persons,

            eyes,

            objects,

            posture,

            alert

        )

        )

        self.connection.commit()

    def insert_report(self, report):

        self.cursor.execute("""

        INSERT INTO reports(

        timestamp,

        report

        )

        VALUES(?,?)

        """,

        (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            report

        )

        )

        self.connection.commit()

    def get_reports(self):

        self.cursor.execute("""

        SELECT *

        FROM reports

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    def get_monitor_logs(self):

        self.cursor.execute("""

        SELECT *

        FROM monitoring_logs

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()

        logger.info("Database Closed")