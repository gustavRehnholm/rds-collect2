#!/bin/bash
# Go from captures to plotted graphs
# replicate the previous result

# Parse, rm unusable data packets, and files with too much dataloss
python3 rds-collect2/parser/parse.py | tee stdout-dir/stdout-parse.txt

# inject the data 
script -q -c "python3 inject.py 1370 itr" /dev/null | tee stdout-dir/output-inject-itr-1370.txt

# train DF, with the smaller datasample
./rds-collect2/scripts/script-df-rep-old.sh

# plot the result
./rds-collect2/scripts/script-plotter-old.sh