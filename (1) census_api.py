#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:40:02 2022

@author: juliadstafford
"""

import pandas as pd
import requests

# setting variable api to the American Community Survey 5-Year API endpoint for 2020
api = "https://api.census.gov/data/2020/acs/acs5"

# setting the for clause of the query to zip code tabulation areas
for_clause = "zip code tabulation area:*"

# my Census API key
key_value = "8a0c471829f0b6d031bc0e9f473f796194d1323f"

# creating a new dictionary with the API payload
# B01003_001E: TOTAL POPULATION
# B11001_001E: TOTAL HOUSEHOLDS (FAMILY AND NONFAMILY)
# B22001_002E: RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS (002 = YES)
# B19058_002E: PUBLIC ASSISTANCE INCOME OR FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS (002 = YES)
payload = {"get":"NAME,B01003_001E,B11001_001E,B22001_002E,B19058_002E", "for":for_clause, "key":key_value}

# calling the request
response = requests.get(api, payload)

# if statement to check if response status is 200 (aka a success)
if response.status_code == 200:
    print("\nSuccess: response status code is", response.status_code)
# else statement prints error code and error text
# assert False will cause the script to stop immediately if the statement is reached
# this helps ensure reliability
else:
    print(response.status_code)
    print(response.text)
    assert False

# parsing the json returned by the Census and return a list of rows
row_list = response.json()

# setting up the column names (first row) and data rows
colnames = row_list[0]
datarows = row_list[1:]

# converting the data into a Pandas dataframe
acs_data = pd.DataFrame(columns=colnames, data=datarows)

# renaming columns
acs_data = acs_data.rename(columns = {"B01003_001E":"Population",
                                      "B11001_001E":"Households",
                                      "B22001_002E":"Receipt of SNAP",
                                      "B19058_002E":"Public Assist",
                                      "zip code tabulation area": "ZIP"})

#%% Selecting out Oregon zip codes

# reading in list of Oregon zip codes
or_zips = pd.read_csv("oregon_zip_codes_database.csv", dtype=str)

# renaming columns
or_zips = or_zips.rename(columns = {"zip": "ZIP"})

# merging the two sets of data on the GEIOD column
oregon_acs_data = acs_data.merge(or_zips, on="ZIP", how="inner", validate="1:1", indicator=True)

# printing the merge indicator
print("\nMerge indicator:")
print(oregon_acs_data["_merge"].value_counts())

# dropping the "_merge" column
oregon_acs_data = oregon_acs_data.drop(columns = ["_merge"])

# writing to output csv
oregon_acs_data.to_csv("2020_ACS_API_request.csv", index=False)
