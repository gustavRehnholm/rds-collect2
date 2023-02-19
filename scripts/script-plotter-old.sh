#!/bin/bash
# Plot all the result graphs

# input: {title} {csv file 1} {csv file 2} ...

# DF with size
python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

# DF without size
python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

#DF tiktok
python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv
