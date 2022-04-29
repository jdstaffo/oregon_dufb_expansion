#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

# reading in input file of high need tracts
high_need = pd.read_csv("high_need.csv")

# converting geography codes to strings as needed
high_need["COUNTYFP"] = high_need["COUNTYFP"].astype(str)
high_need["TRACTCE"] = high_need["TRACTCE"].astype(str)
high_need["GEOID"] = high_need["GEOID"].astype(str)

# reading in input crosswalk file of zip codes and census tracts and prepping for merge
zip_tracts = pd.read_csv("ZIP_TRACT_122020.csv")
zip_tracts = zip_tracts.rename(columns={"TRACT":"GEOID"})
zip_tracts["GEOID"] = zip_tracts["GEOID"].astype(str)
zip_tracts["ZIP"] = zip_tracts["ZIP"].astype(str)
zip_tracts_trim = zip_tracts[["ZIP", "GEOID"]].copy()

# merging the two sets of data on the tract ID column
high_need = high_need.merge(zip_tracts_trim, on="GEOID", how="left", validate="m:m", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(high_need["_merge"].value_counts())

dup_high_need = high_need.duplicated(subset = "GEOID", keep=False)
dups = high_need[dup_high_need]
print(dups)

