#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 09:36:12 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import json
import os

#%% Open Street Map API

stores = pd.read_csv("existing_grocery_stores.csv", dtype=str)

stores["Full address"] = stores["Street address"] + "," + stores["City"] + "," + stores["State"] + "," + stores["Zip code"]

stores_list = stores["Full address"].tolist()

api = "https://nominatim.openstreetmap.org/search"

# looping through the addresses and building a list of results
output = []

for s in stores_list:
    payload = {"q":f"<{s}>", "format":"json"}
    response = requests.get(api, payload)
    if response.status_code == 200:
        print("\nSuccess: response status code is", response.status_code)
    else:
        print(response.status_code)
        print(response.text)
        assert False
    result = response.json()
    print(json.dumps(result))
    for r in result:
        newaddr = {
            "query":s,
            "name":r["display_name"], 
            "lat":r["lat"],
            "lon":r["lon"]
            }
        output.append(newaddr)

store_coords = pd.DataFrame(output)

store_coords = store_coords.dropna()

#%% Cleaning API data
# some of this must be done manually - follow prompts given in script

# finding duplicate records
dup_store_coords = store_coords.duplicated(subset = "query", keep=False)
dups = store_coords[dup_store_coords]
print("\nDuplicated records:")
print(dups)

# selecting duplicate records to keep
# the reivew of coordinates has to be done by hand
# this is done by looking through dups
store_coords.drop([3, 5, 7, 8, 11, 19], axis=0, inplace=True)

# merging store_coords with stores to see which stores did not get coordinates
store_coords = store_coords.rename(columns = {"query":"Full address"})
stores = stores.merge(store_coords, on="Full address", how="outer", validate="1:1", indicator=True)
print("\nMerge indicator:")
print(stores["_merge"].value_counts())

print("\nStores without coordinates:")
print(stores["lat"].isna())

# inputting missing coordinates
# these must be collected from google maps by hand
# this is done by entering the address and right-clicking on the red marker
# the coordinates will be at the top of the drop-down menu
stores.at[2,"lat"] = "45.20671871375452"
stores.at[2,"lon"] = "-123.95964866004289"

stores.at[5,"lat"] = "44.55393395819116"
stores.at[5,"lon"] = "-123.26453513123064"

stores = stores.drop(columns = ["_merge", "name"])

if os.path.exists("existing_store_geodata.csv"):
    os.remove("existing_store_geodata.csv")

stores.to_csv("existing_store_geodata.csv", index=False)