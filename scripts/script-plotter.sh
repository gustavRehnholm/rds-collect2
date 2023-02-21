#!/bin/bash
# Plot all the result graphs

# DF with size
python3 rds-collect2/plotter/plot_df.py default-itr wf-result/df-size-twitch-itr-1355.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-230.csv wf-result/df-size-twitch-none.csv
#python3 rds-collect2/plotter/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1355.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-230.csv wf-result/df-size-twitch-none.csv

# DF without size
python3 rds-collect2/plotter/plot_df.py size-itr wf-result/df-size-twitch-itr-1355.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-230.csv wf-result/df-size-twitch-none.csv
#python3 rds-collect2/plotter/plot_df.py size-rnd wf-result/df-size-twitch-rnd-1355.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-230.csv wf-result/df-size-twitch-none.csv

#DF tiktok
python3 rds-collect2/plotter/plot_df.py tiktok-itr wf-result/df-size-twitch-itr-1355.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-230.csv wf-result/df-size-twitch-none.csv
#python3 rds-collect2/plotter/plot_df.py tiktok-rnd wf-result/df-size-twitch-rnd-1355.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-230.csv wf-result/df-size-twitch-none.csv
