#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:24:00 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

#%% Selecting the high SNAP zip codes
# these are the 30 zip codes with the highest percentage of households recieving SNAP

zip_geodata = pd.read_csv("oregon_zip_geodata.csv")

zip_geodata["ZIP"] = zip_geodata["ZIP"].astype(str)

zip_geodata = zip_geodata.sort_values("Percent SNAP", ascending=False)
high_snap = zip_geodata[:30]

high_snap.to_csv("high_snap.csv", index=False)

#%% Adding geography to high SNAP zip codes

high_snap_trim = high_snap[["ZIP"]].copy()

new_geodata = gpd.GeoDataFrame()
new_geodata = gpd.read_file("oregon_zip_geodata.gpkg")
new_geodata = new_geodata.to_crs(epsg = 2992)

# merging the two sets of data on the GEIOD column
new_geodata = new_geodata.merge(high_snap_trim, on="ZIP", how="inner", validate="1:1", indicator=True)
print("\nMerge indicator:")
print(new_geodata["_merge"].value_counts())
new_geodata = new_geodata.drop(columns = ["_merge"])

if os.path.exists("high_snap_geodata.gpkg"):
    os.remove("high_snap_geodata.gpkg")

new_geodata.to_file("high_snap_geodata.gpkg", layer="Percent SNAP", index=False)

if os.path.exists("high_snap_geodata.csv"):
    os.remove("high_snap_geodata.csv")

new_geodata.to_csv("high_snap_geodata.csv", index=False)