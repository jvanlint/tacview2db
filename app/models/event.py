import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import logging


class Event:
    id: int
    time: str
    action: str

    def __init__(self, xml_tree):
        self.time = xml_tree.find("Time").text
        self.action = xml_tree.find("Action").text

    def write_to_db(self, conn, mission_id):
        sql = """ INSERT INTO Event(mission_id,time,action)
							VALUES(?,?,?) """

        cursor = conn.cursor()
        db_values = (
            mission_id,
            self.time,
            self.action,
        )
        # Execute query and commit to the db.
        cursor.execute(sql, db_values)
        conn.commit()
        self.id = cursor.lastrowid

        return cursor.lastrowid
