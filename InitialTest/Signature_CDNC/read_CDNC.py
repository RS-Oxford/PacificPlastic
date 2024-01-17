#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    read_CDNC.py
# @Author:      Dr. Rui Song
# @Email:       rui.song@physics.ox.ac.uk
# @Time:        17/01/2024 15:03

import netCDF4 as nc

DATA_PATH = '/badc/deposited2022/modis_cdnc_sampling_gridded/data/2017/'
FILE_NAME = 'modis_nd.2017.178.A.v1.nc'

def read_nd_data(file_path, variable_name):

    """
    Reads the variable_name dataset from a NetCDF file.
    """

    # Open the NetCDF file
    with nc.Dataset(file_path, mode='r') as dataset:
        # Access the 'Nd_Z18' dataset
        nd_variable_array = dataset[variable_name][:]

    return nd_variable_array

# test
Nd_BR17_data = read_nd_data(DATA_PATH + FILE_NAME, 'Nd_BR17')
print(Nd_BR17_data)
print(Nd_BR17_data.shape.shape)