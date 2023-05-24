import sqlite3, logging, time

from models.mission import Mission
from models.event import Event
from models.primary import Primary
from models.secondary import Secondary
from models.parent import Parent
from models.database import Database
from models.tacview_data import Tacview


def process_all_tacview_files(
    database_file: str, clear_db: bool, mission_filenames: tuple[str]
):
    # Set start time of processing to calculate total time taken.
    start = time.time()

    # Create a database connection and return a database object.
    db = Database(database_file)

    # If the -c option was passed in then clear the DB before importing any data.
    if clear_db:
        db.clear_table_data()

    for file in mission_filenames:
        logging.info(f"Processing file named {file}.")
        process_tacview_file(db, file)

    db.close_connection

    logging.info(
        f"{len(mission_filenames)} files processed successfully in {time.time() - start:.3f} seconds."
    )


def process_tacview_file(db: Database, filename: str):
    # Parse the XML file by creating a Tacview object with the xml filename.
    tacview_parsed_data = Tacview(filename)

    # Create a mission object, check if it exists in the db and commit it to the database
    mission_obj = Mission(tacview_parsed_data.xml_full_data)
    mission_obj.check_mission_exists(db)
    mission_obj.write_to_db(db)

    # Extract the events data from the parsed XML tree.
    event_data = tacview_parsed_data.xml_event_data

    logging.info("Processing event records.")

    # Initialise counter variables to 0. These are used to display the amount of records processed for logging.
    event_counter = (
        primary_object_counter
    ) = secondary_object_counter = parent_object_counter = 0

    # Process all the events contained with the parsed data. This loop also processes the Primary, Secondary and Parent object associated with an Event.
    for event in event_data:
        event_obj = Event(event)
        event_obj.write_to_db(db, mission_obj.id)
        event_counter += 1

        # Get the primary object. Every Event has at least one Primary Object
        primary_obj = Primary(event)
        primary_obj.write_to_db(db, event_obj.id)
        primary_object_counter += 1

        # Get the Secondary Object (if it exists). This object tells us what the event 'action' was performed on.
        if Secondary.xml_object_exists(event):
            secondary_obj = Secondary(event)
            secondary_obj.write_to_db(db, event_obj.id)
            secondary_object_counter += 1

            # Get the Parent Object (if it exists). This object tells who performed the action.
            # A Parent object can only appear if a secondary object is present.
            # This is why it is contained within the Secondary object's IF statement scope.

            if Parent.xml_object_exists(event):
                parent_obj = Parent(event)
                parent_obj.write_to_db(db, event_obj.id, secondary_obj.id)
                parent_object_counter += 1

    logging.info(
        f"Successfully processed {event_counter} event records, {primary_object_counter} primary records, {secondary_object_counter} secondary records and {parent_object_counter} parent records."
    )
