# -*- coding: utf-8 -*-
#import chromedriver_install as cdi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # many of these imports isn't even used but I tried them earlier for some other bugs so they're just still here.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from datetime import datetime
from createUniqueFile import createUniqueFile
import logging
import random
import functions as f

# logging Save log file of the errors thrown. Maybe put this in a function
logger = logging.getLogger('dynamicScrape')
logger.setLevel(logging.INFO) # you can set this to DEBUG, INFO, ERROR
# assign a file handlerto that instance
fh = logging.FileHandler("errorLog.txt")
fh.setLevel(logging.INFO)# again you can st his differently
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)# This will set the format to the FileHandler
# Add the handler to your loigging instance
logger.addHandler(fh)

randWait = random.randint(1, 120)

# Make a try and except to be able to cath exceptions
try:
	file = open("/home/pi/sharedFolder/Scraping/log.txt", 'a') # opens a file for logging which stores the start and stop of the program. Maybe this comment isnt even needed? :)
	time.sleep(randWait)
	url = "http://www.nasdaqomxnordic.com/shares"
	driver = webdriver.Chrome("/usr/bin/chromedriver") # loads the driver? Maybe the path isn't needed?
	driver2 = webdriver.Chrome()

	driver.get(url) # retrieves the webpage where all the stock are displayed.
	time.sleep(10) # waits a while to let the webpage load. Maybe I should use a excplicit wait instead of this?
	cookieBox = driver.find_element_by_link_text("Ok, got it").click() # yeah the code says it all for this line :)
	xpathSTO = "//*[@id=\"marketCheckboxes\"]/li[3]/label" # the path to the clickbox
	STOClickBox = driver.find_element_by_xpath(xpathSTO) # saves the element in variable.
	STOClickBox.click() # clicks the element. Yeah what?? :D
	xpathSmallCap = "//*[@id=\"nordicSegment\"]/ul/li[3]/label"
	xpathMidCap = "//*[@id=\"nordicSegment\"]/ul/li[2]/label"
	MidCapClickBox = driver.find_element_by_xpath(xpathMidCap)

	SmallCapClickBox = driver.find_element_by_xpath(xpathSmallCap)

	time.sleep(2)
	MidCapClickBox.click()
	time.sleep(2)
	SmallCapClickBox.click()

	time.sleep(6.75)

	div = driver.find_element_by_id('searchSharesListOutput')
	time.sleep(7)
	tbody = div.find_element(By.TAG_NAME, 'tbody')
	tableRows = tbody.find_elements(By.TAG_NAME, 'tr')
	amountOfStock = len(tableRows)
	print("AmountOfStock = " + str(amountOfStock))
	file.write("\nAmountOfStock = " + str(amountOfStock) + '\t\n')
	file.write("Script started ")
	file.write(datetime.now().strftime("%y-%m-%d %H:%M:%S") + '\t\n' )
	#print("Script started: " + datetime.now().strftime("%H:%M:%S") + '\n')
	amountOfLinks = 0

	stockNames = []
	openingPrices = []
	lowestPrices = []
	highestPrices = []
	closingPrices = []
	totalVolumes = []

	for rows in tableRows:
		currentLink = rows.find_element_by_css_selector("td:nth-of-type(2)>a")
		amountOfLinks += 1
		link = currentLink.get_attribute('href')
		time.sleep(7)

		#print(stockName)
		# test with TimeoutException. If Timeout try again
		while True:
			try:
				time.sleep(random.random())
				driver2.get(link)
				break
			except TimeoutException:
				print("Loading took to long. TimeoutException.")
				file.write("TimeoutException occured." + datetime.now().strftime("%y-%m-%d %H:%M:S") + '\t\n')
		#driver2.get(link)
		#nameXpath = "//*[@id=\"shareInfoTop\"]/li[1]/h1/span"
		nameXpath = "/html/body/section/div/div/div/section/div[1]/article/div/div[2]/div[1]/ul[1]/li[1]/h1/span"
		nameElement = driver2.find_element_by_xpath(nameXpath)
		closingPriceElement = driver2.find_element_by_css_selector(".valueLatest") # maybe to long variable names haha
		openingPriceElement = driver2.find_element_by_css_selector(".op")
		lowestPriceElement = driver2.find_element_by_css_selector(".lp")
		highestPriceElement = driver2.find_element_by_css_selector(".hp")
		totalVolumeElement = driver2.find_element_by_css_selector(".tv")
		time.sleep(2)
		stockNames.append(nameElement.text)
		openingPrices.append(openingPriceElement.text)
		lowestPrices.append(lowestPriceElement.text)
		highestPrices.append(highestPriceElement.text)
		closingPrices.append(closingPriceElement.text)
		totalVolumes.append(totalVolumeElement.text)

		# code to print all data of each stock to separate file
		stockName = nameElement.text
		# write the date to the file
		currentStockFile = open("/home/pi/sharedFolder/Scraping/database/" + stockName + ".csv", 'a')
		currentStockFile.write(datetime.now().strftime("%Y-%m-%d") + ",")
		currentStockData = []
		currentStockData.append(closingPriceElement.text)
		currentStockData.append(openingPriceElement.text)
		currentStockData.append(lowestPriceElement.text)
		currentStockData.append(highestPriceElement.text)
		currentStockData.append(totalVolumeElement.text)

		# convert the data
		f.convertData(currentStockData)
		# write the data to file
		f.toCSVFile(currentStockData, currentStockFile)
		currentStockFile.close()
		currentStockData.clear()
		# create pandas DataFrame, which is a neat table of data.
	stockData = pd.DataFrame({'Stock': stockNames, 'Close': closingPrices, 'Open': openingPrices, 'Low': lowestPrices, 'High': highestPrices, 'Volume': totalVolumes})

	pd.set_option('display.max_rows', None)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.width', None)
	pd.set_option('display.max_colwidth', -1)

	#create uniquefilename
	fileName = createUniqueFile()

	print(stockData)
	stockData.to_csv(fileName)

	print(str(amountOfLinks))
	#file.write("AmountOfLinks = " + str(amountOfLinks))
	file.write("Script ended: " + datetime.now().strftime("%y-%m-%d %H:%M:%S"))
	driver.quit()
	driver2.quit()
	file.close()
except Exception as e:
	logger.exception(e)
	print("Exception occurred!")
	driver.quit()
	driver2.quit()
	file.close()
