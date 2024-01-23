#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    trend_extinction.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        22/01/2024 23:27

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import proplot as pplt

# Constants
CSV_OUTPUT_PATH = './csv_APro'
BINSIZE = 0.1  # Group latitudes every 0.1 degree
NUM_ROWS = 399  # Fixed number of rows in each dataframe


def load_data(file_path):
    df = pd.read_csv(file_path)
    num_cols = len(df) // NUM_ROWS  # Calculate number of columns
    alpha_caliop = df['alpha_caliop'].values.reshape(NUM_ROWS, num_cols)
    lats = df['caliop_lat'].unique()
    alts = df['alt_caliop'].unique()
    return alpha_caliop, lats, alts

def create_latitude_bins(lats):
    min_lat = min(lats)
    max_lat = max(lats)
    return np.arange(min_lat, max_lat + BINSIZE, BINSIZE)


def aggregate_data(alpha_data_list):
    all_lats = np.concatenate([lats for _, lats in alpha_data_list])
    lat_bins = create_latitude_bins(all_lats)
    aggregated_alpha = [np.empty((0, NUM_ROWS)) for _ in range(len(lat_bins) - 1)]

    for alpha_caliop, lats in alpha_data_list:
        for i in range(len(lat_bins) - 1):
            bin_min = lat_bins[i]
            bin_max = lat_bins[i + 1]
            indices = (lats >= bin_min) & (lats < bin_max)
            aggregated_alpha[i] = np.vstack((aggregated_alpha[i], alpha_caliop[:, indices].T))

    # Averaging with a check for empty bins
    averaged_alpha = np.empty((len(lat_bins) - 1, NUM_ROWS))

    for i, bin_data in enumerate(aggregated_alpha):

        if bin_data.size == 0:
            # Log a warning or error message indicating the empty bin
            print(f"Warning: No data found for bin {i} (Latitude range: {lat_bins[i]} - {lat_bins[i+1]}). Filling with NaN.")
            averaged_alpha[i] = np.full(NUM_ROWS, np.nan)
        else:
            bin_data[bin_data == np.nan] = 0.
            averaged_alpha[i] = np.mean(bin_data, axis=0)
            print(averaged_alpha[i])

    return averaged_alpha, lat_bins

def plot_averaged_alpha(averaged_alpha, lat_bins, alts):
    """
    Plots the averaged alpha values over given latitude bins and altitudes using ProPlot.

    Parameters:
    averaged_alpha (np.ndarray): 2D array of averaged alpha values.
    lat_bins (np.ndarray): Array of latitude bins.
    alts (np.ndarray): Array of altitudes.

    Returns:
    None
    """
    # Calculate the center of each latitude bin for plotting
    lat_centers = (lat_bins[:-1] + lat_bins[1:]) / 2

    # Create a meshgrid for plotting
    Lats, Alts = np.meshgrid(lat_centers, alts)

    # Create a ProPlot figure for better visual appeal
    fig, ax = pplt.subplots(figsize=(15, 6))

    # Plotting using ProPlot's pcolormesh for better color handling and aesthetics
    colormap = ax.pcolormesh(Lats, Alts, averaged_alpha.T, shading='auto', cmap='jet')

    # Adding a colorbar and setting its label
    ax.colorbar(colormap, label='Extinction Coefficient [km$^{-1}$]')

    # Setting labels and title with improved formatting
    ax.set_xlabel('Latitude [$^{\circ}$]')
    ax.set_ylabel('Altitude [km]')
    ax.set_ylim([0., 10])

    # Improved aesthetics for ticks and limits
    ax.format(xlim=(lat_bins.min(), lat_bins.max()), ylim=(alts.min(), alts.max()))

    # Save the plot with a descriptive filename
    fig.savefig('./extinction_latitude_trend_proplot.png')

def main():
    alpha_data_list = []
    for file in os.listdir(CSV_OUTPUT_PATH):
        if file.endswith('.csv'):
            print('Processing: ', file)
            file_path = os.path.join(CSV_OUTPUT_PATH, file)
            alpha_caliop, lats, alts = load_data(file_path)
            alpha_data_list.append((alpha_caliop, lats))

    averaged_alpha, lat_bins = aggregate_data(alpha_data_list)
    plot_averaged_alpha(averaged_alpha, lat_bins, alts)

if __name__ == "__main__":
    main()
