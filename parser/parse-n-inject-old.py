#!/usr/bin/env python

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd
# For testing
import logging

def main():
    #-----------Constants------------#
    # Sec in an hour
    SEC_PER_HOUR = 60*60
    # Sec in a min
    SEC_PER_MIN = 60
    # nanoseconds in an second
    NANO_SEC_PER_SEC = 1000000000
    # Directory with the noise
    FILES_2_PARSE_DIR = "captures"
    # Directory with the result
    PARSED_FILES_DIR = "parsedFiles-old"
    # Directory with the web traffic
    #   dataset: the whole dataset, can be trained on, but to large for quick testing
    #   dataset-test: a much shorter dataset with only google as a site, only for testing the parser
    WEB_TRAFFIC_FILES_DIR = "dataset"
    # the result file name
    #   dataset/fold-0.csv: information about what the different packet should be used for
    #   dataset-test/fold-0-test.csv: fold file for the dataset-test
    FOLD0_CSV = "dataset/fold-0.csv"
    # How much of the header to remove (to fit the noise with the web traffic)
    HEADER = 40

    # index of the different attributes
    IP_INDEX_SENDER = 0
    IP_INDEX_RECIEVER = 1
    PACKET_ATTR_INDEX_TIME = 0
    PACKET_ATTR_INDEX_IP   = 1
    PACKET_ATTR_INDEX_SIZE = 2


    #----------Variables----------#
    # Change depeding if testing or running
    logging.basicConfig(level=logging.INFO)
    # is used to get the direction of each packet
    ipHost = '10.88.0.9'
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

    # Loop until all web traffic is used, and because the training files will be used last, it is enough to check them
    while(len(webTrafficTrainFiles) > 0):

        # For every file to parse (aka the noise)
        for fileToParsePath in files2Parse:
            print("New file to parse: ", os.path.basename(fileToParsePath))
            
            # When there is no more web traffic data left to inject into, end the program
            if(len(webTrafficTrainFiles) <= 0):
                print("\n")
                print("Of the web traffic there is:")
                print("testing    files   left: ", len(webTraffictestFiles))
                print("validation files   left: ", len(webTrafficvalidFiles))
                print("training   files   left: ", len(webTrafficTrainFiles))
                print("Lines              left: ", len(webTrafficLines))
                print("\n")
                print("No more files to train, ends the program")
                return


            with open(fileToParsePath, 'r') as fileToParse:
                print("Opening ", os.path.basename(fileToParsePath))

                print("web traffic testing Files    left: "      , len(webTrafficTestFiles))
                print("web traffic validation Files left: "      , len(webTrafficValidFiles))
                print("web traffic training Files   left: "      , len(webTrafficTrainFiles))
                print("Lines left in the open web traffic file: ", len(webTrafficLines))
                print("\n")

                # For every line in the noise
                # Go through the current noise file, line for line, because it might be to large for readlines()
                for parseLine in fileToParse:

                    # get each attribute for the current line
                    splitParseLine = parseLine.split("\t")

                    # get the time for the data (convert from seconds with 9 float numbers, to nanoseconds as a integer)
                    parseLineTime           = splitParseLine[PACKET_ATTR_INDEX_TIME].split('.')
                    timeLeftOfDotInNanoSec  = int(parseLineTime[0]) * NANO_SEC_PER_SEC
                    timeRightOfDotInNanoSec = int(parseLineTime[1])
                    totalTimeParseLine      =  timeLeftOfDotInNanoSec + timeRightOfDotInNanoSec

                    # Get the IP of the source [0] and destination [1]
                    directionSplit = splitParseLine[PACKET_ATTR_INDEX_IP].split(',')
                

                    #-----------------Open a new web traffic file------------------

                    # Check if a new web traffic file needs to be loaded
                    if len(webTrafficLines) == 0:
                        deviationTime = totalTimeParseLine 

                        # check which type of web traffic to get, and get the file the result will be written to

                        if len(webTrafficTestFiles) > 0:
                            webTrafficFile = open(webTrafficTestFiles[0], 'r')
                            webTrafficTestFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTestFiles[0], 'a') 
                            print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                            parsedTestFiles.pop(0)

                        elif len(webTrafficValidFiles) > 0:

                            webTrafficFile = open(webTrafficValidFiles[0], 'r') 
                            webTrafficValidFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedValidFiles[0], 'a') 
                            print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                            parsedValidFiles.pop(0)

                        elif len(webTrafficLines) == 0  and len(webTrafficTrainFiles) > 0:

                            webTrafficFile = open(webTrafficTrainFiles[0], 'r') 
                            webTrafficTrainFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTrainFiles[0], 'a') 
                            print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                            parsedTrainFiles.pop(0)

                        else:
                            # Done with the parsing
                            print("Have injected all web traffic with noise")
                            print("Ending the program")
                            return

                    # Set time, direction and packet size, if direction or size is missing, skip the packet  
                
                    # Time
                    finalTime = totalTimeParseLine - deviationTime

                    # Direction
                    if(directionSplit[IP_INDEX_SENDER] == ''):
                        print("The noise packet has no IP address for the sender, skipping this noise packet")
                        continue
                    if (directionSplit[IP_INDEX_SENDER] == ipHost):
                        direction = 's'
                    elif(directionSplit[IP_INDEX_RECIEVER] == ipHost):
                        direction = 'r'
                    # If the IP_HOST is wrong, choose the one that start with an 10 as the host
                    else:
                        checkIfLocal = directionSplit[IP_INDEX_SENDER].split('.')
                        if checkIfLocal[0] == '10':
                            ipHost = directionSplit[0]
                        else: ipHost = directionSplit[1]

                    # Size
                    try:
                        packetSize = str(int(splitParseLine[PACKET_ATTR_INDEX_SIZE])-HEADER)
                    except:
                        print("splitParseLine[2] = " + splitParseLine[2] + " could not be used to determine the packet Size, skipped")
                        continue

                    
                    # Do not accept an empty packet size
                    if int(packetSize) == 0:
                        print("Packet size" + packetSize + " is 0, and therefore invalid")
                        continue
                    

                    # If the current web traffic packet is empty, add the current noise packet
                    # Indicates that one should switch to a new web traffic file, but before that, one should add the noise
                    # TODO: make sure that this does not cause any problem
                    # TODO: might want to rm the print 
                    try:
                        currWebTrafficPacketAttrList = webTrafficLines[0].split(",")
                    except:
                        currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                        print("Crossline is empty, added the noise line")
                        continue

                    # Sort the noise and the web traffic after time
                    if(finalTime < int(currWebTrafficPacketAttrList[PACKET_ATTR_INDEX_TIME])):
                        currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                    else:
                        currParsedFile.writelines(webTrafficLines[0])
                        webTrafficLines.pop(0)

                # Done with the current filesToParse
                print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
                deviationTime = 0
                fileToParse.close()

            # If more web traffic, go to the next file to be parsed (next noise file)
            if(len(webTrafficTestFiles) > 0 and len(webTrafficValidFiles) > 0):
                print("Popping ", os.path.basename(files2Parse[0]))
                files2Parse.pop(0)
                print("Now first one is: ", os.path.basename(files2Parse[0]), "\n")
            else: print("We stopped removing files")


# run main 
if __name__=="__main__":
    main()
