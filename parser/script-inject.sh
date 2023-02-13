#!/bin/bash

# files with the stdout, 
# mostly used for troubleshooting and getting meta information (How many files used for what)
touch output/twitch/output-inject-rnd-1370.txt
#touch output-info/twitch/output-inject-rnd-658.txt
#touch output-info/twitch/output-inject-rnd-342.txt
#touch output-info/twitch/output-inject-rnd-171.txt

# test injection with different captures sizes
python3 inject-rnd.py 1370 | tee output/twitch/output-inject-rnd-1370.txt
#python3 inject-rnd.py 658 | tee output-inject-rnd-658.txt
#python3 inject-rnd.py 342 | tee output-inject-rnd-342.txt
#python3 inject-rnd.py 171 | tee output-inject-rnd-171.txt