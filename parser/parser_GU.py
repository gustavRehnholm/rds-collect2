#!/usr/bin/env python

"""
There needs to be 2 directories in the cwd
* webbtrafficFiles: the web traffic
* files2Parse: the noise

At webbtrafficFiles:


At files2Parse:
The noise has one log file per twitch stream (Different streams, date and time)
They are structured after: time, IP, IP, size


To get a result, noise and web traffic needs to be in their corresponding directory

In the end, the result will be in the directory cwd/parsedFiles
"""


import os
from os import walk
from os import path
from re import search
import time
import pandas as pd

#-----------Constants------------#
# Sec in an hour
hours = 60*60
# Sec in a min
minutes = 60
# nanoseconds in an second
nanoseconds = 1000000000
# To store the total time of the parsed line that one is working on at the moment
currTotalTimeParseLine = time.time()
# is used to get the direction of each packet
IP_host = '10.88.0.9'
# Directory with the noise
files2ParseDir = "captures"
# Directory with the result
parsedFilesDir = "parsedFiles"
# Directory with the web traffic
webbTrafficFilesDir = "dataset"
# the result file name
fold0csv = "dataset/fold-0.csv"
# How much of the header to remove (to fit the noise with the web traffic)
header = 40

#----------Variables----------#
# To standardize the time of each packet
deviationTime = 0
#crossFilePath = []
#newFilePath = []
# Current opened test/valid/train/ parsed file
currParsedFile = []
# all line in the crossfile (aka the unrealistic web traffic)
crossLine = []
# List of all files to parse (aka all files in the filesToParseDir)
files2Parse = []

# files with the webb traffic
crossTrainFiles = []
crossValidFiles = []
crossTestFiles  = []
# Files for the parsed noise
parsedTrainFiles = []
parsedValidFiles = []
parsedTestFiles  = []

# Paths to the directories
files2ParseDirPath = os.path.join(os.getcwd(), files2ParseDir)
parsedDirPath      = os.path.join(os.getcwd(), parsedFilesDir)
webbTrafficDirPath  = os.path.join(os.getcwd(), webbTrafficFilesDir)

# Get all files with noise to parse
for (dirpath, dirnames, filenames) in walk(files2ParseDirPath, topdown=True):
    for files in filenames:
        files2Parse.append(os.path.join(files2ParseDirPath, files))
    print("Files to parse: ", len(files2Parse))
print("Setting up directories")

# Create the result directory
for (dirpath, dirnames, filenames) in walk(webbTrafficDirPath, topdown=True):
    for dirs in dirnames:
        try: 
            os.mkdir(os.path.join(parsedDirPath, dirs))
        except: 
            print("File and directory exists!") 


#----------------------limited data data set sorting--------------------

# dfFiles: The webb traffic
df       = pd.read_csv(fold0csv)
dfFormat = ['log', 'is_train', 'is_valid', 'is_test']
dfFiles  = df[dfFormat]


# Separate the train/valid/test packets of the webb traffic, and make sure that their is one correlating noise packet for each one
# GR: numValidationPackets = 0
# GR: numTestPackets       = 0
for x in range(0, len(dfFiles['log'])):
    if(dfFiles['is_train'][x] == True): 
        parsedTrainFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        crossTrainFiles.append(os.path.join(webbTrafficDirPath,"client", dfFiles['log'][x]))
        # GR: trainIndexes.append(x)
    elif(dfFiles['is_valid'][x] == True): 
        parsedValidFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        crossValidFiles.append(os.path.join(webbTrafficDirPath,"client", dfFiles['log'][x]))
        # GR: numValidationPackets +=1
    # is_test
    else: 
        parsedTestFiles.append(os.path.join(parsedDirPath, dfFiles['log'][x]))
        crossTestFiles.append(os.path.join(webbTrafficDirPath,"client", dfFiles['log'][x]))
        # GR: numTestPackets +=1

# TODO: GR: 
# 1: Se hur mycket noise som saknas för att fylla tränings settet
#       num_duplicate_noise = len(trainIndexes) - (num_noise - (numValidationPackets + numTestPackets))
# 3: utöka noise (hur?)
# 4: spara noise datan 

#----------------------------Parsing-------------------------------------------

print("Starting parse")
print("trainFiles len = ", len(crossTrainFiles))
files2Parse.sort()
print("filesToParse len  = ", len(files2Parse), "\n")

