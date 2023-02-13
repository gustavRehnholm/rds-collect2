'''
Help function to inject noise into the validation and testing data
'''
import os
from os import walk
from os import path
from re import search
import pandas as pd
import random
import sys

# inject noise for the validation and testing
def InjectValidationTesting(webTrafficTestFiles, webTrafficValidFiles, files2Parse):
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

    files2Parse.sort()
    print("filesToParse len  = ", len(files2Parse), "\n")

    # Itterativt add test and validation files
    while(len(webTrafficTestFiles) > 0 and len(webTrafficValidFiles) > 0):

        # For every file to inject (aka the noise)
        for fileToParsePath in files2Parse:
            print("New file to parse: ", os.path.basename(fileToParsePath))


            with open(fileToParsePath, 'r') as fileToParse:
                print("Opening ", os.path.basename(fileToParsePath))

                print("web traffic testing Files    left: "      , len(webTrafficTestFiles))
                print("web traffic validation Files left: "      , len(webTrafficValidFiles))
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

                        if len(webTrafficTestFiles) > 0:
                            webTrafficFile = open(webTrafficTestFiles[0], 'r')
                            webTrafficTestFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTestFiles[0], 'a') 
                            #print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                            parsedTestFiles.pop(0)

                        elif len(webTrafficValidFiles) > 0:

                            webTrafficFile = open(webTrafficValidFiles[0], 'r') 
                            webTrafficValidFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedValidFiles[0], 'a') 
                            #print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                            parsedValidFiles.pop(0)

                        else:
                            # Done with the parsing fo the testing and validating files
                            print("Have injected all web traffic for validation and testing with noise")
                            return files2Parse

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


            print("Popping ", os.path.basename(files2Parse[0]))
            files2Parse.pop(0)
            print("Now first one is: ", os.path.basename(files2Parse[0]))
            print("filesToParse len  = ", len(files2Parse), "\n")
            print("\n")

    return files2Parse

