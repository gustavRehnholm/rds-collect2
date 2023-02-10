'''
parse adn clean all the noise packets

'''

def main():


    #-----------Constants------------#
    # Sec in an hour
    SEC_PER_HOUR = 60*60
    # Sec in a min
    SEC_PER_MIN = 60
    # nanoseconds in an second
    NANO_SEC_PER_SEC = 1000000000
    # Directory with the noise
    FILES_2_PARSE_DIR = "captures"
    # Directory with the noise parsed
    PARSED_FILES_DIR = "parsed-n-cleaned-captures"
    # How much of the header to remove (to fit the noise with the web traffic)
    HEADER = 40

    # index of the different attributes
    IP_INDEX_SENDER = 0
    IP_INDEX_RECIEVER = 1
    PACKET_ATTR_INDEX_TIME = 0
    PACKET_ATTR_INDEX_IP   = 1
    PACKET_ATTR_INDEX_SIZE = 2


    #----------Variables----------#
    # Change depeding if testing or running
    logging.basicConfig(level=logging.INFO)
    # is used to get the direction of each packet
    ipHost = '10.88.0.9'
    # Current opened test/valid/train/ parsed file
    currParsedFile = []
    # List of all files to parse (aka all files in the filesToParseDir)
    files2Parse = []


    #----------------Create the directory structure----------------

    # Paths to the directories
    files2ParseDirPath = os.path.join(os.getcwd(), FILES_2_PARSE_DIR)
    parsedDirPath      = os.path.join(os.getcwd(), PARSED_FILES_DIR)

    # Get list of all noise files (which will be parsed)
    for (dirpath, dirnames, filenames) in walk(files2ParseDirPath, topdown=True):
        for files in filenames:
            files2Parse.append(os.path.join(files2ParseDirPath, files))
            currParsedFile.append(os.path.join(parsedDirPath, files))
        print("Files to parse: ", len(files2Parse))
        print("Parsed Files: ", len(currParsedFile))
'''

    #----------------------------Parsing-------------------------------------------
    '''
    Parse and inject all the noise, if their is more web traffic than noise, the noise will be reused
    '''

    print("Starting parse")
    files2Parse.sort()
    print("filesToParse len  = ", len(files2Parse), "\n")

     # For every file to parse (aka the noise)
        for fileToParsePath in files2Parse:
            print("New file to parse: ", os.path.basename(fileToParsePath))


            with open(fileToParsePath, 'r') as fileToParse:
                print("Opening ", os.path.basename(fileToParsePath))



                # For every line in the noise
                # Go through the current noise file, line for line, because it might be to large for readlines()
                for parseLine in fileToParse:

                    # get each attribute for the current line
                    splitParseLine = parseLine.split("\t")

                    # get the time for the data (convert from seconds with 9 float numbers, to nanoseconds as a integer)
                    parseLineTime           = splitParseLine[PACKET_ATTR_INDEX_TIME].split('.')
                    timeLeftOfDotInNanoSec  = int(parseLineTime[0]) * NANO_SEC_PER_SEC
                    timeRightOfDotInNanoSec = int(parseLineTime[1])
                    totalTimeParseLine      =  timeLeftOfDotInNanoSec + timeRightOfDotInNanoSec

                    # Get the IP of the source [0] and destination [1]
                    directionSplit = splitParseLine[PACKET_ATTR_INDEX_IP].split(',')
                

                    #-----------------Open a new web traffic file------------------

                    # Check if a new web traffic file needs to be loaded
                    if len(webTrafficLines) == 0:
                        deviationTime = totalTimeParseLine 

                        # check which type of web traffic to get, and get the file the result will be written to

                        if len(webTrafficTestFiles) > 0:
                            webTrafficFile = open(webTrafficTestFiles[0], 'r')
                            webTrafficTestFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTestFiles[0], 'a') 
                            print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                            parsedTestFiles.pop(0)

                        elif len(webTrafficValidFiles) > 0:

                            webTrafficFile = open(webTrafficValidFiles[0], 'r') 
                            webTrafficValidFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedValidFiles[0], 'a') 
                            print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                            parsedValidFiles.pop(0)

                        elif len(webTrafficLines) == 0  and len(webTrafficTrainFiles) > 0:

                            webTrafficFile = open(webTrafficTrainFiles[0], 'r') 
                            webTrafficTrainFiles.pop(0)
                            webTrafficLines = webTrafficFile.readlines()
                            webTrafficFile.close()

                            currParsedFile = open(parsedTrainFiles[0], 'a') 
                            print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                            parsedTrainFiles.pop(0)

                        else:
                            # Done with the parsing
                            print("Have injected all web traffic with noise")
                            print("Ending the program")
                            return

                    # Set time, direction and packet size, if direction or size is missing, skip the packet  
                
                    # Time
                    finalTime = totalTimeParseLine - deviationTime

                    # Direction
                    if(directionSplit[IP_INDEX_SENDER] == ''):
                        print("The noise packet has no IP address for the sender, skipping this noise packet")
                        continue
                    if (directionSplit[IP_INDEX_SENDER] == ipHost):
                        direction = 's'
                    elif(directionSplit[IP_INDEX_RECIEVER] == ipHost):
                        direction = 'r'
                    # If the IP_HOST is wrong, choose the one that start with an 10 as the host
                    else:
                        checkIfLocal = directionSplit[IP_INDEX_SENDER].split('.')
                        if checkIfLocal[0] == '10':
                            ipHost = directionSplit[0]
                        else: ipHost = directionSplit[1]

                    # Size
                    try:
                        packetSize = str(int(splitParseLine[PACKET_ATTR_INDEX_SIZE])-HEADER)
                    except:
                        print("splitParseLine[2] = " + splitParseLine[2] + " could not be used to determine the packet Size, skipped")
                        continue

                    
                    # Do not accept an empty packet size
                    if int(packetSize) == 0:
                        print("Packet size" + packetSize + " is 0, and therefore invalid")
                        continue
                    

                    # If the current web traffic packet is empty, add the current noise packet
                    # Indicates that one should switch to a new web traffic file, but before that, one should add the noise
                    # TODO: make sure that this does not cause any problem
                    # TODO: might want to rm the print 
                    try:
                        currWebTrafficPacketAttrList = webTrafficLines[0].split(",")
                    except:
                        currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                        print("Crossline is empty, added the noise line")
                        continue

                    # Sort the noise and the web traffic after time
                    if(finalTime < int(currWebTrafficPacketAttrList[PACKET_ATTR_INDEX_TIME])):
                        currParsedFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                    else:
                        currParsedFile.writelines(webTrafficLines[0])
                        webTrafficLines.pop(0)

                # Done with the current filesToParse
                print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
                deviationTime = 0
                fileToParse.close()

            # If more web traffic, go to the next file to be parsed (next noise file)
            if(len(webTrafficTestFiles) > 0 and len(webTrafficValidFiles) > 0):
                print("Popping ", os.path.basename(files2Parse[0]))
                files2Parse.pop(0)
                print("Now first one is: ", os.path.basename(files2Parse[0]), "\n")
            else: print("We stopped removing files")
'''

# run main 
if __name__=="__main__":
    main()