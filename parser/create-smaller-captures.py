'''
Script to delete captures, used to test how many captures that are needed
'''

import os
from os import walk
from os import path
# to copy files
import shutil

def main():
    print("script starts\n")

    #-----------Constants------------#
    # Directory with the noise
    CAPTURES_1370 = "rds-collect2/parser/parsed-noise/twitch/captures-1355"
    CAPTURES_685  = "rds-collect2/parser/parsed-noise/twitch/captures-685"
    CAPTURES_342  = "rds-collect2/parser/parsed-noise/twitch/captures-342"
    CAPTURES_220  = "rds-collect2/parser/parsed-noise/twitch/captures-230"

    os.system("rm -f -r rds-collect2/parser/parsed-noise/twitch/captures-685")
    os.system("rm -f -r rds-collect2/parser/parsed-noise/twitch/captures-342")
    os.system("rm -f -r rds-collect2/parser/parsed-noise/twitch/captures-230")

    os.system("mkdir rds-collect2/parser/parsed-noise/twitch/captures-685")
    os.system("mkdir rds-collect2/parser/parsed-noise/twitch/captures-342")
    os.system("mkdir rds-collect2/parser/parsed-noise/twitch/captures-230")

    # List of all files to parse (aka all files in the filesToParseDir)
    files2Mv = []

    #----------------Create the directory structure----------------

    # Paths to the directories
    CAPTURES_1370_DIR = os.path.join(os.getcwd(), CAPTURES_1370)
    CAPTURES_685_DIR = os.path.join(os.getcwd(), CAPTURES_685)
    CAPTURES_342_DIR = os.path.join(os.getcwd(), CAPTURES_342)
    CAPTURES_220_DIR = os.path.join(os.getcwd(), CAPTURES_220)

    # Get list of all noise files (which will be parsed)
    for (dirpath, dirnames, filenames) in walk(CAPTURES_1370_DIR, topdown=True):
        for files in filenames:
            files2Mv.append(os.path.join(CAPTURES_1370_DIR, files))

        files2Mv.sort()
        print("Files to move: ", len(files2Mv))
        

    currFileNum = 0
    for currfile in files2Mv:
        print("New file to move: ", currfile)
        currFileNum += 1

        if currFileNum <= 230:
            shutil.copy(currfile, CAPTURES_220_DIR)
        if currFileNum <= 342:
            shutil.copy(currfile, CAPTURES_342_DIR)
        if currFileNum <= 685:
            shutil.copy(currfile, CAPTURES_685_DIR)

    # print to show that there is the right amount of files in each directory

    print("Capture-1355 contains the following number of files")
    os.system("ls rds-collect2/parser/parsed-noise/twitch/captures-1355 | wc -l")
    print("")

    print("Capture-685 contains the following number of files")
    os.system("ls rds-collect2/parser/parsed-noise/twitch/captures-685 | wc -l")
    print("")

    print("Capture-342 contains the following number of files")
    os.system("ls rds-collect2/parser/parsed-noise/twitch/captures-342 | wc -l")
    print("")

    print("Capture-230 contains the following number of files")
    os.system("ls rds-collect2/parser/parsed-noise/twitch/captures-230 | wc -l")
    print("")


# run main 
if __name__=="__main__":
    main()