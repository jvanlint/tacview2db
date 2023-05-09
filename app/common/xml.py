#!/usr/bin/python

import xml.etree.ElementTree as ET
import logging

def parseXMLFile(filename):
	logging.info(f'Attempting to parse XML in {filename}.')
	
	try:
		tree = ET.parse(filename)		#'mission1_server.xml'
		logging.info(f'XML parsed successfully.')
		return tree.getroot()
	except FileNotFoundError:
		logging.error('The XML file was not found.')
		quit()
	except ET.ParseError as parse_error:
		logging.error(f'XML parsing failed. Error {parse_error.msg}')

def create_mission_object(xml_tree):
	missionName = xml_tree[1][0].text
	missionTime = xml_tree[1][1].text
	missionDuration = xml_tree[1][2].text
	missionSource = xml_tree[0][0].text
	missionRecorder = xml_tree[0][1].text
	missionRecordingTime = xml_tree[0][2].text
	missionAuthor = xml_tree[0][3].text

	return  (missionName, missionTime, missionDuration, missionSource, missionRecorder, missionRecordingTime, missionAuthor)