# For every web traffic training data
# It is the longest one, which is why the loop checks that specific one
while(len(crossTrainFiles) > 0):

    # For every file to parse (aka the noise)
    for fileToParsePath in files2Parse:
        print("New file to parse: ", os.path.basename(fileToParsePath))

        with open(fileToParsePath, 'r') as fileToParse:
            print("Opening ", os.path.basename(fileToParsePath))

            print("testingFiles    left: ", len(crossTestFiles))
            print("validationFiles left: ", len(crossValidFiles))
            print("trainingFiles   left: ", len(crossTrainFiles))
            print("Lines left in crossfile: ", len(crossLine))
            print("\n")

            # For every line in the noise
            # Do it lien per line, because the file might be to large for readlines()
            for parseLine in fileToParse:
                splitParseLine = parseLine.split("\t")

                # get the time for the data
                parseLineTime       = splitParseLine[0].split('.')
                totalTimeParseLine  = int(parseLineTime[0]) * nanoseconds
                totalTimeParseLine += int(parseLineTime[1])

                # Get the IP, that the direction will be extracted from
                directionSplit = splitParseLine[1].split(',')
                
                #-------------------limited files open test, valid then training-----------------------
                """
                Extract one web traffic packet and the file it should merge to (in crossLine and currParsedFile)
                """
                if (not len(crossLine) and len(crossTestFiles) > 0): #Check if it's time to preload a new file
                    deviationTime = totalTimeParseLine #make deviation to match start at zero

                    # get the current web traffic packet
                    crossFile = open(crossTestFiles[0], 'r') #File from Tobias set
                    crossTestFiles.pop(0)
                    crossLine = crossFile.readlines()
                    crossFile.close()
                    # get current parsed
                    currParsedFile = open(parsedTestFiles[0], 'a') #What we write to
                    print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                    parsedTestFiles.pop(0)

                elif (not len(crossLine) and len(crossValidFiles) > 0): #Check if it's time to preload a new file
                    deviationTime = totalTimeParseLine #make deviation to match start at zero

                    crossFile = open(crossValidFiles[0], 'r') #File from Tobias set
                    crossValidFiles.pop(0)
                    crossLine = crossFile.readlines()
                    crossFile.close()

                    currParsedFile = open(parsedValidFiles[0], 'a') #What we write to
                    print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                    parsedValidFiles.pop(0)

                elif (not len(crossLine) and len(crossTrainFiles) > 0):
                    deviationTime = totalTimeParseLine #make deviation to match start at zero

                    crossFile = open(crossTrainFiles[0], 'r') #File from Tobias set
                    crossTrainFiles.pop(0)
                    crossLine = crossFile.readlines()
                    crossFile.close()

                    currParsedFile = open(parsedTrainFiles[0], 'a') #What we write to
                    print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                    parsedTrainFiles.pop(0)


                #-------------------------TODO: rewrite this shit code above to take less lines, this looks abyssmal---------------

                # Time for the packets travel
                finalTime = totalTimeParseLine - deviationTime

                # TODO: add continue for when packet size is missing but IP exists. 

                # Get noise packet direction
                if(directionSplit[0] == ''):
                    continue
                if (directionSplit[0] == IP_host):
                    direction = 's'
                elif(directionSplit[1] == IP_host):
                    direction = 'r'
                else:
                    checkIfLocal = directionSplit[0].split('.')
                    if checkIfLocal[0] == '10':
                        IP_host = directionSplit[0]
                    else: IP_host = directionSplit[1]

                #if(int(splitParseLine[2]) > 1420): splitParseLine[2] = '1420\n'
                splitCrossLine = crossLine[0].split(",")

                # get packet size of the noise
                packetSize = str(int(splitParseLine[2])-header)


                # Sort the noise and the web traffic after time
                # write all noise that are shorter than the current webb traffic packet
                if(finalTime < int(splitCrossLine[0])):
                    currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                    currTotalTimeParseLine = totalTimeParseLine
                # if the webb traffic packet is the next one, write it to the parsed list
                else:
                    currParsedFile.writelines(crossLine[0])
                    crossLine.pop(0)

            # Done with the current filesToParse
            print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
            deviationTime = 0
            fileToParse.close()

        # If more to parse, continiue, else end the parsing
        if(len(crossTestFiles) > 0 and len(crossValidFiles) > 0):
            print("Popping ", os.path.basename(files2Parse[0]))
            files2Parse.pop(0)
            print("Now first one is: ", os.path.basename(files2Parse[0]), "\n")
        else: print("We stopped removing files")
