# Parser
This directory is for all scripts that are needed to clean parse the noise, parse it, and inject it with the unrealistic webb traffic

## Core function
It sort all web traffic after if it is for validation, testing or training. It will first make sure that all 

## Pre requiste
To run the code, 3 directories needs to be present. Their names is defined in parser.py constants
* a directory "parsedFiles", where the result will be stored
* a directory "captures-raw" with log files of all the noise that has been collected
* a directory "captures" to store the parsed and cleaned captures
* a directory "dataset" with the unrealistic webb traffic

The code it self will also need to be modified:
* make sure that the host ip address is correct for the noise traffic that one will parse and inject

## Data structure
Bellow will the structure of the directories data be explained.



### unrealistic web traffic
it is stored in the directory dataset, there it has 10 fold files, but for this work, only fold-0.csv will be used. The fold files is structured with the attributes:

* class: the site id number
* site: the webpage the data is generated with
* subpage: subpage of the site
* img: pointer to a visual representation of the data
* log: pointer to the data of the packet
* is_train: boolean, if the data should be used to train the ML
* is_valid: boolean, if the data should be used for validation
* is_test: boolean, it the data should e used for testing

THe log files is in the subdirectory client(for collection at the client side), where it has a directory for each class (as defined in the fold file). The log files is named xxxx-xxxx-xxxx.log, where the first number is for the class, the second one is for the subpage, and the last id of the individual packet for that site and subsite. The log files is structured with the following attributes:

* time: time when the packet was sent in nanoseconds (integer)
* direction: if the packet was sent or received, stored as a s or a r
* size: size in bytes for the packet

### unparsed noise
the unparsed noise is stored in the directory captures, where it has multiple log files for each time noise has been captured.

will have 4 attributes: 
* time in seconds (with 9 float number)
* IP address of the sender
* IP address of the receiver
* packet size in bytes

### Parsed data
The parsed data will have the same structure as the unrealistic web traffic, but with the noise injected in each web traffic log file, and there will not be any fold file. 


## Run the parser

python3 parse-n-inject-rnd.py | tee output.txt


