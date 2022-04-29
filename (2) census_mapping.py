#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 19:40:18 2022

@author: juliadstafford
"""

import geopandas as gpd
import os

# reading in input file of ACS data
acs_data = gpd.read_file("2020_ACS_API_request.csv", dtype=float)

# creating new column for percentage of households recieving SNAP or public assistance more broadly in each tract
acs_data["Percent SNAP"] = round(acs_data["Receipt of SNAP"].astype(float) / acs_data["Households"].astype(float) * 100, 4)
acs_data["Percent Public Assist"] = round(acs_data["Public Assist"].astype(float) / acs_data["Households"].astype(float) * 100, 4)

# saving new columns to new csv
acs_data.to_csv("2020_ACS_with_percents.csv", index=False)

# trimming it for joining onto geography data
acs_trim = acs_data[["GEOID", "Percent SNAP", "Percent Public Assist"]].copy()

# reading in input file of census tract geography
geodata = gpd.GeoDataFrame()
geodata = gpd.read_file("tl_2020_41_tract.zip")
geodata = geodata.to_crs(epsg = 2992)

# merging the two sets of data on the GEIOD column
geodata = geodata.merge(acs_trim, on="GEOID", how="left", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(geodata["_merge"].value_counts())

# dropping the "_merge" column
geodata = geodata.drop(columns = ["_merge"])

# checking to see if the output file already exists
if os.path.exists("tract_data.gpkg"):
    os.remove("tract_data.gpkg")

# writing to output geopackage file
geodata.to_file("tract_data.gpkg", layer="GEOID", index=False)
geodata.to_file("tract_data.gpkg", layer="TRACTCE", index=False)
geodata.to_file("tract_data.gpkg", layer="Percent SNAP", index=False)

# writing to output csv file
geodata.to_csv("tract_data.csv", index=False)
