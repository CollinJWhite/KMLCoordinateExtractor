import os
import csv
import logging
import xml.etree.ElementTree as ET
logging.basicConfig(filename='myProgramLog.txt', filemode='w', level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')

#gets a valid KML file from the user, quitting if they choose
def get_input_file():
    validFile = False
    directory=''
    while(not validFile):
        directory = input('Please enter a KML file to scan for coordinates (press q to quit): ')
        if(directory == 'q'):
            logging.debug('Quitting due to user input...')
            SystemExit
        logging.debug(f'Validating path %s', directory)
        directoryStrLength = len(directory)
        if(os.path.isfile(directory)):
            if(directory[directoryStrLength-4:directoryStrLength] == '.kml'):
                validFile = True
            else:
                basename = os.path.basename(directory)
                logging.warning('User tried using this file: %s. Prompting Again.', basename)
                print(f'{basename} is not a .xml file. Try Again.')
        else:
            logging.warning('User gave an invalid file path: %s. Prompting Again.', directory)
            print('Invalid file path. Try Again.')
    return directory

#writes a CSV file to the working directory with the given name
def write_CSV(CSVName):
    try:
        with open(f'{CSVName}.csv', mode="w", newline="", encoding="utf-8") as file: 
            writer = csv.writer(file)
            writer.writerows(CSVList)
        print(f"CSV file '{CSVName}' written successfully.")
    except OSError as e:
        print(f"Error writing file: {e}")



#--------------------------------Start of main program----------------------------------

logging.info('Start of Program')

directory = get_input_file()

CSVName = input('Please enter the name of the CSV file to be created: ')

tree = ET.parse(directory)

CSVList = [] #list of all lists to be written to CSV file
headerList = ['Longitude','Latitude','Altitude']#list of all headers; Columns of CSV file
CSVList.append(headerList)

#define kml namespace
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

logging.info('')
for coord in tree.findall('.//kml:coordinates', ns):
    coordText = coord.text
    coordList = coordText.split()
    for coordSet in coordList:
        tempList = []
        coords = coordSet.split(',')
        for coordinate in coords:
            tempList.append(coordinate)
        CSVList.append(tempList)

logging.info('Writing to CSV File...')

write_CSV(CSVName)

logging.info(f'CSV file {CSVName}.csv written successfully')