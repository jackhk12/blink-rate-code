# blink-rate-code
Data Analysis and Visualization Script for Blink Rate and Event Correlation

This Python script performs data analysis and visualization on blink rate data in relation to specific events during a test or experiment utilizing ocular biometrics collection equiptment. It reads event and blink data from CSV files, filters and processes the data, and creates a line graph visualizing blink rate spikes across the length of an experiment. The script includes features for identifying top blink rates and their corresponding event timestamps, offering insights into cognitive load and attention during different test intervals.

## Prerequisites

Before running the script, ensure you have the following Python libraries installed:

- [Pandas](https://pandas.pydata.org/): For data manipulation and functionality.
- [NumPy](https://numpy.org/): For array creation and manipulation.
- [Matplotlib](https://matplotlib.org/): For data visualization.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): For the GUI.
- [Logging](https://docs.python.org/3/library/logging.html): For application diagnostics.

You can install these libraries using pip:

```bash
pip install pandas numpy matplotlib tkinter logging
```

## Getting Started
Run the script by executing appropriate change directory commands.

Running this script will prompt the user with a tkinter desktop GUI to select the FOLDER containing the blink and events .csv files; do not select the files individually. The script will then produce a graph detailing blink rate spikes and their respective timestamp, which can be referenced against a user FPOV camera and a retroactive think-aloud to determine cognitive roadblocks and information gaps in task execution. 

The results will be saved to a CSV file named "blinks_per_second.csv," and a plot will be displayed showing the blink rate clusters.
