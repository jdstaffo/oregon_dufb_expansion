#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 09:36:12 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import json
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim

stores = pd.read_csv("existing_grocery_stores.csv", dtype=str)

# creating new address column and empty list for coordinates
stores["Full address"] = stores["Street address"] + "," + stores["City"] + "," + stores["State"] + "," + stores["Zip code"]

# creating list of addresses
stores_list = stores["Full address"].tolist()

# geolocating coordinates of stores

# API endpoint
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
print(dups)

# selecting duplicate records to keep - reivew of coordinates has to be done by hand
store_coords.drop([3, 5, 7, 8, 11, 19], axis=0, inplace=True)

# merging store_coords with stores to see which stores did not get coordinates
store_coords = store_coords.rename(columns = {"query":"Full address"})
stores = stores.merge(store_coords, on="Full address", how="outer", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(stores["_merge"].value_counts())

# inputting missing coordinates - collected from google maps by hand

## THIS IS WHEERE YOU ARE WORKING
# write script to print rows with nan for address
# find coordinates on google maps - or do what Wiloxen suggests

# dropping the "_merge" column
stores = stores.drop(columns = ["_merge"])

# writing to output file
