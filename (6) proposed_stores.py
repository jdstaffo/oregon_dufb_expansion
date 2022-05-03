#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:24:10 2022

@author: juliadstafford
"""

import pandas as pd
import geopandas as gpd
import os

# reading in input file of high need business data from Oregon API
high_need_biz = pd.read_csv("high_need_businesses.csv", dtype=str)

# removing duplicates from dataframe
# most businesses are listed in triplicate in the original Oregon database
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


#%%% YOU WERE HERE
# look through records by hand
# pick which ones to drop
# get coordinates
# map them




# selecting records to keep - reivew of stores has to be done by hand
# looked up addresses on google maps to see if businesses were operating at listed address
# searched for business names to see what industry they were in (grocery vs. restaurants vs. manufacturing)
# looked at yelp reviews if possible or google street view/photos to try to see if store sells fresh fruits and vegetables
sorted_hn_biz.drop([
    3, 5, 7, 8, 11, 19], axis=0, inplace=True)