#!/bin/bash
# To replicate the result from rds-collect, it should perform simmilare

# ./rds-collect2/parser/script-df-rep-old.sh
touch wf-old-result/df-size-twitch-itr-1355.csv
touch wf-old-result/df-constant-twitch-itr-1355.csv
touch wf-old-result/df-tiktok-twitch-itr-1355.csv

# DF with size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train --csv wf-old-result/df-size-twitch-itr-1355.csv

# DF without size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train --constant --csv wf-old-result/df-constant-twitch-itr-1355.csv

# DF tiktok
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train --tiktok --csv wf-old-result/df-tiktok-twitch-itr-1355.csv