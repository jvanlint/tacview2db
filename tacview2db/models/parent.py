import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import logging
from models.database import Database


class Parent:
    type: str
    name: str
    pilot: str
    coalition: str
    country: str
    group: str

    def __init__(self, xml_tree: ET):
        xml_data = xml_tree.find("ParentObject")

        self.type = getattr(xml_data.find("Type"), "text", "n/a")
        self.name = xml_data.find("Name").text
        self.pilot = getattr(xml_data.find("Pilot"), "text", "n/a")

        if xml_data.find("Coalition"):
            self.coalition = getattr(xml_data.find("Coalition"), "text", "n/a")
        else:
            self.coalition = ""

        if xml_data.find("Country"):
            self.country = getattr(xml_data.find("Country"), "text", "n/a")
        else:
            self.country = ""

        self.group = getattr(xml_data.find("Group"), "text", "n/a")

    def xml_object_exists(xml_tree: ET) -> bool:
        xml_data = xml_tree.find("ParentObject")

        if xml_data:
            return True
        else:
            return False

    def write_to_db(self, db: Database, event_id: int, secondary_object_id: int):
        sql = """ INSERT INTO ParentObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group)
						VALUES(?,?,?,?,?,?,?,?) """

        db_values = (
            event_id,
            secondary_object_id,
            self.type,
            self.name,
            self.pilot,
            self.coalition,
            self.country,
            self.group,
        )
        # Execute query and commit to the db.
        record_id = db.execute_sql_statement(sql, db_values)

        return record_id
