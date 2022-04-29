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
tract_geodata = pd.read_csv("tract_data.csv")

# converting geography codes to strings as needed
tract_geodata["COUNTYFP"] = tract_geodata["COUNTYFP"].astype(str)
tract_geodata["GEOID"] = tract_geodata["GEOID"].astype(str) 

# selecting the 30 tracts with the highest percentage of households recieving SNAP
tract_geodata = tract_geodata.sort_values("Percent SNAP", ascending=False)
high_need = tract_geodata[:30]

# trimming it for joining onto geography data
high_need_trim = high_need[["GEOID", "COUNTYFP","Percent SNAP"]].copy()

# reading in input file of census tract geography
new_geodata = gpd.GeoDataFrame()
new_geodata = gpd.read_file("tl_2020_41_tract.zip")
new_geodata = new_geodata.to_crs(epsg = 2992)

# merging the two sets of data on the GEIOD column
new_geodata = new_geodata.merge(high_need_trim, on="GEOID", how="inner", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(new_geodata["_merge"].value_counts())

# dropping the "_merge" column
new_geodata = new_geodata.drop(columns = ["_merge"])

 # checking to see if the output file already exists
if os.path.exists("high_need_data.gpkg"):
    os.remove("high_need_data.gpkg")

# writing to output geopackage file
new_geodata.to_file("high_need_data.gpkg", layer="GEOID", index=False)
new_geodata.to_file("high_need_data.gpkg", layer="COUNTYFP", index=False)
new_geodata.to_file("high_need_data.gpkg", layer="Percent SNAP", index=False)