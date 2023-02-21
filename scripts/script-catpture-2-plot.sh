#!/bin/bash
# Go from captures to plotted graphs
# replicate the previous result

# ./rds-collect2/scripts/script-catpture-2-plot.sh 

touch rds-collect2/parser/stdout-dir/stdout-parse.txt
# Parse, rm unusable data packets, and files with too much dataloss
python3 rds-collect2/parser/parse.py | tee rds-collect2/parser/stdout-dir/stdout-parse.txt

touch rds-collect2/parser/stdout-dir/stdout-smaller.txt
# Create smaller datasets, to test the diffirence the size makes 
python3 rds-collect2/parser/create-smaller-captures.py | tee rds-collect2/parser/stdout-dir/stdout-smaller.txt

# inject the data
touch rds-collect2/parser/stdout-dir/inject.txt
./rds-collect2/scripts/script-inject.sh | tee  rds-collect2/parser/stdout-dir/inject.txt

touch df-old.txt
# train DF, with the smaller datasample
./rds-collect2/scripts/script-df-old.sh | tee df-old.txt

touch plotter-old.txt
# plot the result of the smaller sample size
./rds-collect2/scripts/script-plotter-old.sh | tee plotter-old.txt

touch df.txt
# train DF, with the datasample
./rds-collect2/scripts/script-df.sh | tee df.txt

touch plotter.txt
# plot the result
./rds-collect2/scripts/script-plotter.sh | tee plotter.txt

