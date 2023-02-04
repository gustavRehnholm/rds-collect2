#!/usr/bin/env python

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd
# For testing
import logging

#-----------Constants------------#
# Sec in an hour
SEC_PER_HOUR = 60*60
# Sec in a min
SEC_PER_MIN = 60
# nanoseconds in an second
NANO_SEC_PER_SEC = 1000000000
# is used to get the direction of each packet
IP_HOST = '10.88.0.9'
# Directory with the noise
FILES_2_PARSE_DIR = "captures_test"
# Directory with the result
PARSED_FILES_DIR = "parsedFiles_test"
# Directory with the web traffic
WEB_TRAFFIC_FILES_DIR = "dataset"
# the result file name
FOLD0_CSV = "dataset/fold-0.csv"
# How much of the header to remove (to fit the noise with the web traffic)
HEADER = 40
# Change depeding if testing or running
logging.basicConfig(level=logging.INFO)

#----------Variables----------#
# To store the total time of the parsed line that one is working on at the moment
currTotalTimeParseLine = time.time()
# To standardize the time of each packet
deviationTime = 0
# Current opened test/valid/train/ parsed file
currParsedFile = []
# all line in the web traffic
webTrafficLines = []
# List of all files to parse (aka all files in the filesToParseDir)
files2Parse = []

# files with the webTraffic
webTrafficTrainFiles = []
webTrafficValidFiles = []
webTrafficTestFiles  = []
# Files for the parsed noise
parsedTrainFiles = []
parsedValidFiles = []
parsedTestFiles  = []


#----------------Create the directory structure----------------

# Paths to the directories
files2ParseDirPath = os.path.join(os.getcwd(), FILES_2_PARSE_DIR)
parsedDirPath      = os.path.join(os.getcwd(), PARSED_FILES_DIR)
webTrafficDirPath  = os.path.join(os.getcwd(), WEB_TRAFFIC_FILES_DIR)

# Get list of all noise files (which will be parsed)
for (dirpath, dirnames, filenames) in walk(files2ParseDirPath, topdown=True):
    for files in filenames:
        files2Parse.append(os.path.join(files2ParseDirPath, files))
    print("Files to parse: ", len(files2Parse))
print("Setting up directories")

# Create the structure for the result directory, so it match the web traffics
for (dirpath, dirnames, filenames) in walk(webTrafficDirPath, topdown=True):
    for dirs in dirnames:
        try: 
            os.mkdir(os.path.join(parsedDirPath, dirs))
        except: 
            print("File and directory exists!") 


#----------------------Create the file structure for the parsed dataset--------------------

# dfFiles: The web traffic
df       = pd.read_csv(FOLD0_CSV)
dfFormat = ['log', 'is_train', 'is_valid', 'is_test']
dfFiles  = df[dfFormat]


# For every log file in the web traffic, make sure that there is an correlating log file to store the parsed result
for x in range(0, len(dfFiles['log'])):
    if(dfFiles['is_train'][x] == True): 
        parsedTrainFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        webTrafficTrainFiles.append(os.path.join(webTrafficDirPath,"client", dfFiles['log'][x]))
    elif(dfFiles['is_valid'][x] == True): 
        parsedValidFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        webTrafficValidFiles.append(os.path.join(webTrafficDirPath,"client", dfFiles['log'][x]))
    elif(dfFiles['is_test'][x] == True): 
        parsedTestFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        webTrafficTestFiles.append(os.path.join(webTrafficDirPath,"client", dfFiles['log'][x]))
    else:
        print("ERROR")

#----------------------------Parsing-------------------------------------------
'''
Parse and inject all the noise, if their is more web traffic than noise, the noise will be reused
'''

print("Starting parse")
print("trainFiles len = ", len(webTrafficTrainFiles))
files2Parse.sort()
print("filesToParse len  = ", len(files2Parse), "\n")

