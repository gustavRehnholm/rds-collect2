#!/bin/bash
# Go from captures to plotted graphs
# replicate the previous result

# ./rds-collect2/scripts/script-catpture-2-plot.sh 

# Parse, rm unusable data packets, and files with too much dataloss
#python3 rds-collect2/parser/parse.py | tee rds-collect2/parser/stdout-dir/stdout-parse.txt

python3 rds-collect2/parser/create-smaller-captures.py | tee rds-collect2/parser/stdout-dir/stdout-smaller.txt

# inject the data 
./rds-collect2/scripts/script-inject.sh

# train DF, with the smaller datasample
./rds-collect2/scripts/script-df.sh

# plot the result
./rds-collect2/scripts/script-plotter.sh

# train DF, with the smaller datasample
./rds-collect2/scripts/script-df-rep-old.sh

# plot the result of the smaller sample size
./rds-collect2/scripts/script-plotter-old.sh