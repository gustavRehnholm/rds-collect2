
import os
from os import walk
from os import path
from re import search
import pandas as pd
import random
import sys

def injectTrainingItr(webTrafficTrainFiles, parsedTrainFiles, files2Parse):

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

     # Loop until all web traffic is used, and because the training files will be used last, it is enough to check them
    while(len(webTrafficTrainFiles) > 0):

        # For every file to parse (aka the noise)
        for fileToParsePath in files2Parse:
            print("New file to parse: ", os.path.basename(fileToParsePath))

            with open(fileToParsePath, 'r') as fileToParse:

                print("Opening ", os.path.basename(fileToParsePath))
                print("web traffic training Files   left: "      , len(webTrafficTrainFiles))
                print("Lines left in the open web traffic file: ", len(webTrafficLines))
                print("Noise files to use: ", len(files2Parse))
                print("\n")

                # For every line in the noise
                # Go through the current noise file, line for line, because it might be to large for readlines()
                for parseLine in fileToParse:

                    # get each attribute for the current line
                    splitParseLine = parseLine.split("\t")
                    packetAttrList = splitParseLine[0].split(",")
                

                    #-----------------Open a new web traffic file------------------
                    if len(webTrafficLines) == 0:
                        deviationTime = int(packetAttrList[PACKET_ATTR_INDEX_TIME])

                        if len(webTrafficTrainFiles) > 0:

                            webTrafficFile = open(webTrafficTrainFiles[0], 'r') 
                            webTrafficTrainFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTrainFiles[0], 'a') 
                            parsedTrainFiles.pop(0)

                        else:
                            # Done with the parsing
                            print("Have injected all web traffic with noise")
                            return True
                
                    # Time
                    localTime = int(packetAttrList[PACKET_ATTR_INDEX_TIME])
                    finalTime = localTime - deviationTime

                    # If the current web traffic packet is empty, add the current noise packet
                    # Indicates that one should switch to a new web traffic file, but before that, one should add the noise
                    try:
                        currWebTrafficPacketAttrList = webTrafficLines[0].split(",")
                    except:
                        currParsedFile.writelines([str(finalTime), ",", 
                            packetAttrList[PACKET_ATTR_INDEX_DIR], ",", 
                            packetAttrList[PACKET_ATTR_INDEX_SIZE]])
                        print("webTrafficLines is empty, added the noise line")
                        continue

                    # Sort the noise and the web traffic after time
                    if(finalTime < int(currWebTrafficPacketAttrList[PACKET_ATTR_INDEX_TIME])):
                        currParsedFile.writelines([str(finalTime), ",", 
                            packetAttrList[PACKET_ATTR_INDEX_DIR], ",", 
                            packetAttrList[PACKET_ATTR_INDEX_SIZE]])
                    else:
                        currParsedFile.writelines(webTrafficLines[0])
                        webTrafficLines.pop(0)

                # Done with the current filesToParse
                print("Out of lines in ", os.path.basename(fileToParsePath))
                print("Closing...")
                deviationTime = 0
                fileToParse.close()
