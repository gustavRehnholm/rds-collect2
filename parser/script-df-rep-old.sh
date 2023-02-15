#!/bin/bash
# To replicate the result from rds-collect, it should perform simmilare

# ./rds-collect2/parser/script-df-rep-old.sh

# DF with size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train --csv wf-old-result/df-size-twitch-itr-1370.csv

# DF without size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train --constant --csv wf-old-result/df-constant-twitch-itr-1370.csv

# DF tiktok
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train --tiktok --csv wf-old-result/df-tiktok-twitch-itr-1370.csv