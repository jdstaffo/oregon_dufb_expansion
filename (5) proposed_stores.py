#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd

# reading in input file of high need tracts
high_need = pd.read_csv("high_need.csv")

# converting geography codes to strings as needed
high_need["COUNTYFP"] = high_need["COUNTYFP"].astype(str)
high_need["TRACTCE"] = high_need["TRACTCE"].astype(str)
high_need["GEOID"] = high_need["GEOID"].astype(str)

# reading in input crosswalk file of zip codes and census tracts and prepping for merge
zip_tracts = pd.read_csv("ZIP_TRACT_122021.csv", dtype=str)
zip_tracts = zip_tracts.rename(columns={"tract":"GEOID"})
OR_zip_tracts = zip_tracts.query("usps_zip_pref_state == 'OR'")
zip_tracts_trim = OR_zip_tracts[["zip", "GEOID"]].copy()

# merging the two sets of data on the tract ID column
high_need = high_need.merge(zip_tracts_trim, on="GEOID", how="left", validate="m:m", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(high_need["_merge"].value_counts())

# printing the tracts without zip codes
print("\nTracts without zip codes:")
print(high_need["zip"].isna())

# finding duplicate records - some census tracts overlap with multiple zip codes
dup_high_need = high_need.duplicated(subset = "GEOID", keep=False)
dups = high_need[dup_high_need]
print("\nDuplicated records:")
print(dups)


