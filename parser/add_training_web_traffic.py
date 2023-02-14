
import shutil

def addTrain(webTrafficTrainFiles, parsedTrainFiles):

    # add all web traffic train files
    for i in range(0, len(webTrafficTrainFiles)):
        webTrafficFile = open(webTrafficTrainFiles[i], 'r') 
        webTrafficLines = webTrafficFile.readlines()
        webTrafficFile.close()

        currParsedFile = open(parsedTrainFiles[i], 'a') 

        # add every line from the web traffic file that is open
        for j in range(0, len(webTrafficLines)):
            currParsedFile.writelines(webTrafficLines[j])

    return True
