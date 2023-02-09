#!/usr/bin/env python

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd

hours = 60*60
minutes = 60
nanoseconds = 1000000000
saveTime = time.time()
IP_host = '10.88.0.9'
filesToParseDir = "captures"
parsedFilesDir = "parsedFiles-ittr-1"
crossFilesDir = "dataset"
excelFile = "dataset/fold-0.csv"
header = 40

deviationTime = 0
crossFilePath = []
newFilePath = []
newFile = []
crossLine = []
filesToParse = []

trainFiles = []
validFiles = []
testFiles = []
parsedTrainFiles = []
parsedValidFiles = []
parsedTestFiles = []

masterFile = os.path.join(os.getcwd(), filesToParseDir)
parsedDirectory = os.path.join(os.getcwd(), parsedFilesDir)
directory = os.path.join(os.getcwd(), crossFilesDir)

for (dirpath, dirnames, filenames) in walk(masterFile, topdown=True):
    for files in filenames:
        filesToParse.append(os.path.join(masterFile, files))
    print("Files to parse: ", len(filesToParse))
print("Setting up directories")
for (dirpath, dirnames, filenames) in walk(directory, topdown=True):
    for dirs in dirnames:
        try: 
            os.mkdir(os.path.join(parsedDirectory, dirs))
        except: 
            print("File and directory exists!") 

#----------------------limited data data set sorting--------------------

df = pd.read_csv(excelFile)
dfFormat = ['log', 'is_train', 'is_valid', 'is_test']
dfFiles = df[dfFormat]

for x in range(0, len(dfFiles['log'])):
    if(dfFiles['is_train'][x] == True): 
        parsedTrainFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
        trainFiles.append(os.path.join(directory, "client", dfFiles['log'][x]))
    elif(dfFiles['is_valid'][x] == True): 
        parsedValidFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
        validFiles.append(os.path.join(directory, "client", dfFiles['log'][x]))
    else: 
        parsedTestFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
        testFiles.append(os.path.join(directory, "client", dfFiles['log'][x]))

#-----------------------------------------------------------------------

print("Starting parse")
print("trainFiles len = ", len(trainFiles))
filesToParse.sort()
print("filesToParse len  = ", len(filesToParse), "\n")

while(len(trainFiles) > 0):

    for fileToParsePath in filesToParse:

        # quit without looping through all noise files
        if(len(trainFiles) > 0):
            exit

        print("New file to parse: ", os.path.basename(fileToParsePath))
        with open(fileToParsePath, 'r') as fileToParse:
            print("Opening ", os.path.basename(fileToParsePath))
            
            print("testingFiles    left: "           , len(testFiles))
            print("validationFiles left: "           , len(validFiles))
            print("trainingFiles   left: "           , len(trainFiles))
            print("Lines left in crossfile: "        , len(crossLine))
            print("Noise files left in fileToParse: ", len(filesToParse))
            print("\n")

            for parseLine in fileToParse: #Reading line by line from the master file since it might be to large to do readlines() on
                splitParseLine = parseLine.split("\t")
                parseLineTime = splitParseLine[0].split('.')
                totalTime = int(parseLineTime[0]) * nanoseconds
                totalTime += int(parseLineTime[1])

                directionSplit = splitParseLine[1].split(',')
                
                #-------------------limited files open test, valid then training-----------------------
                if (not len(crossLine) and len(testFiles) > 0): #Check if it's time to preload a new file
                    deviationTime = totalTime #make deviation to match start at zero

                    crossFile = open(testFiles[0], 'r') #File from Tobias set
                    testFiles.pop(0)
                    
                    crossLine = crossFile.readlines()
                    crossFile.close()

                    newFile = open(parsedTestFiles[0], 'a') #What we write to
                    print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                    parsedTestFiles.pop(0)

                elif (not len(crossLine) and len(validFiles) > 0): #Check if it's time to preload a new file
                    deviationTime = totalTime #make deviation to match start at zero

                    crossFile = open(validFiles[0], 'r') #File from Tobias set
                    validFiles.pop(0)
                    
                    crossLine = crossFile.readlines()
                    crossFile.close()

                    newFile = open(parsedValidFiles[0], 'a') #What we write to
                    print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                    parsedValidFiles.pop(0)

                elif (not len(crossLine) and len(trainFiles) > 0):
                    deviationTime = totalTime #make deviation to match start at zero

                    crossFile = open(trainFiles[0], 'r') #File from Tobias set
                    trainFiles.pop(0)
                    
                    crossLine = crossFile.readlines()
                    crossFile.close()

                    newFile = open(parsedTrainFiles[0], 'a') #What we write to
                    print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                    parsedTrainFiles.pop(0)

                #-------------------------rewrite this shit code above to take less lines, this looks abyssmal---------------

                finalTime = totalTime - deviationTime

                # Get direction, and if their is none, continue
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

                # If the current crossLine is empty, skip it and pop it from the list
                try: 
                    splitCrossLine = crossLine[0].split(",")
                except:
                    print("Crossline is empty")
                    crossLine.pop(0)
                    continue

                # If there is lacking a packet size in the current noise packet, skip it
                try:
                    packetSize = str(int(splitParseLine[2])-header)
                except:
                    print("splitParseLine[2] = " + splitParseLine[2] + " could not be used to determine the packet Size, can not use this noise packet")
                    continue

                if(finalTime < int(splitCrossLine[0])):
                    newFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                    saveTime = totalTime
                else:
                    newFile.writelines(crossLine[0])
                    crossLine.pop(0)

            print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
            deviationTime = 0
            fileToParse.close()

        if(len(testFiles) > 0 and len(validFiles) > 0):
            print("Popping ", os.path.basename(filesToParse[0]))
            filesToParse.pop(0)
            print("Now first one is: ", os.path.basename(filesToParse[0]), "\n")
        else: 
            print("We stopped removing files")