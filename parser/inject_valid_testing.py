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
def InjectValidationTesting(webTrafficTestFiles, parsedTestFiles,  webTrafficValidFiles, parsedValidFiles, files2Parse):
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

    noiseTotal = len(files2Parse)

    files2Parse.sort()
    print("filesToParse len  = ", len(files2Parse), "\n")


    # Loop until both test and valid list are injected
    while(len(webTrafficTestFiles) > 0 or len(webTrafficValidFiles) > 0):

        print("New file to parse: ", os.path.basename(files2Parse[0]))

        with open(files2Parse[0], 'r') as fileToParse:
            print("Opening ", os.path.basename(files2Parse[0]))
            print("web traffic testing Files    left: "      , len(webTrafficTestFiles))
            print("web traffic validation Files left: "      , len(webTrafficValidFiles))
            print("Lines left in the open web traffic file: ", len(webTrafficLines))
            print("Noise files in total: ", noiseTotal)
            print("Noise files Left: "    , len(files2Parse))
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

                    if len(webTrafficTestFiles) > 0:
                        webTrafficFile = open(webTrafficTestFiles[0], 'r')
                        webTrafficTestFiles.pop(0)
                        webTrafficLines = webTrafficFile.readlines()
                        webTrafficFile.close()

                        currParsedFile = open(parsedTestFiles[0], 'a') 
                        parsedTestFiles.pop(0)

                    elif len(webTrafficValidFiles) > 0:

                        webTrafficFile = open(webTrafficValidFiles[0], 'r') 
                        webTrafficValidFiles.pop(0)
                        webTrafficLines = webTrafficFile.readlines()
                        webTrafficFile.close()

                        currParsedFile = open(parsedValidFiles[0], 'a') 
                        parsedValidFiles.pop(0)

                    else:
                        print("Done injecting, exiting loop")
                        continue
            
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
            print("Out of lines in ", os.path.basename(files2Parse[0]))
            print("Closing...")
            deviationTime = 0
            fileToParse.close()


        print("Popping ", os.path.basename(files2Parse[0]))
        files2Parse.pop(0)
        print("Now first one is: ", os.path.basename(files2Parse[0]))
        print("Noise files left to inject = ", len(files2Parse), "\n")
        print("\n")


    # To little noise to inject the testing and validation
    if(len(webTrafficTestFiles) > 0 or len(webTrafficValidFiles) > 0):
        print("ERROR: There was not enough noise to inject all the testing and validation web traffic")
        print("web traffic testing Files    left: "      , len(webTrafficTestFiles))
        print("web traffic validation Files left: "      , len(webTrafficValidFiles))
        print("Lines left in the open web traffic file: ", len(webTrafficLines))
        print("Noise files: ", len(files2Parse))
        print("\n")
        return [-1]
    # Has injected noise to all test and validation files
    elif(len(webTrafficTestFiles) <= 0 and len(webTrafficValidFiles) <= 0):
        print("Have injected all web traffic for validation and testing with noise")
        return noiseFilesForTrain

