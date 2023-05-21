import sqlite3
import logging
import time

from models.mission import Mission
from models.event import Event
from models.primary import Primary
from models.secondary import Secondary
from models.parent import Parent
from models.database import Database
from models.tacview_data import Tacview


def process_all_tacview_files(database_file: str, clear_db: bool, mission_filenames):
    # Set start time of processing to calculate total time taken.
    start = time.time()

    # Create a database connection and return the connection object.
    # conn = create_connection(database_file)
    database_obj = Database(database_file)

    # If the -c option was passed in then clear the DB before importing any data.
    if clear_db:
        # clear_table_data(conn)
        database_obj.clear_table_data()

    for file in mission_filenames:
        logging.info(f"Processing file named {file}.")
        process_tacview_file(database_obj.conn, file)

    database_obj.conn.close
    logging.info("All files processed successfully.")
    logging.info("The script took %.3f seconds to finish." % (time.time() - start))


def process_tacview_file(conn: sqlite3.Connection, filename: str):
    # Parse the XML file passed in as an argument.
    tacview_parsed_data = Tacview(filename)

    # tacview_parsed_data = parseXMLFile(filename)

    # Create a mission object and commit it to the database
    mission_obj = Mission(tacview_parsed_data.xml_full_data)
    if mission_obj.check_mission_exists(conn):
        logging.warning("Mission already exists in DB.")
    # Once mission created in DB we get an id for future storing related records.
    mission_obj.write_to_db(conn)

    # Extract the events from the parsed XML tree.
    event_data = tacview_parsed_data.xml_event_data

    # Process all the events contained with the parsed data.

    logging.info("Processing event records.")

    # Initialise counter variables to 0
    event_counter = (
        primary_object_counter
    ) = secondary_object_counter = parent_object_counter = 0

    for event in event_data:
        event_obj = Event(event)
        event_obj.write_to_db(conn, mission_obj.id)

        event_counter += 1

        # Get the primary object. Every Event has at least a Primary Object
        primary_obj = Primary(event)
        primary_obj.write_to_db(conn, event_obj.id)

        primary_object_counter += 1

        # Get the Secondary Object (if it exists). This object tells us what the event 'action' was performed on.
        if Secondary.xml_object_exists(event):
            secondary_obj = Secondary(event)
            secondary_obj.write_to_db(conn, event_obj.id)
            secondary_object_counter += 1

            # Get the Parent Object (if it exists). This object tells who performed the action.
            # A Parent object can only appear if a secondary object is present.
            # This is why it is contained within the Secondary object's IF statement scope.

            if Parent.xml_object_exists(event):
                parent_obj = Parent(event)
                parent_obj.write_to_db(conn, event_obj.id, secondary_obj.id)
                parent_object_counter += 1

    logging.info("EVENT records written to database.")
    logging.info(
        f"Successfully processed {event_counter} event records, {primary_object_counter} primary records, {secondary_object_counter} secondary records and {parent_object_counter} parent records."
    )
