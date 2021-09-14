import requests
from requests import get
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

'''
********** This program extracts the names and prices of the 100 first stocks from the url below
********** saves them in their own array one for the name and one for the price, ant then
********** the data is formated to a fine looking table which then is printed to the console.

********** Next step is to make this script run after the market has closed, save the data for
********** the current dat to it's own file.
'''

#       # TODO
#       Make the program get data for all the stocks in Large Cap not just the 100 first
#       Make the types of data have the correct datatypes. The stockprices should be float and
#       so on...
#
#       Maybe just use on soup object is better? Now I'm just retreaving the tags
#       is contaning the data I want right away.

url = "https://www.avanza.se/aktier/lista.html"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

closingPrice = []
stockNames = []

stockData = soup.find_all('a', class_='ellipsis')
lastPrices = soup.find_all('span', class_='pushBox')

for container in lastPrices:
    # extracts the prices from each stock, formats the string and appends to variable
    lastPrice = container.string
    lastPrice = lastPrice.strip()
    closingPrice.append(lastPrice)
    # extract the namesof the stocks, format the text and append to variable
for names in stockData:
    name = names.text
    name = name.strip()
    stockNames.append(name)

# make table of all the data
stocks = pd.DataFrame({'Aktie': stockNames, 'Pris': closingPrice})

# display all in terminal. Not truncated
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

print(stocks)
stocks.to_csv("aktier.csv")
