import sqlite3
from sqlite3 import Error
import logging


def create_connection(db_file: str) -> sqlite3.Connection:
    """create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    logging.info(f"Attempting to connect to sqlite database {db_file}.")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Database connection made.")
        return conn
    except sqlite3.Err as db_error:
        logging.error(f"Database connection failed. Error: {db_error}")
        quit()


def clear_table_data(conn: sqlite3.Connection):
    logging.warning("Clearing out database before import of data.")
    tables = ["Mission", "ParentObject", "SecondaryObject", "PrimaryObject", "Event"]
    for table in tables:
        sql = f"DELETE FROM {table}"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    logging.warning("Table data cleared.")


def execute_sql_statement(conn: sqlite3.Connection, sql: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def create_required_tables(conn: sqlite3.Connection) -> bool:
    sql = """
            CREATE TABLE IF NOT EXISTS "Event" (
            "id" integer PRIMARY KEY NOT NULL,
            "mission_id" integer(128) NOT NULL,
            "time" char(128) NOT NULL,
            "action" char(128) NOT NULL
            );
        """
    execute_sql_statement(conn, sql)

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
    execute_sql_statement(conn, sql)

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
    execute_sql_statement(conn, sql)

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
    execute_sql_statement(conn, sql)

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
    execute_sql_statement(conn, sql)
