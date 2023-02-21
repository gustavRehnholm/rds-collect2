'''
parse the noise, and clean it from any unusable packets

OBS UNTESTED

'''

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd
import statistics

from multiprocessing import Pool

# touch stdout-dir/stdout-parse.txt
# python3 rds-collect2/parser/parse.py | tee rds-collect2/parser/stdout-dir/stdout-parse.txt

def main():
    print("Start to parse the data")

    #-----------Constants------------#
    # Sec in an hour
    SEC_PER_HOUR = 60*60
    # Sec in a min
    SEC_PER_MIN = 60
    # nanoseconds in an second
    NANO_SEC_PER_SEC = 1000000000
    # Directory with the noise
    FILES_2_PARSE_DIR = "rds-collect2/parser/raw-captures/captures"
    # Directory with the noise parsed
    PARSED_FILES_DIR = "rds-collect2/parser/parsed-noise/twitch/captures-1355"
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
    warningMsg = "WARNING: This file is seen as broken and will not be part of the parsed dataset because: "


    #---info about the noise files as a whole----#
    # list of the loss streak
    listLossStreak = []
    # list of all files that where removed
    rmFilesList = []
    # list of how much data is lost in the file
    listLossPercent = []
    # List of all end times, double check that the longest and shortest log file still is around 1.9h
    endTimeList = []
    # List of the longest time between two packets for each noise file
    holeList = []
    





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

    try:
        pool = Pool()
        rmFilesList, endTimeList, listLossPercent, listLossStreak, holeList  = pool.map(parseFile, files2Parse)
    finally:
        pool.close()
        pool.join()

    rmFilesList = list(filter(None, rmFilesList))
    endTimeList.sort()
    listLossPercent.sort()
    listLossStreak.sort()
    holeList.sort()

    print("Total number of skipped files: ", len(rmFilesList))
    print("\n")
    print("Of the parsed noise files:")
    print("\n")
    print("Mean loss ratio of packets: ", statistics.mean(listLossPercent))
    print("Highest loss ratio: ", listLossPercent[-1])
    print("Mean loss streak: ", statistics.mean(listLossStreak))
    print("Highest loss streak: ", listLossStreak[-1])
    print("Mean hole time: ", statistics.mean(holeList))
    print("Highest hole time: ", holeList[-1])
    print("\n")
    print("Logfile with the longest time(ns): ", endTimeList[-1])
    print("Logfile with the shortest time(ns): ", endTimeList[0])
    print("Logfile with the longest time(h): ", endTimeList[-1]/(NANO_SEC_PER_SEC*60*60))
    print("Logfile with the shortest time(h): ", endTimeList[0]/(NANO_SEC_PER_SEC*60*60))

