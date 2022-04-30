#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:24:00 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

# reading in input file of ACS data
zip_geodata = pd.read_csv("zip_geodata.csv")

# converting geography codes to strings as needed
zip_geodata["ZIP"] = zip_geodata["ZIP"].astype(str)

# selecting the 30 zip codes with the highest percentage of households recieving SNAP
zip_geodata = zip_geodata.sort_values("Percent SNAP", ascending=False)
high_need = zip_geodata[:30]

# writing to output csv file
high_need.to_csv("high_need.csv", index=False)

# trimming it for joining onto geography data
high_need_trim = high_need[["ZIP"]].copy()

# reading in input file of zip code geography
new_geodata = gpd.GeoDataFrame()
new_geodata = gpd.read_file("oregon_zip_geodata.gpkg")
new_geodata = new_geodata.to_crs(epsg = 2992)

# merging the two sets of data on the GEIOD column
new_geodata = new_geodata.merge(high_need_trim, on="ZIP", how="inner", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(new_geodata["_merge"].value_counts())

# dropping the "_merge" column
new_geodata = new_geodata.drop(columns = ["_merge"])

 # checking to see if the output file already exists
if os.path.exists("high_need_data.gpkg"):
    os.remove("high_need_data.gpkg")

# writing to output geopackage file
new_geodata.to_file("high_need_geodata.gpkg", layer="Percent SNAP", index=False)

# writing to output csv file
new_geodata.to_csv("high_need_geodata.csv", index=False)