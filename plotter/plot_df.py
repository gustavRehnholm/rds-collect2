#!/usr/bin/env python3
'''
To plot the result from the WF training
input: {title} {csv file 1} {csv file 2} ...

./rds-collect2/scripts/script-plotter.sh
'''

'''
# default
python3 rds-collect2/plotter/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

python3 rds-collect2/plotter/plot_df.py size-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py size-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

python3 rds-collect2/plotter/plot_df.py tiktok-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/plotter/plot_df.py tiktok-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv
'''

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

def main():
    '''
    sys.argv[0] : name of the program
    sys.argv[1] : title
    sys.argv[2] : first file
    '''

    datasets = []
    title = sys.argv[1]

    colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
    markers_list = ['x','o','v','^','<']
    
    if title == "old-result":
        labels = ["default", "constant", "tiktok"]
    else:
        labels = ["1370", "685", "342", "220", "none"]

    # Extract all csv files that should be plotted in a graph
    for i in range(2, len(sys.argv)):
        datasets.append(pd.read_csv(sys.argv[i]))

    # end program if data is unsuable
    if len(datasets) <= 0:
        print("ERROR: there is no inputted files")
        print("Aborting program")
        return
    elif len(datasets) > len(colors):
        print("ERROR: there are more lines to plot than colors, add more colors in the colors list")
        print("There is ", len(datasets), " lines to show in the graphs")
        print("Aborting program")
        return
    elif len(datasets) > len(labels):
        print("ERROR: there are more lines to plot than labels, add more labels in the labels list")
        print("There is ", len(datasets), " lines to show in the graphs")
        print("Aborting program")
    elif len(datasets) > len(markers_list):
        print("ERROR: there are more lines to plot than markers, add more markers in markers_list")
        print("There is ", len(datasets), " lines to show in the graphs")
        print("Aborting program")
        return
        

    # plot all lines for the graph
    for j in range(0, len(datasets)):
        sns.pointplot(data=datasets[j], x ="th", y="accuracy", markers=markers_list[j], color=colors[j], label=labels[j])

    plt.ylim(0, 1)
    plt.legend()
    plt.title(title)

    fig = plt.gcf()
    fig.savefig("fig/" + title)

    plt.show()


# run main 
if __name__=="__main__":
    main()