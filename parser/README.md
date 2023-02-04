# Parser
This directory is for all scripts and data that are needed to parse the noise, and inject it with the unrealistic webb traffic

## Pre requiste
To run the code, 3 directories needs to be present. Their names is defined in parser.py constants
* a directory "parsedFiles", where the result will be stored
* a direcotry "captures" with log files of all the noise that has been collected
* a directory "dataset" with the unrealistic webb traffic

## Data structure
the logs will be named xxxx-xxxx-xxxx.log, where the first number represents the source for the web traffic


in the code parser.py:
* make sure that the host ip address is correct

## Run the parser

python3 parser.py