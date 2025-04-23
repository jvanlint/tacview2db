import logging
import time
import os

from models.mission import Mission
from models.event import Event
from models.primary import Primary
from models.secondary import Secondary
from models.parent import Parent
from models.database import Database
from models.tacview_data import Tacview
from pathlib import Path
from tqdm import tqdm


def calculate_total_bytes(files: str):
    total_bytes = 0

    for file in files:
        total_bytes += os.path.getsize(file)

    return total_bytes


def calculate_file_size(file: str):
    return os.path.getsize(file)


def process_all_tacview_files(
    db: Database, clear_db: bool, mission_filenames: tuple[str]
) -> tuple[int]:
    # Set start time of processing to calculate total time taken.
    start = time.perf_counter()

    file_counter = 0
    total_bytes = calculate_total_bytes(mission_filenames)
    #! Remove this code
    # total_files = len(mission_filenames)
    # total_bytes_processed = 0

    # If the -c option was passed (or checkbox ticked in GUI) in then clear the DB before importing any data.
    if clear_db:
        db.clear_table_data()

    # Create a progress bar object
    progress_bar = tqdm(
        total=total_bytes,
        ncols=80,
        unit="kb",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    )

    for file in mission_filenames:
        if Path(file).exists():
            process_tacview_file(db, file)
            file_counter += 1
            progress_bar.set_postfix_str(file)
            # progress_bar.set_description("Processing...")
            progress_bar.update(calculate_file_size(file))
        else:
            logging.error(
                f"File name {file} does not exist and being skipped for processing."
            )

    # Close the progress bar
    progress_bar.close()

    end = time.perf_counter()
    logging.info(
        f"{file_counter} files processed successfully in {end - start:.3f} seconds. {len(mission_filenames) - file_counter} files were not found."
    )

    return (file_counter, len(mission_filenames))


def process_tacview_file(db: Database, filename: str):
    logging.info(f"Processing file named {filename}.")
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
