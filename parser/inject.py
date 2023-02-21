'''
Inject parsed noise to the web traffic
Is best to run from the script: script-inject
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
from add_training_web_traffic import addTrain

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
    FILES_2_INJECT_DIR = "rds-collect2/parser/parsed-noise/twitch/captures-" + str(length)
    # Directory with the result
    INJECTED_FILES_DIR = "rds-collect2/parser/injected-datasets/twitch/parsedFiles-" + choice + "-" + str(length)
    # Directory with the web traffic
    WEB_TRAFFIC_FILES_DIR = "rds-collect2/parser/dataset/client"
    # Information about what the different web traffics should be used for on the WF (training, validation, testing)
    FOLD0_CSV = "rds-collect2/parser/dataset/fold-0.csv"

    # index of the different attributes
    PACKET_ATTR_INDEX_TIME  = 0
    PACKET_ATTR_INDEX_DIR   = 1
    PACKET_ATTR_INDEX_SIZE  = 2

    #----------Variables----------#
    # List of all the noise, which should be injected into the web traffic
    files2Inject = []

    # files with the webTraffic
    webTrafficTrainFiles = []
    webTrafficValidFiles = []
    webTrafficTestFiles  = []
    # Files for the parsed noise
    injectedTrainFiles = []
    injectedValidFiles = []
    injectedTestFiles  = []


    #----------------Create the directory structure----------------

    # Paths to the directories
    files2InjectDirPath = os.path.join(os.getcwd(), FILES_2_INJECT_DIR)
    injectedDirPath      = os.path.join(os.getcwd(), INJECTED_FILES_DIR)
    webTrafficDirPath  = os.path.join(os.getcwd(), WEB_TRAFFIC_FILES_DIR)

    # Get list of all noise files (which will be parsed)
    for (dirpath, dirnames, filenames) in walk(files2InjectDirPath, topdown=True):
        for files in filenames:
            files2Inject.append(os.path.join(files2InjectDirPath, files))
        print("Files to parse: ", len(files2Inject))
    print("Setting up directories")

    # Create the structure for the result directory, so it match the web traffics
    os.system("rm -f -r " + INJECTED_FILES_DIR)
    os.system("mkdir " + INJECTED_FILES_DIR)

    for (dirpath, dirnames, filenames) in walk(webTrafficDirPath, topdown=True):
        for dirs in dirnames:
            try: 
                os.mkdir(os.path.join(injectedDirPath, dirs))
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
            injectedTrainFiles.append(os.path.join(injectedDirPath, dfFiles['log'][x]))
            webTrafficTrainFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        elif(dfFiles['is_valid'][x] == True): 
            injectedValidFiles.append(os.path.join(injectedDirPath, dfFiles['log'][x]))
            webTrafficValidFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        elif(dfFiles['is_test'][x] == True): 
            injectedValidFiles.append(os.path.join(injectedDirPath, dfFiles['log'][x]))
            webTrafficTestFiles.append(os.path.join(webTrafficDirPath, dfFiles['log'][x]))
        else:
            print("ERROR a packet in the web traffic is neither for training, validation or testing in the fold-0 file.")
            print("Aborting the program")
            return

    print("Starting injecting noise")
    print("trainFiles len = ", len(webTrafficTrainFiles))

    noise2train = InjectValidationTesting(webTrafficTestFiles, injectedValidFiles,  webTrafficValidFiles, injectedValidFiles, files2Inject, choice, length)

    if(noise2train[0] == -1):
        print("ERROR: Injection of the valid and testing web traffic has failed")
        print("Aborting the program")
        return

    if(choice == "itr"):
        successfully = injectTrainingItr(webTrafficTrainFiles, injectedTrainFiles, noise2train, choice, length)
    elif(choice == "rnd"):
        successfully = injectTrainingRnd(webTrafficTrainFiles, injectedTrainFiles, noise2train, choice, length)
    elif(choice == "none"):
        successfully = addTrain(webTrafficTrainFiles, injectedTrainFiles)
    else:
        print("ERROR: the value of choice has been changed: ", choice)
        print("Aborting program")
        return

    if(successfully):
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




