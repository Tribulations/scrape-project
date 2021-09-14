# -*- coding: utf-8 -*-
#import chromedriver_install as cdi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
# code from https://www.pluralsight.com/guides/guide-scraping-dynamic-web-pages-python-selenium

driver = webdriver.Chrome("/usr/bin/chromedriver") # loads the driver?
driver.get("http://www.nasdaqomxnordic.com/shares") # retrieves the webpage?

xpath = "//*[@id=\"marketCheckboxes\"]/li[3]/label" # the path to the clickbox
element = driver.find_element_by_xpath(xpath) # saves the element i var.
element.click() # clicks the element
xpathToTable = "/html/body/section/div/div/div/section/div/article/div/div[2]/table[1]"
div = driver.find_element_by_id('searchSharesListOutput')

javaScript = "document.getElementByTagName(\"div\")"
links = driver.execute_script(javaScript)
driver.quit()
