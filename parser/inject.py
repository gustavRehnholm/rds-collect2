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

# Help functions for injecting different web traffic, and do it in different manners
from inject_valid_testing import InjectValidationTesting
from inject_training_itr import injectTrainingItr
from inject_training_rnd import injectTrainingRnd

def main():
    length = sys.argv[1]
    choice = sys.argv[2]

    if(choice == "itr"):
        print("The script will used the capture-", length, " file and inject the training data iterative")
    elif(choice == "rnd"):
        print("The script will used the capture-", length, " file and inject the training data randomly")
    elif(choice == "none"):
        print("The script will used the capture-", length, " file and inject no training data")
    else:
        print(choice, " Is an invalid choice, must be itr, rnd or none")
        print("Aborting program")
        return

    #-----------Constants------------#
    # Directory with the noise
    FILES_2_PARSE_DIR = "parsed-noise/twitch/captures-" + str(length)
    # Directory with the result
    PARSED_FILES_DIR = "injected-datasets/twitch/parsedFiles-" + choice + "-" + str(length)
    # Directory with the web traffic
    WEB_TRAFFIC_FILES_DIR = "dataset-test/client"
    # Information about what the different web traffics should be used for on the WF (training, validation, testing)
    FOLD0_CSV = "dataset-test/fold-0-test.csv"

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
            print("Aborting the program")
            return

    print("Starting injecting noise")
    print("trainFiles len = ", len(webTrafficTrainFiles))

    noise2train = InjectValidationTesting(webTrafficTestFiles, parsedTestFiles,  webTrafficValidFiles, parsedValidFiles, files2Parse)

    if(noise2train[0] == -1):
        print("ERROR: Injection of the valid and testing web traffic has failed")
        print("Aborting the program")
        return

    if(choice == "itr"):
        successfully = injectTrainingItr(webTrafficTrainFiles, parsedTrainFiles, noise2train)
    elif(choice == "rnd"):
        successfully = injectTrainingRnd(webTrafficTrainFiles, parsedTrainFiles, noise2train)
    elif(choice == "none"):
        successfully = True
    else:
        print("ERROR: the value of choice has been changed: ", choice)
        print("Aborting program")
        return

    if(successfully):
        # Done with the injection
        print("Have injected all web traffic with noise, after the choice: ", choice)
        print("Total noise files: ", sys.argv[1])
        print("Noise files for testing and validation: ", int(sys.argv[1]) - len(noise2train))
        print("Noise files for training: ", len(noise2train))
        print("Ending the program")
        return
    else:
        print("Failed to inject the noise")
        return

# run main 
if __name__=="__main__":
    main()




