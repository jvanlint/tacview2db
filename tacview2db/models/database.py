import sqlite3
from sqlite3 import Error
import logging


class Database:
    conn: sqlite3.Connection

    def __init__(self, database_file: str) -> None:
        logging.info(f"Attempting to connect to database {database_file}.")
        try:
            self.conn = sqlite3.connect(database_file)
            logging.info("Database connection made.")
        except sqlite3.Err as db_error:
            logging.error(f"Database connection failed. Error: {db_error}")
            quit()

    def close_connection(self):
        self.conn.close

    def clear_table_data(self):
        logging.warning("Clearing out database before import of tacview data.")
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

    def execute_sql_statement(self, sql: str, data=()) -> bool:
        cursor = self.conn.cursor()
        try:
            if data:
                cursor.execute(sql, data)
                self.conn.commit()
                return cursor.lastrowid
            else:
                cursor.execute(sql)
                self.conn.commit()
                return cursor.fetchone()
        except:
            logging.error("SQL statement issue.")

    def create_required_tables() -> bool:
        sql = """
                CREATE TABLE IF NOT EXISTS "Event" (
                "id" integer PRIMARY KEY NOT NULL,
                "mission_id" integer(128) NOT NULL,
                "time" char(128) NOT NULL,
                "action" char(128) NOT NULL
                );
            """
        self.execute_sql_statement(sql)

        sql = """ 
                CREATE TABLE IF NOT EXISTS "Mission" (
                "id" integer PRIMARY KEY NOT NULL,
                "name" char(128),
                "date" char(128),
                "duration" char(128),
                "source" char(128),
                "recorder" char(128),
                "recording_time" char(128),
                "author" char(128)
                );
            """
        self.execute_sql_statement(sql)

        sql = """
                CREATE TABLE IF NOT EXISTS "ParentObject" (
                "id" integer PRIMARY KEY NOT NULL,
                "event_id" integer(128) NOT NULL,
                "tacview_id" char(128) NOT NULL,
                "type" char(128),
                "name" char(128),
                "pilot" char(128),
                "coalition" char(128),
                "country" char(128),
                "obj_group" char(128)
                );
            """
        self.execute_sql_statement(sql)

        sql = """
                CREATE TABLE IF NOT EXISTS "PrimaryObject" (
                "id" integer PRIMARY KEY NOT NULL,
                "event_id" integer(128) NOT NULL,
                "tacview_id" char(128) NOT NULL,
                "type" char(128),
                "name" char(128),
                "pilot" char(128),
                "coalition" char(128),
                "country" char(128),
                "obj_group" char(128),
                "parent_id" char(128)
                );
            """
        self.execute_sql_statement(sql)

        sql = """
                CREATE TABLE IF NOT EXISTS "SecondaryObject" (
                "id" integer PRIMARY KEY NOT NULL,
                "event_id" integer(128) NOT NULL,
                "tacview_id" char(128) NOT NULL,
                "type" char(128),
                "name" char(128),
                "pilot" char(128),
                "coalition" char(128),
                "country" char(128),
                "obj_group" char(128),
                "parent_id" char(128)
                );
            """
        self.execute_sql_statement(sql)
