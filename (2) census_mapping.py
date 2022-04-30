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
oregon_acs_data = pd.read_csv("2020_ACS_API_request.csv", dtype=str)

# creating new column for percentage of households recieving SNAP or public assistance more broadly in each tracto
oregon_acs_data["Percent SNAP"] = round(oregon_acs_data["Receipt of SNAP"].astype(float) / oregon_acs_data["Households"].astype(float) * 100, 4)
oregon_acs_data["Percent Public Assist"] = round(oregon_acs_data["Public Assist"].astype(float) / oregon_acs_data["Households"].astype(float) * 100, 4)

# saving new columns to new csv
oregon_acs_data.to_csv("2020_ACS_with_percents.csv", index=False)
#%%

##FIX THIS SO THAT IT"S NOT ON GEOID - should be on zip instead
## AND READ IN ZCTA data, not tract


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