# takes one raw nosise file, and parse it
# returns value to: {rmFilesList, endTimeList, listLossPercent, listLossStreak, holeList}
def parseFile(fileToParsePath):
    print("New file to parse: ", os.path.basename(fileToParsePath))

    #---Info about the currently opened noise file---#
    # longest streak of lost packets in the file
    currLossStreak = 0
    currLongestLossStreak = 0
    #---to find holes of time without any packets
    prevTime = 0
    currTime = 0
    currHole = 0
    longestHole = 0

    # number of files that was removed (and the different reasons why it has been removed)
    rmFiles = 0
    rmHoleLen = 0
    rmNumPacket = 0
    rmPercentLoss = 0
    rmLossStreak = 0

    # reset counter for this packet
    currNumPacket = 0
    currNumParsedPackets = 0
    currNumSkippedPackets = 0


    with open(fileToParsePath, 'r') as fileToParse:
        print("Opening ", os.path.basename(fileToParsePath))

        
        currParsedFile = open(currParsedFiles[0], 'a') 
        print("Printing to new parsed noise file", os.path.basename(currParsedFiles[0])) 
        path = currParsedFiles[0]
        currParsedFiles.pop(0)
        

        # For every line in the noise
        # Go through the current noise file, line for line, because it might be to large for readlines()
        for parseLine in fileToParse:
            # Store the previous packets time
            prevTime = currTime

            # keep track how many packets there is in this file
            currNumPacket += 1

            # get each attribute for the current line
            splitParseLine = parseLine.split("\t")

            # get the time for the data (convert from seconds with 9 float numbers, to nanoseconds as a integer)
            parseLineTime           = splitParseLine[PACKET_ATTR_INDEX_TIME].split('.')
            timeLeftOfDotInNanoSec  = int(parseLineTime[0]) * NANO_SEC_PER_SEC
            timeRightOfDotInNanoSec = int(parseLineTime[1])
            totalTimeParseLine      =  timeLeftOfDotInNanoSec + timeRightOfDotInNanoSec
            currTime = totalTimeParseLine

            # Get the IP of the source [0] and destination [1]
            directionSplit = splitParseLine[PACKET_ATTR_INDEX_IP].split(',')

            # get the time between two packets, and the longest time which this has happened in this file
            currHole = currTime - prevTime
            if currHole > longestHole:
                longestHole = currHole

            # Set time, direction and packet size, if direction or size is missing, skip the packet  
        

            # Direction
            if(directionSplit[IP_INDEX_SENDER] == ''):
                #print("The noise packet has no IP address for the sender, skipping this noise packet")
                currNumSkippedPackets += 1
                currLossStreak += 1
                if currLongestLossStreak < currLossStreak:
                    currLongestLossStreak = currLossStreak
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
                currLossStreak += 1
                if currLongestLossStreak < currLossStreak:
                    currLongestLossStreak = currLossStreak
                continue

            
            # Do not accept an empty packet size
            if int(packetSize) == 0:
                #print("Packet size" + packetSize + " is 0, and therefore invalid")
                currNumSkippedPackets += 1
                currLossStreak += 1
                if currLongestLossStreak < currLossStreak:
                    currLongestLossStreak = currLossStreak
                continue
            elif int(packetSize) < 0:
                #print("Packet size" + packetSize + " is negative, and therefore invalid")
                currNumSkippedPackets += 1
                currLossStreak += 1
                if currLongestLossStreak < currLossStreak:
                    currLongestLossStreak = currLossStreak
                continue

            # parse the packet and incerment the counter
            currParsedFile.writelines([str(totalTimeParseLine), ",", direction, ",", packetSize, "\n"])
            currNumParsedPackets += 1
            currLossStreak = 0

        # Done with the current filesToParse
        endTimeList.append(totalTimeParseLine)
        if endTimeList[-1] != totalTimeParseLine:
            print("ERROR")
            print(endTimeList[-1])
            print(totalTimeParseLine)
            return

        currPercentLoss = currNumSkippedPackets / currNumPacket

        holeList.append(longestHole)

        if currLongestLossStreak >= 20:
            print(warningMsg)
            print("The longest time of lost packets (", currLongestLossStreak, "), is over 20")
            os.system("rm " + path)
            print("\n")
            return path
        elif currPercentLoss >= 0.05:
            print(warningMsg)
            print("The percentage loss of packets (", currPercentLoss, "), is over 5 percent")
            os.system("rm " + path)
            print("\n")
            return path
        elif (longestHole / (NANO_SEC_PER_SEC * 60)) > 2:
            print(warningMsg)
            print("The longest hole was (", longestHole / (NANO_SEC_PER_SEC * 60), "), seconds, which is larger than 3 sec")
            os.system("rm " + path)
            print("\n")
            return path
        elif currNumPacket <=  32000:
            print(warningMsg)
            print("The number of packets (", currNumPacket, "), is under 32k, meaning that it lacks to much data")
            os.system("rm " + path)
            print("\n")
            return path
        else:
            listLossPercent.append(currPercentLoss)
            listLossStreak.append(currLongestLossStreak)
            print("\n")
            print("Out of lines in ", os.path.basename(fileToParsePath))
            print("Closing...")
            print("Number of packets/lines in the file:         ", currNumPacket)
            print("Number of parsed packets/lines in the file:  ", currNumParsedPackets)
            print("Number of skipped packets/lines in the file: ", currNumSkippedPackets)
            print("Longest streak of skipped packets: ", currLongestLossStreak)
            print("Lost packages in this file: ", currPercentLoss)
            print("This files time length: ", endTimeList[-1])
            print("\n")
            fileToParse.close()
            return


            
# run main 
if __name__=="__main__":
    main()