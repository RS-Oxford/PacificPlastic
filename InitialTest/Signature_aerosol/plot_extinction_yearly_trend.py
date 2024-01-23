#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    plot_extinction_yearly_trend.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        23/01/2024 15:18

import os
import pandas as pd
import numpy as np
import proplot as pplt

# Constants
CSV_OUTPUT_PATH = './csv_APro'
FIG_OUT_PATH = './figures'

if not os.path.exists(FIG_OUT_PATH):
    os.mkdir(FIG_OUT_PATH)

BINSIZE = 0.1  # Group latitudes every 0.1 degree
NUM_ROWS = 399  # Fixed number of rows in each dataframe

def load_data(file_path):
    df = pd.read_csv(file_path)
    num_cols = len(df) // NUM_ROWS
    alpha_caliop = df['alpha_caliop'].values.reshape(NUM_ROWS, num_cols)
    lats = df['caliop_lat'].unique()
    alts = df['alt_caliop'].unique()
    return alpha_caliop, lats, alts

def create_latitude_bins(lats):
    min_lat, max_lat = min(lats), max(lats)
    return np.arange(min_lat, max_lat + BINSIZE, BINSIZE)

def aggregate_data(alpha_data_list):
    all_lats = np.concatenate([lats for _, lats in alpha_data_list])
    lat_bins = create_latitude_bins(all_lats)
    aggregated_alpha = [np.empty((0, NUM_ROWS)) for _ in range(len(lat_bins) - 1)]

    for alpha_caliop, lats in alpha_data_list:
        for i, (bin_min, bin_max) in enumerate(zip(lat_bins[:-1], lat_bins[1:])):
            indices = (lats >= bin_min) & (lats < bin_max)
            aggregated_alpha[i] = np.vstack((aggregated_alpha[i], alpha_caliop[:, indices].T))

    averaged_alpha = np.empty((len(lat_bins) - 1, NUM_ROWS))
    for i, bin_data in enumerate(aggregated_alpha):
        if bin_data.size == 0:
            print(f"Warning: No data for bin {i} ({lat_bins[i]} - {lat_bins[i+1]}).")
            averaged_alpha[i] = np.full(NUM_ROWS, np.nan)
        else:
            bin_data = np.nan_to_num(bin_data, nan=0)
            averaged_alpha[i] = np.mean(bin_data, axis=0)
    return averaged_alpha, lat_bins

def plot_averaged_alpha(averaged_alpha, lat_bins, alts, ax):
    lat_centers = (lat_bins[:-1] + lat_bins[1:]) / 2
    Lats, Alts = np.meshgrid(lat_centers, alts)
    colormap = ax.pcolormesh(Lats, Alts, averaged_alpha.T, shading='auto', cmap='RdYlBu_r', vmin=0., vmax=0.1)
    ax.colorbar(colormap, label='Extinction Coefficient [km$^{-1}$]')
    ax.set_xlabel('Latitude [$^{\circ}$]')
    ax.set_ylabel('Altitude [km]')
    ax.format(xlim=(lat_bins.min(), lat_bins.max()), ylim=(0., 10))

def main():
    fig, axs = pplt.subplots(nrows=4, ncols=3, figsize=(15, 18))
    months = [f'{2017}-{month:02d}' for month in range(1, 13)]

    for month, ax in zip(months, axs):
        CSV_OUTPUT_PATH_MONTH = CSV_OUTPUT_PATH +'/%s'%month[-2:]
        alpha_data_list = []
        for file in os.listdir(CSV_OUTPUT_PATH_MONTH):
            if file.endswith('.csv') and month in file:
                print('Processing: ', file)
                file_path = os.path.join(CSV_OUTPUT_PATH_MONTH, file)
                alpha_caliop, lats, alts = load_data(file_path)
                alpha_data_list.append((alpha_caliop, lats))

        averaged_alpha, lat_bins = aggregate_data(alpha_data_list)
        plot_averaged_alpha(averaged_alpha, lat_bins, alts, ax)
        ax.set_title(f'{month}')

    fig.suptitle('Monthly Extinction Coefficient Trends for 2017')
    fig.savefig(FIG_OUT_PATH + '/extinction_trends_2017.png')

if __name__ == "__main__":
    main()
