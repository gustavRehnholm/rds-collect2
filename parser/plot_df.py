#!/usr/bin/env python3
'''
To plot the result from the WF training
input: {title} {csv file 1} {csv file 2} ...
'''

'''
# default
python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv

python3 rds-collect2/parser/plot_df.py default-itr wf-result/df-size-twitch-itr-1370.csv wf-result/df-size-twitch-itr-685.csv wf-result/df-size-twitch-itr-342.csv wf-result/df-size-twitch-itr-220.csv wf-result/df-size-twitch-none.csv
python3 rds-collect2/parser/plot_df.py default-rnd wf-result/df-size-twitch-rnd-1370.csv wf-result/df-size-twitch-rnd-685.csv wf-result/df-size-twitch-rnd-342.csv wf-result/df-size-twitch-rnd-220.csv wf-result/df-size-twitch-none.csv
'''
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

    colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
    labels = ["1370", "685", "342", "220", "none"]

    # Extract all csv files that should be plotted in a graph
    for i in range(2, len(sys.argv)):
        datasets.append(pd.read_csv(sys.argv[i], sep=','))

    # end program if data is unsuable
    if len(datasets) <= 0:
        print("ERROR: there is no inputted files")
        print("Aborting program")
        return
    elif len(datasets) > len(colors):
        print("ERROR: there are more lines to plot than colors, add more colors in the colors list")
        print("Aborting program")
        return
    elif len(datasets) > len(labels):
        print("ERROR: there are more lines to plot than labels, add more labels in the labels list")
        print("Aborting program")
        return

    # plot all lines for the graph
    for j in range(0, len(dataset)):
        sns.pointplot(data=dataset[j], x ="th", y="accuracy", markers='|', color=colors[j], label=labels[j])

        plt.plot(dataset[j]['th'], label="Threshold")
        plt.plot(dataset[j]['accuracy'], label="accuracy")

    plt.ylim(0, 1)
    plt.legend()
    plt.title(sys.argv[1])
    plt.show()


# run main 
if __name__=="__main__":
    main()