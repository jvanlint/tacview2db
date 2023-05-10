#!/usr/bin/python

import xml.etree.ElementTree as ET
import logging
from typing import Tuple


def parseXMLFile(filename: str) -> ET:
    logging.info(f'Attempting to parse XML in {filename}.')

    try:
        tree = ET.parse(filename)  # 'mission1_server.xml'
        logging.info(f'XML parsed successfully.')
        return tree.getroot()
    except FileNotFoundError:
        logging.error('The XML file was not found.')
        quit()
    except ET.ParseError as parse_error:
        logging.error(f'XML parsing failed. Error {parse_error.msg}')


def extract_mission_object_data(xml_tree: ET) -> Tuple[str]:

    logging.info(f'Extracting high level MISSION info from parsed XML tree.')

    missionName = xml_tree[1][0].text
    missionTime = xml_tree[1][1].text
    missionDuration = xml_tree[1][2].text
    missionSource = xml_tree[0][0].text
    missionRecorder = xml_tree[0][1].text
    missionRecordingTime = xml_tree[0][2].text
    missionAuthor = xml_tree[0][3].text

    return (missionName, missionTime, missionDuration, missionSource, missionRecorder, missionRecordingTime, missionAuthor)


def extract_event_data(xml_tree: ET) -> ET:

    logging.info(f'Extracting EVENTS for given mission from parsed XML tree.')
    return xml_tree[2].findall('Event')


def extract_event_object_data(mission_id, xml_tree: ET) -> Tuple[str]:
    time = xml_tree.find('Time').text
    action = xml_tree.find('Action').text
    return(mission_id, time, action)


def extract_primary_object_data(event_id, xml_tree) -> Tuple[str]:

    primary_object = xml_tree.find('PrimaryObject')

    primaryID = primary_object.get('ID')
    primaryName = primary_object.find('Name').text
    primaryType = getattr(primary_object.find('Type'), 'text', 'n/a')
    primaryPilot = getattr(primary_object.find('Pilot'), 'text',  'n/a')
    primaryCoalition = getattr(
        primary_object.find('Coalition'), 'text',  'n/a')
    primaryCountry = getattr(primary_object.find('Country'), 'text',  'n/a')
    primaryGroup = getattr(primary_object.find('Group'), 'text',  'n/a')
    primaryParent = getattr(primary_object.find('Parent'), 'text',  'n/a')

    return(event_id, primaryID, primaryType, primaryName, primaryPilot,
           primaryCoalition, primaryCountry, primaryGroup, primaryParent)


def extract_secondary_object_data(event_id, xml_tree):

    secondary_object = xml_tree.find('SecondaryObject')

    if secondary_object:
        secondaryID = secondary_object.get('ID')
        secondaryType = secondary_object.find('Type').text
        secondaryName = secondary_object.find('Name').text
        secondaryPilot = getattr(secondary_object.find('Pilot'), 'text', 'n/a')
        if secondary_object.find('Coalition') is not None:
            secondaryCoalition = secondary_object.find('Coalition').text
        else:
            secondaryCoalition = ""

        if secondary_object.find('Country') is not None:
            secondaryCountry = secondary_object.find('Country').text
        else:
            secondaryCountry = ""

        secondaryParent = getattr(
            secondary_object.find('Parent'), 'text', 'n/a')
        secondaryGroup = getattr(secondary_object.find('Group'), 'text', 'n/a')
        secondaryParent = getattr(
            secondary_object.find('Parent'), 'text', 'n/a')

        return (event_id, secondaryID, secondaryType, secondaryName, secondaryPilot,
                secondaryCoalition, secondaryCountry, secondaryGroup, secondaryParent)
    else:
        return None


def extract_parent_object_data(event_id, parentID, xml_tree):
    parent_object = xml_tree.find('ParentObject')

    if parent_object:
        parentType = parent_object.find('Type').text
        parentName = parent_object.find('Name').text
        parentPilot = getattr(parent_object.find('Pilot'), 'text', None)
        parentCoalition = parent_object.find('Coalition').text

        if parent_object.find('Country') is not None:
            parentCountry = parent_object.find('Country').text
        else:
            parentCountry = ""

        parentGroup = parent_object.find('Group').text

        return (event_id, parentID, parentType, parentName,
                parentPilot, parentCoalition, parentCountry, parentGroup)
    else:
        return None
