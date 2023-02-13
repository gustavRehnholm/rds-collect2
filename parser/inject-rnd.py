'''
Inject parsed noise to the web traffic
'''

#!/usr/bin/env python

import os
from os import walk
from os import path
from re import search
import pandas as pd
import random
import sys

from inject_valid_testing import InjectValidationTesting

def main():
    length = sys.argv[1]

    #-----------Constants------------#
    # Directory with the noise
    FILES_2_PARSE_DIR = "parsed-noise/twitch/captures-" + str(length)
    # Directory with the result
    PARSED_FILES_DIR = "injected-datasets/twitch/parsedFiles-ittr-" + str(length)
    # Directory with the web traffic
    WEB_TRAFFIC_FILES_DIR = "dataset/client"
    # Information about what the different web traffics should be used for on the WF (training, validation, testing)
    FOLD0_CSV = "dataset/fold-0.csv"

    # index of the different attributes
    PACKET_ATTR_INDEX_TIME  = 0
    PACKET_ATTR_INDEX_DIR   = 1
    PACKET_ATTR_INDEX_SIZE  = 2

    #----------Variables----------#
    # To standardize the time of each packet
    deviationTime = 0
    # Current opened test/valid/train/ parsed file
    currParsedFile = []
    # all lines that are left to read in the current opened web traffic file
    webTrafficLines = []
    # List of all the noise, which should be injected into the web traffic
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
    os.system("rm -f -r " + PARSED_FILES_DIR)
    os.system("mkdir " + PARSED_FILES_DIR)

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
            webTrafficTrainFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        elif(dfFiles['is_valid'][x] == True): 
            parsedValidFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
            webTrafficValidFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        elif(dfFiles['is_test'][x] == True): 
            parsedTestFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
            webTrafficTestFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        else:
            print("ERROR a packet in the web traffic is neither for training, validation or testing in the fold-0 file.")

    print("Starting injecting noise")
    print("trainFiles len = ", len(webTrafficTrainFiles))
    noise2train = InjectValidationTesting(webTrafficTestFiles, webTrafficValidFiles, files2Parse)


    print("Start the randomised injection of the training data")
    # Loop until all web traffic is used, and because the training files will be used last, it is enough to check them
    while(len(webTrafficTrainFiles) > 0):

        # Choose one of the remaining noise at random to inject into the web traffic for training
        rnd_index = random.randrange(len(noise2train) - 1)
        fileToParsePath = noise2train[rnd_index]

        print("New file to parse: ", os.path.basename(fileToParsePath))


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
                packetAttrList = splitParseLine[0].split(",")
            

                #-----------------Open a new web traffic file------------------

                # Check if a new web traffic file needs to be loaded
                if len(webTrafficLines) == 0:
                    deviationTime = int(packetAttrList[PACKET_ATTR_INDEX_TIME])

                    # check which type of web traffic to get, and get the file the result will be written to

                    if len(webTrafficTrainFiles) > 0:

                        webTrafficFile = open(webTrafficTrainFiles[0], 'r') 
                        webTrafficTrainFiles.pop(0)
                        webTrafficLines = webTrafficFile.readlines()
                        webTrafficFile.close()

                        currParsedFile = open(parsedTrainFiles[0], 'a') 
                        #print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                        parsedTrainFiles.pop(0)

                    else:
                        # Done with the parsing
                        print("Have injected all web traffic with noise")
                        print(sys.argv[1],"/", len(noise2train), "(total noise files)/(noise files for training)")
                        print("Ending the program")
                        return

                # Set time, direction and packet size, if direction or size is missing, skip the packet  
            
                # Time
                localTime = int(packetAttrList[PACKET_ATTR_INDEX_TIME])
                finalTime = localTime - deviationTime

                # If the current web traffic packet is empty, add the current noise packet
                # Indicates that one should switch to a new web traffic file, but before that, one should add the noise
                try:
                    currWebTrafficPacketAttrList = webTrafficLines[0].split(",")
                except:
                    currParsedFile.writelines([str(finalTime), ",", packetAttrList[PACKET_ATTR_INDEX_DIR], ",", packetAttrList[PACKET_ATTR_INDEX_SIZE]])
                    print("webTrafficLines is empty, added the noise line")
                    continue

                # Sort the noise and the web traffic after time
                if(finalTime < int(currWebTrafficPacketAttrList[PACKET_ATTR_INDEX_TIME])):
                    currParsedFile.writelines([str(finalTime), ",", packetAttrList[PACKET_ATTR_INDEX_DIR], ",", packetAttrList[PACKET_ATTR_INDEX_SIZE]])
                else:
                    currParsedFile.writelines(webTrafficLines[0])
                    webTrafficLines.pop(0)

            # Done with the current filesToParse
            print("Out of lines in ", os.path.basename(fileToParsePath))
            print("Closing...")
            deviationTime = 0
            fileToParse.close()

        print("We stopped removing files")
        print("filesToParse len  = ", len(noise2train), "\n")

   #########################################################################################################################################
   #########################################################################################################################################
   #########################################################################################################################################

    # Done with the parsing
    print("Have injected all web traffic with noise")
    print(sys.argv[1],"/", len(noise2train), "(total noise files)/(noise files for training)")
    print("Ending the program")
    return

# run main 
if __name__=="__main__":
    main()




