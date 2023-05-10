#!/usr/bin/python

import sqlite3
from sqlite3 import Error
import logging


def create_connection(db_file: str) -> sqlite3.Connection:
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    logging.info(f'Attempting to connect to sqlite database {db_file}.')
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info('Database connection made.')
        return conn
    except sqlite3.Err as db_error:
        logging.error(f'Database connection failed. Error: {db_error}')
        quit()


def check_mission_exists(conn: sqlite3.Connection, mission) -> bool:
    logging.info(f'Checking if {mission[0]} already in database.')

    cursor = conn.cursor()

    sql = ''' SELECT * FROM Mission WHERE name = ? '''

    # Execute query and commit to the db.
    result = cursor.execute(sql, (mission[0],))

    if result.fetchone():
        return True
    else:
        return False


def create_mission_record(conn: sqlite3.Connection, mission):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    logging.info(f'Attempting to add mission named {mission[0]} to database.')

    cursor = conn.cursor()

    sql = ''' INSERT INTO Mission(name,date,duration, source, recorder, recording_time, author)
							VALUES(?,?,?,?,?,?,?) '''

    # Execute query and commit to the db.
    cursor.execute(sql, mission)
    conn.commit()

    logging.info(f'Created mission in database.')

    # Return the id of the newly created Mission record.
    return cursor.lastrowid


def create_event_record(conn: sqlite3.Connection, event):
    """
    Create a new event record
    :param conn:
    :param event:
    :return:
    """

    sql = ''' INSERT INTO Event(mission_id,time,action)
							VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()
    return cur.lastrowid


def create_primary_record(conn, primary):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO PrimaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
							VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, primary)
    conn.commit()
    return cur.lastrowid


def create_secondary_record(conn: sqlite3.Connection, secondary):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO SecondaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
						VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, secondary)
    conn.commit()
    return cur.lastrowid


def create_parent_record(conn: sqlite3.Connection, parent):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO ParentObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group)
						VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, parent)
    conn.commit()
    return cur.lastrowid


def clear_table_data(conn):
    logging.warning('Clearing out database before import of data.')
    tables = ['Mission', 'ParentObject',
              'SecondaryObject', 'PrimaryObject', 'Event']
    for table in tables:
        sql = f'DELETE FROM {table}'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    logging.warning('Table data cleared.')
