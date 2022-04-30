#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 19:40:18 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

# reading in input file of ACS data
oregon_acs_data = pd.read_csv("2020_ACS_API_ZCTA_request.csv", dtype=str)

# creating new column for percentage of households recieving SNAP or public assistance more broadly in each tracto
oregon_acs_data["Percent SNAP"] = round(oregon_acs_data["Receipt of SNAP"].astype(float) / oregon_acs_data["Households"].astype(float) * 100, 4)
oregon_acs_data["Percent Public Assist"] = round(oregon_acs_data["Public Assist"].astype(float) / oregon_acs_data["Households"].astype(float) * 100, 4)

# saving new columns to new csv
oregon_acs_data.to_csv("2020_ACS_with_percents.csv", index=False)

# trimming it for joining onto geography data
oregon_acs_trim = oregon_acs_data[["ZIP", "Percent SNAP", "County", "Households"]].copy()

# reading in input file of ZCTA geography
zip_geodata = gpd.GeoDataFrame()
zip_geodata = gpd.read_file("cb_2020_us_zcta520_500k.zip")
zip_geodata = zip_geodata.to_crs(epsg = 2992)
zip_geodata = zip_geodata.rename(columns = {"ZCTA5CE20":"ZIP"})

# merging the two sets of data on the ZIP column
zip_geodata = zip_geodata.merge(oregon_acs_trim, on="ZIP", how="inner", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(zip_geodata["_merge"].value_counts())

# dropping the "_merge" column
zip_geodata = zip_geodata.drop(columns = ["_merge"])

# checking to see if the output file already exists
if os.path.exists("zip_geodata.gpkg"):
    os.remove("zip_geodata.gpkg")

# writing to output geopackage file
zip_geodata.to_file("zip_geodata.gpkg", layer="ZIP", index=False)
zip_geodata.to_file("zip_geodata.gpkg", layer="Percent SNAP", index=False)

# writing to output csv file
zip_geodata.to_csv("zip_geodata.csv", index=False)
