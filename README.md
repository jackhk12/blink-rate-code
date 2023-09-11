# blink-rate-code
Data Analysis and Visualization Script for Blink Rate and Event Correlation

This Python script performs data analysis and visualization on blink rate data in relation to specific events during a test or experiment utilizing ocular biometrics collection equiptment. It reads event and blink data from CSV files, filters and processes the data, and creates a line graph visualizing blink rate spikes across the length of an experiment. The script includes features for identifying top blink rates and their corresponding event timestamps, offering insights into cognitive load and attention during different test intervals.

Running this script will prompt the user with a tkinter desktop GUI to select the FOLDER containing the blink and events .csv files; do not select the files individually. The script will then produce a graph detailing blink rate spikes and their respective timestamp, which can be referenced against a user FPOV camera and a retroactive think-aloud to determine cognitive roadblocks and information gaps in task execution. 

