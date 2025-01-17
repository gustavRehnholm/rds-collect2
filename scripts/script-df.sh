#!/bin/bash
# Run all the wf that one needs
# sample 5 is good for quick testing, but for proper results, on will most likely need 100 samples

# ./rds-collect2/parser/script-df.sh

sample = 5

echo run with sample $sample

# DF with size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train -s $sample --csv wf-result/df-size-twitch-itr-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train -s $sample --csv wf-result/df-size-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train -s $sample --csv wf-result/df-size-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-230 --train -s $sample --csv wf-result/df-size-twitch-itr-230.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1355 --train -s $sample --csv wf-result/df-size-twitch-rnd-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train -s $sample --csv wf-result/df-size-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train -s $sample --csv wf-result/df-size-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-230 --train -s $sample --csv wf-result/df-size-twitch-rnd-230.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-none-1355 --train -s $sample --csv wf-result/df-size-twitch-none.csv

# DF without size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train --constant -s $sample --csv wf-result/df-constant-twitch-itr-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train --constant -s $sample --csv wf-result/df-constant-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train --constant -s $sample --csv wf-result/df-constant-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-230 --train --constant -s $sample --csv wf-result/df-constant-twitch-itr-230.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1355 --train --constant -s $sample --csv wf-result/df-constant-twitch-rnd-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train --constant -s $sample --csv wf-result/df-constant-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train --constant -s $sample --csv wf-result/df-constant-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-230 --train --constant -s $sample --csv wf-result/df-constant-twitch-rnd-230.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-none-1355 --train --constant -s $sample --csv wf-result/df-constant-twitch-none.csv

# DF tiktok
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1355 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-itr-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-230 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-itr-230.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1355 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-rnd-1355.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-230 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-rnd-230.csv

/df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-none-1355 --train --tiktok -s $sample --csv wf-result/df-tiktok-twitch-none.csv