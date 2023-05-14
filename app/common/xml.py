import xml.etree.ElementTree as ET
import logging
from typing import Tuple


def parseXMLFile(filename: str) -> ET:
    logging.info(f"Attempting to parse XML in {filename}.")

    try:
        tree = ET.parse(filename)  # 'mission1_server.xml'
        logging.info(f"XML parsed successfully.")
        return tree.getroot()
    except FileNotFoundError:
        logging.error("The XML file was not found.")
        quit()
    except ET.ParseError as parse_error:
        logging.error(f"XML parsing failed. Error {parse_error.msg}")


def extract_event_data(xml_tree: ET) -> ET:
    logging.info(f"Extracting EVENTS for given mission from parsed XML tree.")
    return xml_tree[2].findall("Event")
