#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:24:10 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import json
import os

#%% Sorting through active businesses in high SNAP zip codes

high_snap_biz = pd.read_csv("high_snap_businesses.csv", dtype=str)

# removing duplicates from dataframe
# specifically removing mailing addreses, authorized representatives, and registered agent entries
# so that the resulting dataframe should just have principal places of business
# most businesses are listed in triplicate with several address categories in the original Oregon database
high_snap_biz = high_snap_biz[high_snap_biz["associated_name_type"].str.contains("MAILING ADDRESS") == False]
high_snap_biz = high_snap_biz[high_snap_biz["associated_name_type"].str.contains("AUTHORIZED REPRESENTATIVE") == False]
high_snap_biz = high_snap_biz[high_snap_biz["associated_name_type"].str.contains("REGISTERED AGENT") == False]

# final duplicate check to see if any remain
dups = high_snap_biz.duplicated(subset = "registry_number", keep=False)
print("\nDuplicate business records:", dups.sum())
high_snap_biz = high_snap_biz.drop_duplicates(subset = "registry_number")

# sorting through high SNAP business API results to find grocery-adjacent stores
search_hs_biz1 = high_snap_biz.loc[high_snap_biz["business_name"].str.contains(r"\bfood\b|\bfoods\b", case=False, regex=True)]
search_hs_biz2 = high_snap_biz.loc[high_snap_biz["business_name"].str.contains(r"\bgrocery\b|\bmarket\b", case=False, regex=True)]
search_hs_biz3 = high_snap_biz.loc[high_snap_biz["business_name"].str.contains(r"\bfruit\b|\bvegetable\b", case=False, regex=True)]

sorted_hs_biz = pd.concat([search_hs_biz1, search_hs_biz2, search_hs_biz3])
print("\nPossible grocery stores in high SNAP areas:")
print(sorted_hs_biz["business_name"])

# writing to output file to make it easier to select records to keep (next step)
if os.path.exists("initial_sort_hs_biz_geodata.csv"):
    os.remove("initial_sort_hs_biz_geodata.csv")

sorted_hs_biz.to_csv("initial_sort_hs_biz_geodata.csv", index=False)

#%% Selecting proposed grocery stores
# review of stores must be done manually
# this is done by:
# looking up addresses on google maps to confirm that the businesses were operating at listed address
# and looking at yelp and google reviews and/or google street view/photos to see if store sells fresh fruits and vegetables
# tip: save the initial_sort csv under a different name (so that it does not get re-created when script is run)
# and color-code it for the stores to keep and stores to drop

sorted_hs_biz = sorted_hs_biz.sort_values("business_name", ascending=True)
sorted_hs_biz = sorted_hs_biz.reset_index()
sorted_hs_biz = sorted_hs_biz.drop(columns = ["index"])
proposed_hs_biz = sorted_hs_biz.loc[[11, 30, 31, 33, 34, 42, 43, 46, 48, 49, 66, 72, 80, 83, 84, 115, 125, 126]]

#%% Open Street Map API

proposed_hs_biz["Full address"] = proposed_hs_biz["address"] + "," + proposed_hs_biz["city"] + "," + proposed_hs_biz["state"] + "," + proposed_hs_biz["zip"]

stores_list = proposed_hs_biz["Full address"].tolist()

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

new_store_coords = pd.DataFrame(output)

#%% Cleaning API data
# some of this must be done manually - follow prompts given in script

# finding duplicate records
dup_store_coords = new_store_coords.duplicated(subset = "query", keep=False)
dups = new_store_coords[dup_store_coords]
print("\nDuplicated records:")
print(dups)

# selecting duplicate records to keep
# the reivew of coordinates has to be done by hand
# this is done by looking through dups
new_store_coords.drop([1, 4, 7, 10, 12, 13, 14, 15, 16, 17, 18, 22, 26, 28, 29], axis=0, inplace=True)

# merging new_store_coords with proposed_hs_biz to see which stores did not get coordinates
new_store_coords = new_store_coords.rename(columns = {"query":"Full address"})
proposed_hs_biz = proposed_hs_biz.merge(new_store_coords, on="Full address", how="outer", validate="1:1", indicator=True)
print("\nMerge indicator:")
print(proposed_hs_biz["_merge"].value_counts())

print("\nStores without coordinates:")
print(proposed_hs_biz["lat"].isna())

# inputting missing coordinates
# these must be collected from google maps by hand
# this is done by entering the address and right-clicking on the red marker
# the coordinates will be at the top of the drop-down menu
proposed_hs_biz.at[5,"lat"] = "44.61417915022682"
proposed_hs_biz.at[5,"lon"] = "-121.13409075772348"

proposed_hs_biz.at[15,"lat"] = "42.05009779833905"
proposed_hs_biz.at[15,"lon"] = "-123.61654453082276"

proposed_hs_biz.at[17,"lat"] = "45.5062899164863"
proposed_hs_biz.at[17,"lon"] = "-122.47476227303814"

proposed_hs_biz = proposed_hs_biz.drop(columns = ["_merge"])

if os.path.exists("proposed_hs_biz_geodata.csv"):
    os.remove("proposed_hs_biz_geodata.csv")

proposed_hs_biz.to_csv("proposed_hs_biz_geodata.csv", index=False)