#!/bin/bash
# Run all the wf that one needs, but with sample 5, to provide a quick test to see that the trainign works as intended

# ./rds-collect2/parser/script-df-test.sh

# DF with size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train -s 5 --csv wf-test-result/df-size-twitch-itr-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train -s 5 --csv wf-test-result/df-size-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train -s 5 --csv wf-test-result/df-size-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-220 --train -s 5 --csv wf-test-result/df-size-twitch-itr-220.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1370 --train -s 5 --csv wf-test-result/df-size-twitch-rnd-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train -s 5 --csv wf-test-result/df-size-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train -s 5 --csv wf-test-result/df-size-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-220 --train -s 5 --csv wf-test-result/df-size-twitch-rnd-220.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-none-1370 --train -s 5 --csv wf-test-result/df-size-twitch-none.csv

# DF without size
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-itr-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-220 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-itr-220.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1370 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-rnd-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-220 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-rnd-220.csv

./df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-none-1370 --train --constant -s 5 --csv wf-test-result/df-constant-twitch-none.csv

# DF tiktok
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-1370 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-itr-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-685 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-itr-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-342 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-itr-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-itr-220 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-itr-220.csv

./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-1370 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-rnd-1370.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-685 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-rnd-685.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-342 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-rnd-342.csv
./df-fitness.py -d rds-collect2/parser/injected-datasets/twitch/parsedFiles-rnd-220 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-rnd-220.csv

/df-fitness.py -d rds-collect2/parser/injected-dataset/twitch/parsedFiles-none-1370 --train --tiktok -s 5 --csv wf-test-result/df-tiktok-twitch-none.csv