import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import logging


class Primary:
    id: int
    type: str
    name: str
    pilot: str
    coalition: str
    country: str
    group: str
    parent_id: str

    def __init__(self, xml_tree: ET):
        xml_data = xml_tree.find("PrimaryObject")

        self.id = xml_data.get("ID")
        self.type = getattr(xml_data.find("Type"), "text", "n/a")
        self.name = xml_data.find("Name").text
        self.pilot = getattr(xml_data.find("Pilot"), "text", "n/a")
        self.coalition = getattr(xml_data.find("Coalition"), "text", "n/a")
        self.country = getattr(xml_data.find("Country"), "text", "n/a")
        self.group = getattr(xml_data.find("Group"), "text", "n/a")
        self.parent_id = getattr(xml_data.find("Parent"), "text", "n/a")

    def write_to_db(self, conn: sqlite3.Connection, event_id: int):
        sql = """ INSERT INTO PrimaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
							VALUES(?,?,?,?,?,?,?,?,?) """
        cursor = conn.cursor()
        db_values = (
            event_id,
            self.id,
            self.type,
            self.name,
            self.pilot,
            self.coalition,
            self.country,
            self.group,
            self.parent_id,
        )
        # Execute query and commit to the db.
        cursor.execute(sql, db_values)
        conn.commit()
        self.id = cursor.lastrowid

        return cursor.lastrowid
