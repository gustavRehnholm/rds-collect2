
import shutil

def addTrain(webTrafficTrainFiles, parsedTrainFiles):

    for i in range(0, len(webTrafficTrainFiles)):
        shutil.copy(webTrafficTrainFiles[0], parsedTrainFiles[0])

    return True
