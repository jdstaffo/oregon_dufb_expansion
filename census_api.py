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

# setting the for clause of the query
for_clause = "tract:*"

# setting the in clause of the query
# state = Oregon
in_clause = "state:41"

# my Census API key
key_value = "8a0c471829f0b6d031bc0e9f473f796194d1323f"

# creating a new dictionary with the API payload
# B19001_001E: HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)
# B19019_001E: MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY HOUSEHOLD SIZE
# B11016_001E: HOUSEHOLD TYPE BY HOUSEHOLD SIZE
# B99221_001E: ALLOCATION OF FOOD STAMPS/SNAP RECEIPT
# B19058_001E: PUBLIC ASSISTANCE INCOME OR FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS
payload = {"get":"NAME,B19001_001E,B19019_001E,B11016_001E,B99221_001E,B19058_001E", "for":for_clause, "in":in_clause, "key":key_value}

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
acs_data = acs_data.rename(columns = {"B19001_001E":"income", 
                              "B19019_001E":"hh income",
                              "B11016_001E":"hh size",
                              "B99221_001E":"SNAP",
                              "B19058_001E":"public assist"})

# creating new column for each tract's GEOID
# GEOID: state, county, and tract IDs
acs_data["GEOID"] = acs_data["state"]+acs_data["county"]+acs_data["tract"]

# writing to output csv
acs_data.to_csv("2020_ACS_API_request.csv")
