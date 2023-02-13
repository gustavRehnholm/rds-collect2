'''
parse the noise, and clean it from any unusable packets


'''

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd

# touch stdout-dir/stdout-parse.txt
# python3 parse.py | tee stdout-dir/stdout-parse.txt

def main():

    #-----------Constants------------#
    # Sec in an hour
    SEC_PER_HOUR = 60*60
    # Sec in a min
    SEC_PER_MIN = 60
    # nanoseconds in an second
    NANO_SEC_PER_SEC = 1000000000
    # Directory with the noise
    FILES_2_PARSE_DIR = "raw-captures/captures"
    # Directory with the noise parsed
    PARSED_FILES_DIR = "parsed-noise/twitch/captures-1370"
    # How much of the header to remove (to fit the noise with the web traffic)
    HEADER = 40

    # index of the different attributes
    IP_INDEX_SENDER   = 0
    IP_INDEX_RECIEVER = 1
    PACKET_ATTR_INDEX_TIME = 0
    PACKET_ATTR_INDEX_IP   = 1
    PACKET_ATTR_INDEX_SIZE = 2

    #----------Variables----------#
    # is used to get the direction of each packet
    ipHost = '10.88.0.9'
    # Current opened test/valid/train/ parsed file
    currParsedFiles= []
    # List of all files to parse (aka all files in the filesToParseDir)
    files2Parse = []
    # List of all end times, double check that the longest and shortest log file still is around 1.9h
    endTimeList = []

    # total number of packets that was in the unparsed noise files
    numPackets = 0
    # total number of successfully parsed packets
    numParsedPackets = 0
    # total number of packets that could not be parsed
    numSkippedPackets = 0

    # this files number of packets
    currNumPacket = 0
    # this files number of successfully packets
    currNumParsedPackets = 0
    # this files number of skipped packets
    currNumSkippedPackets = 0


    #----------------Create the directory structure----------------

    # Paths to the directories
    files2ParseDirPath = os.path.join(os.getcwd(), FILES_2_PARSE_DIR)
    parsedDirPath      = os.path.join(os.getcwd(), PARSED_FILES_DIR)

    os.system("rm -f -r " + PARSED_FILES_DIR)
    os.system("mkdir " + PARSED_FILES_DIR)

    # Get list of all noise files (which will be parsed)
    for (dirpath, dirnames, filenames) in walk(files2ParseDirPath, topdown=True):
        for files in filenames:
            files2Parse.append(os.path.join(files2ParseDirPath, files))
            currParsedFiles.append(os.path.join(parsedDirPath, files))
        print("Files to parse: ", len(files2Parse))
        print("Parsed Files: ", len(currParsedFiles))



    #----------------------------Parsing-------------------------------------------

    print("Starting parse")
    files2Parse.sort()
    print("filesToParse len  = ", len(files2Parse), "\n")

    currIndex = -1

    # For every file to parse (aka the noise)
    for fileToParsePath in files2Parse:
        print("New file to parse: ", os.path.basename(fileToParsePath))

        # increment the index (to indicate to the user how long the program must run)
        currIndex += 1
        # total number of packets
        numPackets += currNumPacket
        # successfully packets
        numParsedPackets += currNumParsedPackets
        # packets that could not be parsed
        numSkippedPackets += currNumSkippedPackets
        # reset counter for this packet
        currNumPacket = 0
        currNumParsedPackets = 0
        currNumSkippedPackets = 0


        with open(fileToParsePath, 'r') as fileToParse:
            #print("\n")
            print(currIndex , "/", len(files2Parse), " files left")
            print("Opening ", os.path.basename(fileToParsePath))

            currParsedFile = open(currParsedFiles[0], 'a') 
            print("Printing to new parsed noise file", os.path.basename(currParsedFiles[0])) 
            #print("\n")
            currParsedFiles.pop(0)

            # For every line in the noise
            # Go through the current noise file, line for line, because it might be to large for readlines()
            for parseLine in fileToParse:

                # keep track how many packets there is in this file
                currNumPacket += 1

                # get each attribute for the current line
                splitParseLine = parseLine.split("\t")

                # get the time for the data (convert from seconds with 9 float numbers, to nanoseconds as a integer)
                parseLineTime           = splitParseLine[PACKET_ATTR_INDEX_TIME].split('.')
                timeLeftOfDotInNanoSec  = int(parseLineTime[0]) * NANO_SEC_PER_SEC
                timeRightOfDotInNanoSec = int(parseLineTime[1])
                totalTimeParseLine      =  timeLeftOfDotInNanoSec + timeRightOfDotInNanoSec

                # Get the IP of the source [0] and destination [1]
                directionSplit = splitParseLine[PACKET_ATTR_INDEX_IP].split(',')

                # Set time, direction and packet size, if direction or size is missing, skip the packet  
            

                # Direction
                if(directionSplit[IP_INDEX_SENDER] == ''):
                    #print("The noise packet has no IP address for the sender, skipping this noise packet")
                    currNumSkippedPackets += 1
                    continue
                elif (directionSplit[IP_INDEX_SENDER] == ipHost):
                    direction = 's'
                elif(directionSplit[IP_INDEX_RECIEVER] == ipHost):
                    direction = 'r'
                # If the IP_HOST is wrong, choose the one that start with an 10 as the host
                else:
                    checkIfLocal = directionSplit[IP_INDEX_SENDER].split('.')
                    if checkIfLocal[0] == '10':
                        ipHost = directionSplit[0]
                        direction = 's'
                    else: 
                        ipHost = directionSplit[1]
                        direction = 'r'

                # Size
                try:
                    packetSize = str(int(splitParseLine[PACKET_ATTR_INDEX_SIZE])-HEADER)
                except:
                    #print("splitParseLine[2] = " + splitParseLine[2] + " could not be used to determine the packet Size, skipped")
                    currNumSkippedPackets += 1
                    continue

                
                # Do not accept an empty packet size
                if int(packetSize) == 0:
                    #print("Packet size" + packetSize + " is 0, and therefore invalid")
                    currNumSkippedPackets += 1
                    continue
                elif int(packetSize) < 0:
                    #print("Packet size" + packetSize + " is negative, and therefore invalid")
                    currNumSkippedPackets += 1
                    continue

                # parse the packet and incerment the counter
                currParsedFile.writelines([str(totalTimeParseLine), ",", direction, ",", packetSize, "\n"])
                currNumParsedPackets += 1



            # Done with the current filesToParse
            endTimeList.append(totalTimeParseLine)
            if endTimeList[-1] != totalTimeParseLine:
                print("ERROR")
                print(endTimeList[-1])
                print(totalTimeParseLine)
                return

            print("\n")
            print("Out of lines in ", os.path.basename(fileToParsePath))
            print("Closing...")
            print("Number of packets/lines in the file:         ", currNumPacket)
            print("Number of parsed packets/lines in the file:  ", currNumParsedPackets)
            print("Number of skipped packets/lines in the file: ", currNumSkippedPackets)
            print("This files time lenght: ", endTimeList[-1])
            print("\n")
            fileToParse.close()

    endTimeList.sort()

    print("Total number of packets/lines:         ", numPackets)
    print("Total number of parsed packets/lines:  ", numParsedPackets)
    print("Total number of skipped packets/lines: ", numSkippedPackets)
    print("Logfile with the longest time: ", endTimeList[-1])
    print("Logfile with the shortest time: ", endTimeList[0])

# run main 
if __name__=="__main__":
    main()