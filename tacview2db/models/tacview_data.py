import xml.etree.ElementTree as ET
import logging
from typing import Tuple


class Tacview:
    xml_full_data: ET
    xml_event_data: ET

    def __init__(self, xml_file: str):
        logging.info(f"Attempting to parse XML in {xml_file}.")

        # Parse the xml file to obtain the full data tree and the events data.
        try:
            tree = ET.parse(xml_file)
            self.xml_full_data = tree.getroot()
            self.xml_event_data = self.xml_full_data[2].findall("Event")
            logging.info(f"XML parsed successfully.")

        except FileNotFoundError:
            logging.error("The XML file was not found.")
            quit()

        except ET.ParseError as parse_error:
            logging.error(f"XML parsing failed. Error {parse_error.msg}")
