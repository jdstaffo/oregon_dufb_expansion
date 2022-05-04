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

# reading in input file of high need business data from Oregon API
high_need_biz = pd.read_csv("high_need_businesses.csv", dtype=str)

# removing duplicates from dataframe
# specifically removing mailing addreses, authorized representatives, and registered agent entries
# so that the resulting dataframe should just have principal places of business
# most businesses are listed in triplicate with several address categories in the original Oregon database
high_need_biz = high_need_biz[high_need_biz["associated_name_type"].str.contains("MAILING ADDRESS") == False]
high_need_biz = high_need_biz[high_need_biz["associated_name_type"].str.contains("AUTHORIZED REPRESENTATIVE") == False]
high_need_biz = high_need_biz[high_need_biz["associated_name_type"].str.contains("REGISTERED AGENT") == False]

# final duplicate check to see if any remain
dups = high_need_biz.duplicated(subset = "registry_number", keep=False)
print("\nDuplicate business records:", dups.sum())
high_need_biz = high_need_biz.drop_duplicates(subset = "registry_number")

# sorting through high need business API results to find grocery-adjacent stores
search_hn_biz1 = high_need_biz.loc[high_need_biz["business_name"].str.contains("food | foods", case=False)]
search_hn_biz2 = high_need_biz.loc[high_need_biz["business_name"].str.contains("grocery | market", case=False)]
search_hn_biz3 = high_need_biz.loc[high_need_biz["business_name"].str.contains("fruit | vegetable", case=False)]

# joining the search databases
sorted_hn_biz = pd.concat([search_hn_biz1, search_hn_biz2, search_hn_biz3])
print("\nPossible grocery stores in high need areas:")
print(sorted_hn_biz["business_name"])



## CHECK REMAINDER OF SCRIPT BY HAND
## BECAUSE OF NEW API CALL 5/4/22 9:30am



#%%
# selecting records to keep - reivew of stores has to be done by hand
# looked up addresses on google maps to see if businesses were operating at listed address
# searched for business names to see what industry they were in (grocery vs. restaurants vs. manufacturing)
# looked at yelp reviews or google street view/photos to try to see if store sells fresh fruits and vegetables
sorted_hn_biz = sorted_hn_biz.sort_values("business_name", ascending=True)
sorted_hn_biz = sorted_hn_biz.reset_index()
sorted_hn_biz = sorted_hn_biz.drop(columns = ["index"])
proposed_hn_biz = sorted_hn_biz.loc[[7, 8, 9, 19, 23]]

#%% Finding store coordinates

# creating new address column and empty list for coordinates
proposed_hn_biz["Full address"] = proposed_hn_biz["address"] + "," + proposed_hn_biz["city"] + "," + proposed_hn_biz["state"] + "," + proposed_hn_biz["zip"]

# creating list of addresses
stores_list = proposed_hn_biz["Full address"].tolist()

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

new_store_coords = pd.DataFrame(output)

# finding duplicate records
dup_store_coords = new_store_coords.duplicated(subset = "query", keep=False)
dups = new_store_coords[dup_store_coords]
print("\nDuplicated records:")
print(dups)

# selecting duplicate records to keep - reivew of coordinates has to be done by hand
new_store_coords.drop([2, 4], axis=0, inplace=True)

# merging new_store_coords with proposed_hn_biz to see which stores did not get coordinates
new_store_coords = new_store_coords.rename(columns = {"query":"Full address"})
proposed_hn_biz = proposed_hn_biz.merge(new_store_coords, on="Full address", how="outer", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(proposed_hn_biz["_merge"].value_counts())

# printing the stores without coordinates
print("\nStores without coordinates:")
print(proposed_hn_biz["business_name"], proposed_hn_biz["lat"].isna())

# inputting missing coordinates - collected from google maps by hand
proposed_hn_biz.at[0,"lat"] = "45.665884996636265"
proposed_hn_biz.at[0,"lon"] = "-121.89524677488562"

# dropping the "_merge" column
proposed_hn_biz = proposed_hn_biz.drop(columns = ["_merge"])

# checking to see if the output file already exists
if os.path.exists("proposed_hn_biz_geodata.csv"):
    os.remove("proposed_hn_biz_geodata.csv")

proposed_hn_biz.to_csv("proposed_hn_biz_geodata.csv", index=False)