#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:40:02 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import os

# setting variable api to the American Community Survey 5-Year API endpoint for 2019
api = "https://api.census.gov/data/2019/acs/acs5"

# setting the for clause of the query to zip code tabulation areas
for_clause = "zip code tabulation area:*"

# setting the in clause of the query to Oregon (state FIPS 41)
in_clause = "state:41"

# my Census API key
key_value = "8a0c471829f0b6d031bc0e9f473f796194d1323f"

# creating a new dictionary with the API payload
# B01003_001E: TOTAL POPULATION
# B11001_001E: TOTAL HOUSEHOLDS (FAMILY AND NONFAMILY)
# B22001_002E: RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS (002 = YES)
payload = {"get":"NAME,B01003_001E,B11001_001E,B22001_002E", "for":for_clause, "in": in_clause, "key":key_value}

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
                                      "zip code tabulation area": "ZIP"})

# checking to see if the output file already exists
if os.path.exists("2019_ACS_API_ZCTA_request.csv"):
    os.remove("2019_ACS_API_ZCTA_request.csv")

# writing to output csv
acs_data.to_csv("2019_ACS_API_ZCTA_request.csv", index=False)
