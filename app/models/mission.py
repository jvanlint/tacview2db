import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import logging


class Mission:
    id: int
    name: str
    time: str
    duration: str
    source: str
    recorder: str
    recordingTime: str
    author: str

    def __init__(self, xml_tree: ET):
        self.name = xml_tree[1][0].text
        self.time = xml_tree[1][1].text
        self.duration = xml_tree[1][2].text
        self.source = xml_tree[0][0].text
        self.recorder = xml_tree[0][1].text
        self.recordingTime = xml_tree[0][2].text
        self.author = xml_tree[0][3].text

    def write_to_db(self, conn: sqlite3.Connection):
        logging.info(f"Attempting to add mission named {self.name} to database.")

        cursor = conn.cursor()

        sql = """ INSERT INTO Mission(name,date,duration, source, recorder, recording_time, author)
                                VALUES(?,?,?,?,?,?,?) """
        db_values = (
            self.name,
            self.time,
            self.duration,
            self.source,
            self.recorder,
            self.recordingTime,
            self.author,
        )
        # Execute query and commit to the db.
        cursor.execute(sql, db_values)
        conn.commit()

        logging.info(f"Created mission in database.")

        self.id = cursor.lastrowid

        # Return the id of the newly created Mission record.
        return cursor.lastrowid

    def check_mission_exists(self, conn: sqlite3.Connection) -> bool:
        logging.info(f"Checking if {self.name} already in database.")

        cursor = conn.cursor()

        sql = """ SELECT * FROM Mission WHERE name = ? """

        # Execute query and commit to the db.
        result = cursor.execute(sql, (self.name,))

        if result.fetchone():
            return True
        else:
            return False
