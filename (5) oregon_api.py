#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import json
import os

#%% Oregon API - Active Businesses - ALL

high_snap = pd.read_csv("high_snap_geodata.csv")

high_snap["ZIP"] = high_snap["ZIP"].astype(str)

hs_zips = high_snap["ZIP"].to_list()

print("\nHigh SNAP zip codes:")
print(hs_zips)

api = "https://data.oregon.gov/resource/tckn-sxa6.json"

payload = {"state":"OR", "$limit":"50000"}

# looping through zips of interest and collecting the results in a large dictionary
# using zip codes as keys - manually copy these from the print call above
hs_zips = ['97236', '97233', '97204', '97859', '97622', '97639', '97536', '97731', '97463', '97914',
           '97329', '97345', '97907', '97905', '97350', '97741', '97761', '97001', '97108', '97147',
           '97480', '97343', '97344', '97534', '97523', '97497', '97406', '97465', '97417', '97431']

result = {}

for z in hs_zips:
    payload["zip"] = z
    response = requests.get(api,payload)
    print("\nResponse status code is", response.status_code)
    result[z] = pd.DataFrame.from_records(response.json())
    print(len(result[z]))

high_snap_businesses = pd.concat(result)

# dropping unnecessary columns
high_snap_businesses = high_snap_businesses.drop(columns = ["jurisdiction", "first_name", "middle_name", "last_name",
                                                            "suffix", "entity_of_record_reg_number", "entity_of_record_name"])

if os.path.exists("high_snap_businesses.csv"):
    os.remove("high_snap_businesses.csv")

high_snap_businesses.to_csv("high_snap_businesses.csv", index=False)