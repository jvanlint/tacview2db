import xml.etree.ElementTree as ET
from models.database import Database


class Secondary:
    id: int
    type: str
    name: str
    pilot: str
    coalition: str
    country: str
    group: str
    parent_id: str

    def __init__(self, xml_tree: ET):
        xml_data = xml_tree.find("SecondaryObject")

        self.id = xml_data.get("ID")
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
        self.parent_id = getattr(xml_data.find("Parent"), "text", "n/a")

    def xml_object_exists(xml_tree: ET) -> bool:
        xml_data = xml_tree.find("SecondaryObject")

        if xml_data:
            return True
        else:
            return False

    def write_to_db(self, db: Database, event_id: int) -> int:
        sql = """ INSERT INTO SecondaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
                    VALUES(?,?,?,?,?,?,?,?,?) """
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
        self.id = db.execute_sql_statement(sql, db_values)

        return self.id
