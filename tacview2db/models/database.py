import sqlite3
import logging


class Database:
    """
    Database class to manage SQLite database connections and operations for tacview data.
    Handles database initialization, queries, and table management.
    """
    conn: sqlite3.Connection

    def __init__(self, database_file: str) -> None:
        """
        Initialize database connection with the provided file path.
        
        Args:
            database_file (str): Path to the SQLite database file
        """
        logging.info(f"Attempting to connect to database {database_file}.")
        try:
            self.conn = sqlite3.connect(database_file)
            logging.info("Database connection made.")
        except sqlite3.Error as db_error:
            logging.error(f"Database connection failed. Error: {db_error}")
            quit()

    def close_connection(self):
        """
        Close the database connection.
        """
        self.conn.close()
 
    def clear_table_data(self):
        """
        Clear all data from the database tables before importing new tacview data.
        Tables are cleared in a specific order to respect foreign key constraints.
        """
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
            # self.conn.commit()
            logging.warning(f"Table {table} cleared.")
        logging.warning("All table data cleared.")

    def execute_sql_select_query(self, sql: str):
        """
        Execute a SQL SELECT query and return the first result.
        
        Args:
            sql (str): SQL SELECT query to execute
            
        Returns:
            The first row of the query result or None if error occurs
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchone()

        except Exception as e:
            logging.error(f"SQL statement issue: {e}")

    def execute_sql_statement(self, sql: str, data=()) -> bool:
        """
        Execute a generic SQL statement with optional parameter binding.
        
        Args:
            sql (str): SQL statement to execute
            data (tuple): Optional data parameters for the SQL statement
            
        Returns:
            For INSERT statements: the row ID of the inserted row
            For other statements: the first row of results or None if error occurs
        """
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
        except Exception as e:
            logging.error(f"SQL statement issue: {e}")

    # This code unused and also doesn't seem to work
    def create_required_tables(self) -> bool:
        """
        Create the required database tables if they don't already exist.
        Note: This function is currently unused and may have issues.
        
        Returns:
            bool: True if successful (implied, function doesn't actually return a value)
        """
        # Create Event table
        sql = """
                CREATE TABLE IF NOT EXISTS "Event" (
                "id" integer PRIMARY KEY NOT NULL,
                "mission_id" integer(128) NOT NULL,
                "time" char(128) NOT NULL,
                "action" char(128) NOT NULL
                );
            """
        self.execute_sql_statement(sql)

        # Create Mission table
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

        # Create ParentObject table
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

        # Create PrimaryObject table
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

        # Create SecondaryObject table
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
