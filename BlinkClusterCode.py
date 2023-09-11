import pandas as pd # for data manipulation & functionality
import numpy as np # for array creation & manipulation
import matplotlib as mpl  # for data visualization backend 
import matplotlib.pyplot as plt # for data visualization frontend
import os # for reading & writing files to the system
import tkinter as tk # for the GUI
from tkinter import filedialog # for file interaction and manipulation within tkinter
import logging # for application diagnostics 


def get_path():
    root = tk.Tk() 
    root.withdraw() 
    msg = "Select the directory"
    arguments = {"title": msg}
    path = filedialog.askdirectory(**arguments)

    # check if the folder contains the required files
    if (
        not os.path.exists(os.path.join(path, "events.csv"))
        or not os.path.exists(os.path.join(path, "blinks.csv"))
    ):
        error = f"The selected folder does not contain a blinks.csv or events.csv file"
        logging.error(error)
        raise SystemExit(error)
    return path

# read events and blinks data from CSV files
path = get_path()
events_df_plot = pd.read_csv(os.path.join(path, "events.csv"))
blinks_df_plot = pd.read_csv(os.path.join(path, "blinks.csv"))

# filter blinks only occurring between event name A and B
event_name_A_plot = "10 Secs Before Stepping Off"
event_name_B_plot = "Test End"

# define timestamps of event A and event B
time_event_A_plot = events_df_plot[events_df_plot["name"] == event_name_A_plot]["timestamp [ns]"].values[0]
time_event_B_plot = events_df_plot[events_df_plot["name"] == event_name_B_plot]["timestamp [ns]"].values[0]

# filter only timestamps in the blinks file to between those corresponsing to event A and event B
blinks_df_filter_plot = blinks_df_plot[    (blinks_df_plot["start timestamp [ns]"] > time_event_A_plot)
    & (blinks_df_plot["end timestamp [ns]"] < time_event_B_plot)
]

# define seconds_the_section_last as the difference between time_event_B and time_event_A in seconds
seconds_the_section_last_plot = (time_event_B_plot - time_event_A_plot) / 1e9

# build a df to prep for plot calculation
blinks_df_filter_plot_copy = blinks_df_filter_plot.copy()
blinks_df_filter_plot_copy["second"] = np.nan
blinks_per_second_plot = pd.DataFrame(
    columns=["Length of Test [s]", "Blink Rate [#]", "avg_blink_duration"]
)

plotlengthinterval = 1.0 # specify the plot length interval in seconds

# count the intervals between the end of the recording and time_event_A
for i in range(int(seconds_the_section_last_plot / plotlengthinterval)):
    time_interval_start_plot = time_event_B_plot - (i + 1) * plotlengthinterval * 1e9
    time_interval_end_plot = time_event_B_plot - i * plotlengthinterval * 1e9
    indexes_plot = blinks_df_filter_plot_copy["start timestamp [ns]"].between(time_interval_start_plot, time_interval_end_plot)
    blinks_df_filter_plot_copy.loc[indexes_plot, "Length of Test [s]"] = i
    avg_blink_duration_plot = blinks_df_filter_plot_copy.loc[indexes_plot, "duration [ms]"].mean() 
    blinks_per_second_plot = pd.concat(
        [
            blinks_per_second_plot,
            pd.DataFrame(
                [[i, indexes_plot.sum(), avg_blink_duration_plot]],
                columns=["Length of Test [s]", "Blink Rate [#]", "avg_blink_duration"],
            ),
        ],
        ignore_index=True,
    )

blinks_per_second_plot.to_csv("blinks_per_second.csv")
blinks_per_second_plot.plot(x= "Length of Test [s]", y="Blink Rate [#]", title= "Cognitive Load Visualized By Blink Rate Clusters")

# sort the dataframe by blink rate in descending order
blinks_per_second_plot = blinks_per_second_plot.sort_values(by='Blink Rate [#]', ascending=False)

# get the top five blink rates
top_five_blinks = blinks_per_second_plot.head(5)

ax = plt.gca()
ax.spines['right'].set_color((.8,.8,.8))
ax.spines['top'].set_color((.8,.8,.8))

#for index, row in top_five_blinks.iterrows():
    #ax.annotate(f'{row["Blink Rate [#]"]}', xy=(row["Length of Test [s]"], 
    #row["Blink Rate [#]"]), xycoords='data', xytext=(-30, 30), textcoords='offset points', 
    #fontsize=10, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2"), zorder=0)

plt.grid('on', color='lightgray', linestyle='dashed')
plt.grid(zorder=0)
plt.show()



# filter blinks based on start and end timestamps
blinks_df_cluster = blinks_df_filter_plot.copy()
# already tried using the "original" df, doesn't work. 

# convert time_event_A and time_event_B to integers
time_event_A_plot = time_event_A_plot.astype(int)
time_event_B_plot = time_event_B_plot.astype(int)

# Blink rate per second
blinks_df_filter_copy = blinks_df_filter_plot.copy()
blinks_df_filter_copy["second"] = np.nan
blinks_per_second = pd.DataFrame(
    columns=["second", "number of blinks", "avg_blink_duration"]
)


# define seconds_the_section_last as the difference between time_event_B and time_event_A in seconds
seconds_the_section_last = (time_event_B_plot - time_event_A_plot) / 1e9 

interval = 1.0 # specify the interval in seconds

# count the intervals between the end of the recording and time_event_A
for i in range(int(seconds_the_section_last / interval)):
    time_interval_start = time_event_B_plot - (i + 1) * interval * 1e9
    time_interval_end = time_event_B_plot - i * interval * 1e9
    indexes = blinks_df_filter_copy["start timestamp [ns]"].between(time_interval_start, time_interval_end)
    blinks_df_filter_copy.loc[indexes, "second"] = i
    avg_blink_duration = blinks_df_filter_copy.loc[indexes, "duration [ms]"].mean() 
    blinks_per_second = pd.concat(
        [
            blinks_per_second,
            pd.DataFrame(
                [[i, indexes.sum(), avg_blink_duration]],
                columns=["second", "number of blinks", "avg_blink_duration"],
            ),
        ],
        ignore_index=True,
    )
# Sort the dataframe by number of blinks in descending order
blinks_per_second_plot.sort_values(by=["number of blinks"], ascending=False, inplace=True)

# Get the top three rows of the dataframe
top_3_rows = blinks_per_second_plot.head(5)

# Get the seconds and blink count for the top 3 rows
top_3_seconds = top_3_rows["second"]
top_3_blink_counts = top_3_rows["number of blinks"]

# Print the top 3 seconds and their blink counts
for i in range(5):
    print("Second:", top_3_seconds.iloc[i], "Blink count:", top_3_blink_counts.iloc[i])



# Get the blink ids and timestamps that were recorded in the top 3 seconds
top_3_seconds_list = top_3_seconds.tolist()
top_3_blink_ids = blinks_df_filter_plot.nlargest(5, 'blink ID')
top_3_blink_start_timestamps = blinks_df_filter_plot.nlargest(5, 'start timestamp [ns]')
# Print the top 3 blink timestamps
for i in range(5):
    print("Blink ID:", top_3_blink_ids.iloc[i], "Timestamp:", top_3_blink_start_timestamps.iloc[i])







