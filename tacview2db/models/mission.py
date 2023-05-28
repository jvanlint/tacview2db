import xml.etree.ElementTree as ET
import logging
from models.database import Database


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

    def write_to_db(self, db: Database) -> int:
        logging.info(f"Attempting to add mission named {self.name} to database.")

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

        self.id = db.execute_sql_statement(sql, db_values)

        logging.info(f"Created mission in database.")

        # Return the id of the newly created Mission record.
        return self.id

    def check_mission_exists(self, db: Database) -> bool:
        logging.info(f"Checking if {self.name} already in database.")

        sql = f"SELECT * FROM Mission WHERE name = '{self.name}'"

        # Execute query and commit to the db.
        result = db.execute_sql_select_query(sql)

        # If the result is 0 then the mission was not found.
        if result:
            logging.warning("Mission already exists in DB.")
            return True
        else:
            return False
