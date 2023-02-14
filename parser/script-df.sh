#!/bin/bash
# Run all the wf that one needs

# For testing ./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-itr-1370 --train -s 5 -h

./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-itr-1370 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-itr-658 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-itr-342 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-itr-171 --train -s 100 -h

./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-rnd-1370 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-rnd-658 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-rnd-342 --train -s 100 -h
./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-rnd-171 --train -s 100 -h

./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-none-1370 --train -s 100 -h
