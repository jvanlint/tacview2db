#!/usr/bin/python

import argparse
import os
import time
import sys
import logging
from dotenv import load_dotenv

from common.database import create_connection, create_mission, create_event, create_parent, create_primary, create_secondary, clear_table_data, check_mission_exists
from common.xml import parseXMLFile, create_mission_object


def process_tacview_file(filename: str, database_name: str, clear_db: bool):

    # Parse the XML file passed in as an argument.
    parsed_xml = parseXMLFile(filename)

    # Create a database connection and return the connection object.
    conn = create_connection(database_name)

    # If the -c option was passed in then clear the DB before importing any data.
    if clear_db:
        clear_table_data(conn)

    # Create a mission object and commit it to the database
    mission_data = create_mission_object(parsed_xml)
    print(check_mission_exists(conn, mission_data))
    mission_id = create_mission(conn, mission_data)

    event_data = parsed_xml[2].findall('Event')

    # Process all the events contained with the parsed data.

    logging.info('Processing event records.')
    event_counter = 0

    for event in event_data:
        event_counter += 1
        # Each Event will have a Time, Action and a Primary Object
        action = event.find('Action').text
        time = event.find('Time').text
        event_id = 0

        with conn:
            event_1 = (mission_id, time, action)
            event_id = create_event(conn, event_1)

        # Get the primary object
        # Every Event has at least a Primary Object
        primaryObject = event.find('PrimaryObject')
        primaryID = primaryObject.get('ID')
        primaryName = primaryObject.find('Name').text
        primaryType = getattr(primaryObject.find('Type'), 'text', 'n/a')
        primaryPilot = getattr(primaryObject.find('Pilot'), 'text',  'n/a')
        primaryCoalition = getattr(
            primaryObject.find('Coalition'), 'text',  'n/a')
        primaryCountry = getattr(primaryObject.find('Country'), 'text',  'n/a')
        primaryGroup = getattr(primaryObject.find('Group'), 'text',  'n/a')
        primaryParent = getattr(primaryObject.find('Parent'), 'text',  'n/a')

        with conn:
            primary = (event_id, primaryID, primaryType, primaryName, primaryPilot,
                       primaryCoalition, primaryCountry, primaryGroup, primaryParent)
            primary_id = create_primary(conn, primary)

        # Get the Secondary Object. This object tells us what the action ws performed on.
        secondaryObject = event.find('SecondaryObject')

        if secondaryObject:
            secondaryID = secondaryObject.get('ID')
            secondaryType = secondaryObject.find('Type').text
            secondaryName = secondaryObject.find('Name').text
            secondaryPilot = getattr(
                secondaryObject.find('Pilot'), 'text', 'n/a')
            if secondaryObject.find('Coalition') is not None:
                secondaryCoalition = secondaryObject.find('Coalition').text
            else:
                secondaryCoalition = ""

            if secondaryObject.find('Country') is not None:
                secondaryCountry = secondaryObject.find('Country').text
            else:
                secondaryCountry = ""

            secondaryParent = getattr(
                secondaryObject.find('Parent'), 'text', 'n/a')
            secondaryGroup = getattr(
                secondaryObject.find('Group'), 'text', 'n/a')
            secondaryParent = getattr(
                secondaryObject.find('Parent'), 'text', 'n/a')

            with conn:
                secondary = (event_id, secondaryID, secondaryType, secondaryName, secondaryPilot,
                             secondaryCoalition, secondaryCountry, secondaryGroup, secondaryParent)
                secondary_id = create_secondary(conn, secondary)

        # Get the Parent Object. This object tells who performed the action.
        parentObject = event.find('ParentObject')
        # print(parentObject)

        if parentObject:
            parentID = secondaryObject.get('ID')
            parentType = parentObject.find('Type').text
            parentName = parentObject.find('Name').text
            parentPilot = getattr(parentObject.find('Pilot'), 'text', None)
            parentCoalition = parentObject.find('Coalition').text

            if parentObject.find('Country') is not None:
                parentCountry = parentObject.find('Country').text
            else:
                parentCountry = ""

            parentGroup = parentObject.find('Group').text

            with conn:
                parent = (event_id, parentID, parentType, parentName,
                          parentPilot, parentCoalition, parentCountry, parentGroup)
                parent_id = create_parent(conn, parent)

    logging.info(f'Successfully processed {event_counter} event records.')


def main(argv):
    parser = argparse.ArgumentParser(
        description='Process TacView XML into a SQLite3 database.')
    parser.add_argument('filename', action='store',
                        help='The XML filename to process.')
    parser.add_argument('-c', '--cleardb', action='store_true',
                        help='Clear DB before importing file.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging to console.')
    args = parser.parse_args()

    # Process arguments
    mission_filename = args.filename
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
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    logging.info(
        f'Begin processing file named {mission_filename}. Clear DB set to {clear_db}')

    start = time.time()

    process_tacview_file(mission_filename, database_file, clear_db)

    print('-' * 80)
    print('*** Export to database complete! ***')
    print('The script took %.3f seconds to finish.' % (time.time() - start))


if __name__ == '__main__':
    main(sys.argv[1:])
