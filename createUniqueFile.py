#!/usr/bin/python
from datetime import datetime
from pathlib import Path
import time

def createUniqueFile():
	uniqueFileCreated = False
	while uniqueFileCreated == False:
		currentDatetime = datetime.now()

		#this should work in a single row instead of all variables above?
		fileName = currentDatetime.strftime("%Y-%m-%d-%H-%M-%S-%f") #%f is microseconds
		filepath = "/home/pi/sharedFolder/Scraping/" + fileName + ".csv"

		newFile =  Path(filepath)
		#check if the file name is unique
		if newFile.is_file() == False:
			#filename does not already exist
			#return the unique filename
			uniqueFileCreated = True

	return filepath
