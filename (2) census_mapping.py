#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 19:40:18 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

#%% Calculating percentage of households recieving SNAP in each zip code

oregon_acs_data = pd.read_csv("2019_ACS_API_ZCTA_request.csv", dtype=str)

oregon_acs_data["Percent SNAP"] = round(oregon_acs_data["Receipt of SNAP"].astype(float) / oregon_acs_data["Households"].astype(float) * 100, 4)

oregon_acs_data.to_csv("2019_ACS_with_percents.csv", index=False)

#%% Spatial join between ZCTA data and Oregon state boundary
# this will cup zip codes that are partially outside of the state

oregon_acs_trim = oregon_acs_data[["ZIP", "Percent SNAP", "Households"]].copy()

zip_geodata = gpd.GeoDataFrame()
zip_geodata = gpd.read_file("cb_2020_us_zcta520_500k.zip")
zip_geodata = zip_geodata.to_crs(epsg = 2992)
zip_geodata = zip_geodata.rename(columns = {"ZCTA5CE20":"ZIP"})

# merging the two sets of data on the ZIP column
zip_geodata = zip_geodata.merge(oregon_acs_trim, on="ZIP", how="inner", validate="1:1", indicator=True)
print("\nMerge indicator:")
print(zip_geodata["_merge"].value_counts())
zip_geodata = zip_geodata.drop(columns = ["_merge"])

states = gpd.read_file("s_22mr22.zip")

oregon_state = states.query("STATE == 'OR'")
oregon_state = oregon_state.to_crs(epsg = 2992)

or_zips_geodata = zip_geodata.clip(oregon_state, keep_geom_type=True)

if os.path.exists("oregon_zip_geodata.gpkg"):
    os.remove("oregon_zip_geodata.gpkg")

or_zips_geodata.to_file("oregon_zip_geodata.gpkg", layer="ZIP", index=False)
or_zips_geodata.to_file("oregon_zip_geodata.gpkg", layer="Percent SNAP", index=False)
oregon_state.to_file("oregon_state_geodata.gpkg", layer = "geometry", index=False)

if os.path.exists("oregon_zip_geodata.csv"):
    os.remove("oregon_zip_geodata.csv")

or_zips_geodata.to_csv("oregon_zip_geodata.csv", index=False)