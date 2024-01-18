#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    read_CDNC.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        17/01/2024 15:03

import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

DATA_PATH = '/badc/deposited2022/modis_cdnc_sampling_gridded/data/2015/'
FILE_NAME = 'modis_nd.2015.178.A.v1.nc'

def read_nd_data(file_path, variable_name):
    """
    Reads the variable_name dataset from a NetCDF file.
    """
    with nc.Dataset(file_path, mode='r') as dataset:
        nd_variable_array = dataset[variable_name][:]

    return nd_variable_array


def plot_global_data(lon, lat, data, title, save_path):
    """
    Plots the data on a global map and saves the plot.

    Parameters:
    lon (numpy.ndarray): Longitude boundaries.
    lat (numpy.ndarray): Latitude boundaries.
    data (numpy.ndarray): Data to plot.
    title (str): Title of the plot.
    save_path (str): Path to save the plot.
    """
    # Create a meshgrid for plotting
    lon_centers = (lon[:, 1] + lon[:, 0]) / 2
    lat_centers = (lat[:, 1] + lat[:, 0]) / 2
    LON, LAT = np.meshgrid(lon_centers, lat_centers)

    # Create the plot
    plt.figure(figsize=(15, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # Plot the data
    c = ax.pcolormesh(LON, LAT, data.squeeze(), transform=ccrs.PlateCarree())

    # Add a colorbar
    plt.colorbar(c, orientation='vertical')

    # Add title and labels
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Save the plot
    plt.savefig(save_path)
    plt.close()


# Read data
Nd_BR17_data = read_nd_data(DATA_PATH + FILE_NAME, 'Nd_BR17')
lat = read_nd_data(DATA_PATH + FILE_NAME, 'lat_bnds')
lon = read_nd_data(DATA_PATH + FILE_NAME, 'lon_bnds')

# Plot and save the data
plot_title = 'Global Plot of Nd_BR17 Data'
save_plot_path = 'Nd_BR17_global_plot.png'
plot_global_data(lon, lat, Nd_BR17_data, plot_title, save_plot_path)

