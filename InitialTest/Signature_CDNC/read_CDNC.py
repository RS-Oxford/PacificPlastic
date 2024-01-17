#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    read_CDNC.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        17/01/2024 15:03

import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta

DATA_PATH = '/badc/deposited2022/modis_cdnc_sampling_gridded/data/2015/'

def read_nd_data(file_name, variable_name):
    """
    Reads the variable_name dataset from a NetCDF file.
    """
    print("Reading data from file: " + file_name)
    with nc.Dataset(file_name, mode='r') as dataset:
        nd_variable_array = dataset[variable_name][:]

    return nd_variable_array

def filter_data(lat, lon, data, lat_range, lon_range):
    """
    Filters the data by latitude and longitude range.
    """
    lat_mask = (lat >= lat_range[0]) & (lat <= lat_range[1])
    lon_mask = (lon >= lon_range[0]) & (lon <= lon_range[1])
    return data[:, lat_mask, :][:, :, lon_mask]

# Initialize an array to store monthly data
monthly_data = [[] for _ in range(12)]

for day in range(1, 366):
    file_name = DATA_PATH + f'modis_nd.2015.{day:03d}.A.v1.nc'

    if not os.path.exists(file_name):
        continue
    print(file_name)
    Nd_BR17_data = read_nd_data(file_name, 'Nd_BR17')[0, :, :]
    lat = read_nd_data(file_name, 'lat_bnds')[::-1].mean(axis=1)
    lon = read_nd_data(file_name, 'lon_bnds').mean(axis=1)

    # Filter data
    filtered_data = filter_data(lat, lon, Nd_BR17_data, [20, 40], [-150, -120])

    # Determine the month for the current day
    month = datetime(2015, 1, 1) + timedelta(days=day - 1)
    monthly_data[month.month - 1].append(filtered_data)

# Calculate the mean for each month
monthly_mean_values = [np.nanmean(np.array(month_data)) for month_data in monthly_data if month_data]

# Plotting the curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, 13), monthly_mean_values, marker='o')
plt.title('Average Nd_BR17 Values by Month')
plt.xlabel('Month')
plt.ylabel('Average Value')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True)
plt.savefig('average_nd_br17_values_by_month.png')
plt.show()
