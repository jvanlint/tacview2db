import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import logging
from models.database import Database


class Event:
    id: int
    time: str
    action: str

    def __init__(self, xml_tree: ET):
        self.time = xml_tree.find("Time").text
        self.action = xml_tree.find("Action").text

    def write_to_db(self, db: Database, mission_id: int) -> int:
        sql = """ INSERT INTO Event(mission_id,time,action)
							VALUES(?,?,?) """

        db_values = (
            mission_id,
            self.time,
            self.action,
        )

        self.id = db.execute_sql_statement(sql, db_values)

        return self.id
