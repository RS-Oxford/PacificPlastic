#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    plot_extinction_yearly_trend_lon.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        23/01/2024 22:15

import os
import pandas as pd
import numpy as np
import proplot as pplt
import matplotlib.ticker as ticker
# Constants
CSV_OUTPUT_PATH = './csv_APro_lon_distribution'
FIG_OUT_PATH = './figures'

if not os.path.exists(FIG_OUT_PATH):
    os.mkdir(FIG_OUT_PATH)

BINSIZE = 0.1  # Group longitudes every 0.1 degree
NUM_ROWS = 399  # Fixed number of rows in each dataframe

def load_data(file_path):
    df = pd.read_csv(file_path)
    num_cols = len(df) // NUM_ROWS
    alpha_caliop = df['alpha_caliop'].values.reshape(NUM_ROWS, num_cols)
    longs = df['caliop_lon'].unique()  # Adjusted to read longitude
    alts = df['alt_caliop'].unique()

    longs[longs<0.] = 360. + longs[longs<0.]
    return alpha_caliop, longs, alts

def create_longitude_bins(longs):
    min_long, max_long = min(longs), max(longs)
    return np.arange(min_long, max_long + BINSIZE, BINSIZE)

def aggregate_data(alpha_data_list):
    all_longs = np.concatenate([longs for _, longs in alpha_data_list])
    long_bins = create_longitude_bins(all_longs)
    aggregated_alpha = [np.empty((0, NUM_ROWS)) for _ in range(len(long_bins) - 1)]

    for alpha_caliop, longs in alpha_data_list:
        for i, (bin_min, bin_max) in enumerate(zip(long_bins[:-1], long_bins[1:])):
            indices = (longs >= bin_min) & (longs < bin_max)
            aggregated_alpha[i] = np.vstack((aggregated_alpha[i], alpha_caliop[:, indices].T))

    averaged_alpha = np.empty((len(long_bins) - 1, NUM_ROWS))
    for i, bin_data in enumerate(aggregated_alpha):
        if bin_data.size == 0:
            print("Warning: No data for bin")
            averaged_alpha[i] = np.full(NUM_ROWS, np.nan)
        else:
            bin_data = np.nan_to_num(bin_data, nan=0)
            averaged_alpha[i] = np.mean(bin_data, axis=0)
    return averaged_alpha, long_bins

def plot_averaged_alpha(averaged_alpha, long_bins, alts, ax):
    long_centers = (long_bins[:-1] + long_bins[1:]) / 2
    Longs, Alts = np.meshgrid(long_centers, alts)
    ax.set_xlabel('Longitude', fontsize=20)
    ax.set_ylabel('Altitude [km]', fontsize=20)
    ax.format(xlim=(long_bins.min(), long_bins.max()), ylim=(0., 4), fontsize=18)

    # Custom function to format longitude labels
    def format_lon_labels(lon):
        if lon > 180:
            return f"{360 - lon:.0f}°W"
        else:
            return f"{lon:.0f}°E"

    # Set a reasonable interval for longitude ticks
    tick_interval = 10  # Adjust the interval as needed
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_interval))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_lon_labels(x)))

    for label in ax.get_xticklabels():
        label.set_fontsize(18)  # Adjust the font size as needed

    # This will return the 'mappable' object used for the colorbar.
    return ax.pcolormesh(Longs, Alts, averaged_alpha.T, shading='auto', cmap='RdYlBu_r', vmin=0., vmax=0.1)

def main():
    fig, axs = pplt.subplots(nrows=4, ncols=3, figsize=(28, 18))
    months = ['{}-{:02d}'.format(2017, month) for month in range(1, 2)]

    mappables = []
    number_of_columns = 3

    for month, ax in zip(months, axs):
        CSV_OUTPUT_PATH_MONTH = CSV_OUTPUT_PATH + '/%s' % month[-2:]
        alpha_data_list = []
        for file in os.listdir(CSV_OUTPUT_PATH_MONTH):
            if file.endswith('.csv') and month in file:
                print('Processing: ', file)
                file_path = os.path.join(CSV_OUTPUT_PATH_MONTH, file)
                alpha_caliop, longs, alts = load_data(file_path)
                alpha_data_list.append((alpha_caliop, longs))

        averaged_alpha, long_bins = aggregate_data(alpha_data_list)
        mappable = plot_averaged_alpha(averaged_alpha, long_bins, alts, ax)
        mappables.append(mappable)
        ax.set_title('{}'.format(month), fontsize=18)

    fig.colorbar(mappables[-1], loc='b', span=number_of_columns, label='Extinction Coefficient [km$^{-1}$]', labelsize=18, ticklabelsize=16)
    fig.suptitle('Monthly Extinction Coefficient Trends for 2017', fontsize=20)
    fig.savefig(FIG_OUT_PATH + '/extinction_trends_2017_lon.png')

if __name__ == "__main__":
    main()