# Loop until all web traffic is used
# TODO: change condition of the parsing loop?
while(len(webTrafficTrainFiles) > 0):

    # For every file to parse (aka the noise)
    for fileToParsePath in files2Parse:
        print("New file to parse: ", os.path.basename(fileToParsePath))

        with open(fileToParsePath, 'r') as fileToParse:
            print("Opening ", os.path.basename(fileToParsePath))

            print("web traffic testing Files    left: " , len(webTrafficTestFiles))
            print("web traffic  validation Files left: ", len(webTrafficValidFiles))
            print("web traffic training Files   left: " , len(webTrafficTrainFiles))
            print("Lines left in web traffic: "         , len(webTrafficLines))
            print("\n")

            # For every line in the noise
            # Go thorugh the current noise file, line for line, because it might be to large for readlines()
            for parseLine in fileToParse:

                # get each attribute for the current line
                splitParseLine = parseLine.split("\t")
                # get the time for the data
                parseLineTime       = splitParseLine[0].split('.')
                totalTimeParseLine  = int(parseLineTime[0]) * NANO_SEC_PER_SEC
                logging.info("totalTimeParseLine = " + totalTimeParseLine)
                totalTimeParseLine += int(parseLineTime[1])
                logging.info("totalTimeParseLine = " + totalTimeParseLine)

                # Get the IP, that the direction will be extracted from
                directionSplit = splitParseLine[1].split(',')
                logging.info("directionSplit" + directionSplit)
                

                #-------------------limited files open test, valid then training-----------------------
                """
                Extract one web traffic packet and the file it should merge to (in crossLine and currParsedFile)
                """
                if (not len(webTrafficLines) and len(webTrafficTestFiles) > 0): #Check if it's time to preload a new file

                    # make deviation to match start at zero
                    deviationTime = totalTimeParseLine 

                    # get the current web traffic packet
                    crossFile = open(webTrafficTestFiles[0], 'r') #File from Tobias set
                    webTrafficTestFiles.pop(0)
                    webTrafficLines = crossFile.readlines()
                    crossFile.close()

                    # get current parsed
                    currParsedFile = open(parsedTestFiles[0], 'a') #What we write to
                    print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                    parsedTestFiles.pop(0)

                elif (not len(webTrafficLines) and len(webTrafficValidFiles) > 0): #Check if it's time to preload a new file
                    deviationTime = totalTimeParseLine #make deviation to match start at zero

                    crossFile = open(webTrafficValidFiles[0], 'r') #File from Tobias set
                    webTrafficValidFiles.pop(0)
                    webTrafficLines = crossFile.readlines()
                    crossFile.close()

                    currParsedFile = open(parsedValidFiles[0], 'a') #What we write to
                    print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                    parsedValidFiles.pop(0)

                elif (not len(webTrafficLines) and len(webTrafficTrainFiles) > 0):
                    deviationTime = totalTimeParseLine #make deviation to match start at zero

                    crossFile = open(webTrafficTrainFiles[0], 'r') #File from Tobias set
                    webTrafficTrainFiles.pop(0)
                    webTrafficLines = crossFile.readlines()
                    crossFile.close()

                    currParsedFile = open(parsedTrainFiles[0], 'a') #What we write to
                    print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                    parsedTrainFiles.pop(0)


                #-------------------------TODO: rewrite this shit code above to take less lines, this looks abyssmal---------------

                # Set time, direction and packet size, if direction or size is missing, skip the packet  
               
                finalTime = totalTimeParseLine - deviationTime

                if(directionSplit[0] == ''):
                    continue
                if (directionSplit[0] == IP_HOST):
                    direction = 's'
                elif(directionSplit[1] == IP_HOST):
                    direction = 'r'
                else:
                    checkIfLocal = directionSplit[0].split('.')
                    if checkIfLocal[0] == '10':
                        IP_HOST = directionSplit[0]
                    else: IP_HOST = directionSplit[1]

                splitCrossLine = webTrafficLines[0].split(",")
                try:
                    packetSize = str(int(splitParseLine[2])-HEADER)
                except:
                    continue
                    print("splitParseLine[2] = " + splitParseLine[2] + " could not be used to determine the packet Size, skipped")


                # Sort the noise and the web traffic after time
                # write all noise that are shorter than the current webb traffic packet
                if(finalTime < int(splitCrossLine[0])):
                    currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                    currTotalTimeParseLine = totalTimeParseLine
                # if the webb traffic packet is the next one, write it to the parsed list
                else:
                    currParsedFile.writelines(webTrafficLines[0])
                    webTrafficLines.pop(0)

            # Done with the current filesToParse
            print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
            deviationTime = 0
            fileToParse.close()

        # If more to parse, continiue, else end the parsing
        if(len(webTrafficTestFiles) > 0 and len(webTrafficValidFiles) > 0):
            print("Popping ", os.path.basename(files2Parse[0]))
            files2Parse.pop(0)
            print("Now first one is: ", os.path.basename(files2Parse[0]), "\n")
        else: print("We stopped removing files")
