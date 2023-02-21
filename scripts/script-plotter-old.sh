#!/bin/bash
# Plot all the result graphs

# input: {title} {csv file 1} {csv file 2} ...
# wf-old-result/df-size-twitch-itr-1370.csv

# DF size, constant and tiktok
python3 rds-collect2/plotter/plot_df.py old-result wf-old-result/df-size-twitch-itr-1355.csv wf-old-result/df-constant-twitch-itr-1355.csv wf-old-result/df-tiktok-twitch-itr-1355.csv

#python3 rds-collect2/plotter/plot_df.py old-result wf-result/df-size-twitch-itr-1355.csv wf-result/df-constant-twitch-itr-1355.csv wf-result/df-tiktok-twitch-itr-1355.csv
