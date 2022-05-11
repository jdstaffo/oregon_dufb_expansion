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

stores = pd.read_csv("existing_grocery_stores.csv", dtype=str)

# creating new address column and empty list for coordinates
stores["Full address"] = stores["Street address"] + "," + stores["City"] + "," + stores["State"] + "," + stores["Zip code"]

# creating list of addresses
stores_list = stores["Full address"].tolist()

# geolocating coordinates of stores

# coordinates API endpoint
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

# dropping records with no query
store_coords = store_coords.dropna()

# finding duplicate records
dup_store_coords = store_coords.duplicated(subset = "query", keep=False)
dups = store_coords[dup_store_coords]
print("\nDuplicated records:")
print(dups)

# selecting duplicate records to keep - reivew of coordinates has to be done by hand
store_coords.drop([3, 5, 7, 8, 11, 19], axis=0, inplace=True)

# merging store_coords with stores to see which stores did not get coordinates
store_coords = store_coords.rename(columns = {"query":"Full address"})
stores = stores.merge(store_coords, on="Full address", how="outer", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(stores["_merge"].value_counts())

# printing the stores without coordinates
print("\nStores without coordinates:")
print(stores["Store name"], stores["lat"].isna())

# inputting missing coordinates - collected from google maps by hand
stores.at[2,"lat"] = "45.20671871375452"
stores.at[2,"lon"] = "-123.95964866004289"

stores.at[5,"lat"] = "44.55393395819116"
stores.at[5,"lon"] = "-123.26453513123064"

# dropping the "_merge" column and the "name" column for clarity
stores = stores.drop(columns = ["_merge", "name"])

# checking to see if the output file already exists
if os.path.exists("existing_store_geodata.csv"):
    os.remove("existing_store_geodata.csv")

stores.to_csv("existing_store_geodata.csv", index=False)