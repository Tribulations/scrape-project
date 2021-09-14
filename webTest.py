file = open("/home/pi/sharedFolder/Scraping/kuk.txt", 'a')
file.write("Program started! \t\n")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True



url = "http://www.nasdaqomxnordic.com/shares"


driver = webdriver.Chrome("/usr/bin/chromedriver")
file.write("webdriver started! \t\n")
driver.get(url)


file.write("Program ended! \t\n")
file.close()
driver.quit()
