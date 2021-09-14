# define functions which will be used in a scrapeProject

# replace a comma with a period and convert to float
def toFloat(text):
    temp = text.replace(',', '.')
    num = float(temp)
    return num

# remove whitespace and convert to int
def toInt(text):
    temp = text.replace(' ', '')
    num = int(temp)
    return num

def convertData(values):
    for i in range(len(values)):
        if i == len(values) - 1:
            values[i] = values[i].replace(' ', '')
            break
        values[i] = values[i].replace(',', '.')

# write vaues to file           **********Should i close the file in the function or outside?
def toCSVFile(values, file):
    for i in range(len(values)):
        if i == len(values) - 1:
            file.write(str(values[i]) + '\n')
            break
        file.write(str(values[i]) + ',')
