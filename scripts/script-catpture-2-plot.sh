#!/bin/bash
# Go from captures to plotted graphs
# replicate the previous result

# ./rds-collect2/scripts/script-catpture-2-plot.sh 

# Parse, rm unusable data packets, and files with too much dataloss
#touch rds-collect2/parser/stdout-dir/stdout-parse.txt
#python3 rds-collect2/parser/parse.py | tee rds-collect2/parser/stdout-dir/stdout-parse.txt

# Create smaller datasets, to test the diffirence the size makes 
#touch rds-collect2/parser/stdout-dir/stdout-smaller.txt
#python3 rds-collect2/parser/create-smaller-captures.py | tee rds-collect2/parser/stdout-dir/stdout-smaller.txt

# inject the data
touch rds-collect2/parser/stdout-dir/inject.txt
./rds-collect2/scripts/script-inject.sh | tee  rds-collect2/parser/stdout-dir/inject.txt

# train DF, with the smaller datasample as in the previous work
#touch df-old.txt
#./rds-collect2/scripts/script-df-old.sh | tee df-old.txt

# plot the result of the smaller sample size
#touch plotter-old.txt
#./rds-collect2/scripts/script-plotter-old.sh | tee plotter-old.txt

# train DF, with the datasample
touch df.txt
./rds-collect2/scripts/script-df.sh | tee df.txt

# plot the result
touch plotter.txt
./rds-collect2/scripts/script-plotter.sh | tee plotter.txt

