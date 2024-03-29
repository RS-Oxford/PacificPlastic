#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    caliop_extraction_lon.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        23/01/2024 17:53

import os
import csv
import sys
import logging
import argparse
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from get_caliop import *

# Constants
LOG_EXTENSION = ".log"
# latitude distribution
NORTHERN_LATITUDE = 40
SOUTHERN_LATITUDE = 15
EASTERN_LONGITUDE_THRESHOLD = 145   # Eastern threshold at 140 degrees East
WESTERN_LONGITUDE_THRESHOLD = -125  # Western threshold at 125 degrees West
MIN_ALTITUDE = 0
MAX_ALTITUDE = 20

# Set up argument parser
parser = argparse.ArgumentParser(description="Script to process data at specific date.")
parser.add_argument("DATE_SEARCH", type=str, help="Date in the format YYYY-MM-DD.")

# Parse the arguments
args = parser.parse_args()

# Use the parsed arguments
DATE_SEARCH = args.DATE_SEARCH

# Directory paths and locations
CALIPSO_DATA_PATH = "/gws/nopw/j04/gbov/data/asdc.larc.nasa.gov/data/CALIPSO/LID_L2_05kmAPro-Standard-V4-51/"
CSV_OUTPUT_PATH = './csv_APro_lon_distribution'
# Create csv saving directory if not present
if not os.path.exists(CSV_OUTPUT_PATH):
    os.mkdir(CSV_OUTPUT_PATH)

# Initialize Logging
script_base_name, _ = os.path.splitext(sys.modules['__main__'].__file__)
log_file_name = script_base_name + LOG_EXTENSION
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filemode='w', filename=log_file_name, level=logging.INFO)
logger = logging.getLogger()

def main():

    # search all data at CALIPSO_DATA_PATH/year/month/
    year = DATE_SEARCH.split('-')[0]
    month = DATE_SEARCH.split('-')[1]
    day = DATE_SEARCH.split('-')[2]

    CSV_OUTPUT_PATH_MONTH = CSV_OUTPUT_PATH + '/%s'%month
    if not os.path.exists(CSV_OUTPUT_PATH_MONTH):
        os.mkdir(CSV_OUTPUT_PATH_MONTH)

    data_path = os.path.join(CALIPSO_DATA_PATH, year, month)

    file_list = os.listdir(data_path)
    # only keep files that contains year-month-day in the full file name
    file_list = [file for file in file_list if DATE_SEARCH in file]

    # iterate through all files
    for file in file_list:
        # print(data_path + file)
        try:

            (footprint_lat_caliop, footprint_lon_caliop,
             alt_caliop, beta_caliop, alpha_caliop,
             caliop_aerosol_type, caliop_feature_type, caliop_dp, alt_tropopause) \
                = extract_variables_from_caliop(data_path + '/' + file, logger)

            print('Processing file: {}'.format(file))

        except:
            print('Cannot process file: {}'.format(file))
            continue

        caliop_aerosol_type = caliop_aerosol_type[:, (footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        caliop_feature_type = caliop_feature_type[:, (footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        caliop_dp = caliop_dp[:, (footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        beta_caliop = beta_caliop[:, (footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        alpha_caliop = alpha_caliop[:, (footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        caliop_lat = footprint_lat_caliop[(footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]
        caliop_lon = footprint_lon_caliop[(footprint_lat_caliop > SOUTHERN_LATITUDE) & (footprint_lat_caliop < NORTHERN_LATITUDE) & ((footprint_lon_caliop > EASTERN_LONGITUDE_THRESHOLD) | (footprint_lon_caliop < WESTERN_LONGITUDE_THRESHOLD))]

        if caliop_aerosol_type.shape[1] > 0:

            flat_aerosol_type = caliop_aerosol_type.flatten()
            flat_feature_type = caliop_feature_type.flatten()
            flat_dp = caliop_dp.flatten()
            flat_beta = beta_caliop.flatten()
            flat_alpha = alpha_caliop.flatten()

            # Create a DataFrame
            df = pd.DataFrame({
                'caliop_aerosol_type': flat_aerosol_type,
                'caliop_feature_type': flat_feature_type,
                'caliop_dp': flat_dp,
                'beta_caliop': flat_beta,
                'alpha_caliop': flat_alpha,
                'caliop_lat': np.tile(caliop_lat, caliop_aerosol_type.shape[0]),
                'caliop_lon': np.tile(caliop_lon, caliop_aerosol_type.shape[0]),
                'alt_caliop': np.repeat(alt_caliop, caliop_aerosol_type.shape[1])
            })

            # Save the DataFrame
            output_file = os.path.join(CSV_OUTPUT_PATH_MONTH, f"{file[0:-4]}.csv")
            df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
