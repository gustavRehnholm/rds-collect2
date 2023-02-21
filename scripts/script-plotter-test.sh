#!/bin/bash
# Plot all the result graphs for the test data

# DF with size
python3 rds-collect2/plotter/plot_df.py default-itr wf-test-result/df-size-twitch-itr-1370.csv wf-test-result/df-size-twitch-itr-685.csv wf-test-result/df-size-twitch-itr-342.csv wf-test-result/df-size-twitch-itr-220.csv wf-test-result/df-size-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py default-rnd wf-test-result/df-size-twitch-rnd-1370.csv wf-test-result/df-size-twitch-rnd-685.csv wf-test-result/df-size-twitch-rnd-342.csv wf-test-result/df-size-twitch-rnd-220.csv wf-test-result/df-size-twitch-none.csv

# DF without size
python3 rds-collect2/plotter/plot_df.py size-itr wf-test-result/df-constant-twitch-itr-1370.csv wf-test-result/df-constant-twitch-itr-685.csv wf-test-result/df-constant-twitch-itr-342.csv wf-test-result/df-constant-twitch-itr-220.csv wf-test-result/df-constant-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py size-rnd wf-test-result/df-constant-twitch-rnd-1370.csv wf-test-result/df-constant-twitch-rnd-685.csv wf-test-result/df-constant-twitch-rnd-342.csv wf-test-result/df-constant-twitch-rnd-220.csv wf-test-result/df-constant-twitch-none.csv

#DF tiktok
python3 rds-collect2/plotter/plot_df.py tiktok-itr f-test-result/df-tiktok-twitch-itr-1370.csv wf-test-result/df-tiktok-twitch-itr-685.csv wf-test-result/df-tiktok-twitch-itr-342.csv wf-test-result/df-tiktok-twitch-itr-220.csv wf-test-result/df-tiktok-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py tiktok-rndwf-test-result/df-tiktok-twitch-rnd-1370.csv wf-test-result/df-tiktok-twitch-rnd-685.csv wf-test-result/df-tiktok-twitch-rnd-342.csv wf-test-result/df-tiktok-twitch-rnd-220.csv wf-test-result/df-tiktok-twitch-none.csv
