#!/usr/bin/python

import argparse
import os
import time
import sys
import logging
from dotenv import load_dotenv
import sqlite3

from common.database import create_connection, create_mission_record, create_event_record, create_parent_record, create_primary_record, create_secondary_record, clear_table_data, check_mission_exists
from common.xml import parseXMLFile, extract_mission_object_data, extract_event_data, extract_event_object_data, extract_primary_object_data, extract_secondary_object_data, extract_parent_object_data


def process_tacview_file(conn: sqlite3.Connection, filename: str):

    # Parse the XML file passed in as an argument.
    tacview_parsed_data = parseXMLFile(filename)

    # Create a mission object and commit it to the database
    mission_data = extract_mission_object_data(tacview_parsed_data)
    # Once mission created in DB we get an id for future storing related records.
    mission_id = create_mission_record(conn, mission_data)

    # Extract the events from the parsed XML tree.
    event_data = extract_event_data(tacview_parsed_data)

    # Process all the events contained with the parsed data.

    logging.info('Processing event records.')
    event_counter = primary_object_counter = secondary_object_counter = parent_object_counter = 0

    for event in event_data:

        event_id = create_event_record(
            conn, extract_event_object_data(mission_id, event))
        event_counter += 1

        # Get the primary object. Every Event has at least a Primary Object
        primary_object_data = extract_primary_object_data(event_id, event)
        create_primary_record(conn, primary_object_data)
        primary_object_counter += 1

        # Get the Secondary Object. This object tells us what the event 'action' was performed on.
        secondary_object_data = extract_secondary_object_data(event_id, event)
        if secondary_object_data:
            secondaryObjectID = secondary_object_data[1]
            create_secondary_record(conn, secondary_object_data)
            secondary_object_counter += 1

        # Get the Parent Object. This object tells who performed the action. They can only appear if a secondary object is present.
            parent_object_data = extract_parent_object_data(
                event_id, secondaryObjectID, event)
            if parent_object_data:
                create_parent_record(conn, parent_object_data)
                parent_object_counter += 1

    logging.info(
        f'Successfully processed {event_counter} event records, {primary_object_counter} primary records, {secondary_object_counter} secondary records and {parent_object_counter} parent records.')


def main(argv):
    parser = argparse.ArgumentParser(
        description='Process TacView XML into a SQLite3 database.')
    parser.add_argument('filename', action='store', nargs='+',
                        help='The XML filename to process.')
    parser.add_argument('-c', '--cleardb', action='store_true',
                        help='Clear DB before importing file.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging to console.')
    args = parser.parse_args()

    # Process arguments
    mission_filenames = args.filename
    clear_db = args.cleardb

    # Read environment variables
    load_dotenv()
    database_file = os.getenv('DATABASE_NAME')

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
                logging.FileHandler("app.log", mode='w'),
                # logging.StreamHandler(),
        ],
    )

    if args.verbose:
        console = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s -  %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    start = time.time()

    # Create a database connection and return the connection object.
    conn = create_connection(database_file)

    # If the -c option was passed in then clear the DB before importing any data.
    if clear_db:
        clear_table_data(conn)

    for file in mission_filenames:
        logging.info(f'Begin processing file named {file}.')
        process_tacview_file(conn, file)

    conn.close

    print('-' * 80)
    print('*** Export to database complete! ***')
    print('The script took %.3f seconds to finish.' % (time.time() - start))


if __name__ == '__main__':
    main(sys.argv[1:])
