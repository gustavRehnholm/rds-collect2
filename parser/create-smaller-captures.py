'''
Script to delete captures, used to test how many captures that are needed
'''

import os
from os import walk
from os import path
# to copy files
import shutil

def main():
    print("script starts")

    #-----------Constants------------#
    # Directory with the noise
    CAPTURES_1370 = "captures-1370"
    CAPTURES_685  = "captures-685"
    CAPTURES_342  = "captures-342"
    CAPTURES_171  = "captures-171"

    # List of all files to parse (aka all files in the filesToParseDir)
    files2Mv = []

    #----------------Create the directory structure----------------

    # Paths to the directories
    CAPTURES_1370_DIR = os.path.join(os.getcwd(), CAPTURES_1370)
    CAPTURES_685_DIR = os.path.join(os.getcwd(), CAPTURES_685)
    CAPTURES_342_DIR = os.path.join(os.getcwd(), CAPTURES_342)
    CAPTURES_171_DIR = os.path.join(os.getcwd(), CAPTURES_171)

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

        if currFileNum >= 171:
            shutil.copy(currfile, CAPTURES_171_DIR)
        if currFileNum >= 342:
            shutil.copy(currfile, CAPTURES_342_DIR)
        if currFileNum >= 685:
            shutil.copy(currfile, CAPTURES_685_DIR)


# run main 
if __name__=="__main__":
    main()