#!/bin/bash
# Plot all the result graphs

# input: {title} {csv file 1} {csv file 2} ...
# wf-old-result/df-size-twitch-itr-1370.csv

# DF with size
python3 rds-collect2/plotter/plot_df.py default-itr wf-old-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv

# DF without size
python3 rds-collect2/plotter/plot_df.py default-itr wf-old-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv

#DF tiktok
python3 rds-collect2/plotter/plot_df.py default-itr wf-old-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv