#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 19:40:18 2022

@author: juliadstafford
"""

import geopandas as gpd

# reading in input file of ACS data
acs_data = gpd.read_file("2020_ACS_API_request.csv")

# reading in input file of census tract geography
geodata = gpd.GeoDataFrame()
geodata = gpd.read_file ("tl_2021_41_tract.zip")

# merging the two input files on the GEIOD column
geodata = geodata.merge(acs_data, on="GEOID", how="left", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(geodata["_merge"].value_counts())

# dropping the "_merge" column
geodata = geodata.drop(columns = ["_merge"])

# setting the CRS of the dataframe
geodata = geodata.set_crs(epsg = 2992)

# writing to output geopackage file
geodata.to_file("census_tracts.gkpg", layer = "public assist", index=False)
