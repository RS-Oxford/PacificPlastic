#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    plot_trend.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        18/01/2024 15:37

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from datetime import datetime
import numpy as np

def read_csv_data(file_path):
    """
    Reads data from a CSV file and returns lists of dates and values.
    """
    dates, averages, std_devs = [], [], []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            dates.append(datetime.strptime(row[0], '%Y-%m'))
            averages.append(float(row[1]))
            std_devs.append(float(row[2]))
    return dates, averages, std_devs

def plot_data(dates, averages, std_devs):
    """
    Plots the data on a graph.
    """
    plt.figure(figsize=(12, 6))
    plt.errorbar(dates, averages, yerr=std_devs, fmt='o', color='b', ecolor='lightgray', elinewidth=3, capsize=0)

    plt.title('Monthly Average Nd_BR17 Values with Standard Deviations (2000-2020)')
    plt.xlabel('Time (Year-Month)')
    plt.ylabel('Average Nd_BR17 Value')
    plt.grid(True)

    # Formatting the date on the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gcf().autofmt_xdate()  # Auto-rotate the dates

    plt.savefig('monthly_average_nd_br17_values_2000_2020.png')
    plt.show()

# Main execution
dates, averages, std_devs = read_csv_data('./averaged_data_2000_2020.csv')
plot_data(dates, averages, std_devs)
