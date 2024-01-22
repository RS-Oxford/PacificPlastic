#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    extract_CDNC_northeast_Pacific.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        18/01/2024 11:10

import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from datetime import datetime, timedelta

def read_nd_data(file_name, variable_name):
    """
    Reads the specified variable from a NetCDF file.
    """
    print(f"Reading data from file: {file_name}")
    with nc.Dataset(file_name, mode='r') as dataset:
        variable_array = dataset[variable_name][:]
    return variable_array

def filter_data(lat, lon, data, lat_range, lon_range):
    """
    Filters data within specified latitude and longitude ranges.
    """
    lat_mask = (lat >= lat_range[0]) & (lat <= lat_range[1])
    lon_mask = (lon >= lon_range[0]) & (lon <= lon_range[1])
    return data[lat_mask, :][:, lon_mask]

def process_yearly_data(year):
    """
    Processes and aggregates data for a given year.
    """
    data_path = f'/badc/deposited2022/modis_cdnc_sampling_gridded/data/{year}/'
    monthly_data = [[] for _ in range(12)]

    for day in range(1, 366):
        file_name = data_path + f'modis_nd.{year}.{day:03d}.A.v1.nc'
        if not os.path.exists(file_name):
            continue

        nd_data = read_nd_data(file_name, 'Nd_BR17')[0, :, :].T
        lat = read_nd_data(file_name, 'lat_bnds')[::-1].mean(axis=1)
        lon = read_nd_data(file_name, 'lon_bnds').mean(axis=1)

        filtered_data = filter_data(lat, lon, nd_data, [20, 40], [-150, -130])
        month = (datetime(year, 1, 1) + timedelta(days=day - 1)).month
        monthly_data[month - 1].append(filtered_data)
        print(f"Processed: Year {year}, Month {month}, Day {day}")

    return monthly_data

def save_to_csv(yearly_data):
    """
    Saves aggregated data into a CSV file.
    """
    with open('Northeast_Pacific_2000_2020.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year-Month', 'Average Value', 'Standard Deviation'])

        for year, months in yearly_data.items():
            for month, data in enumerate(months, start=1):
                if data:
                    month_data = np.array(data)
                    avg = np.nanmean(month_data)
                    std = np.nanstd(month_data)
                    writer.writerow([f'{year}-{month:02d}', avg, std])

# Main execution
yearly_data = {}
for year in range(2000, 2021):
    yearly_data[year] = process_yearly_data(year)

save_to_csv(yearly_data)

# write a fucntion ...

