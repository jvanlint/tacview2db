import sqlite3
from sqlite3 import Error
import logging


class Database:
    conn: sqlite3.Connection

    def __init__(self, database_file: str) -> None:
        logging.info(f"Attempting to connect to sqlite database {database_file}.")
        try:
            self.conn = sqlite3.connect(database_file)
            logging.info("Database connection made.")
        except sqlite3.Err as db_error:
            logging.error(f"Database connection failed. Error: {db_error}")
            quit()

    def clear_table_data(self):
        logging.warning("Clearing out database before import of data.")
        tables = [
            "Mission",
            "ParentObject",
            "SecondaryObject",
            "PrimaryObject",
            "Event",
        ]
        cursor = self.conn.cursor()
        for table in tables:
            sql = f"DELETE FROM {table}"
            cursor.execute(sql)
            self.conn.commit()
        logging.warning("Table data cleared.")

    def execute_sql_statement(self, sql: str) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except:
            logging.error("SQL statement issue.")
