#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:40:02 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import os

#%% Census API - 2019 American Community Survey ZCTA data for Oregon

api = "https://api.census.gov/data/2019/acs/acs5"

for_clause = "zip code tabulation area:*"

in_clause = "state:41"

key_value = "8a0c471829f0b6d031bc0e9f473f796194d1323f"

# specific ACS variables in the API
# B11001_001E: TOTAL HOUSEHOLDS (FAMILY AND NONFAMILY)
# B22001_002E: RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS (002 = YES)
payload = {"get":"NAME,B11001_001E,B22001_002E", "for":for_clause, "in": in_clause, "key":key_value}


response = requests.get(api, payload)

if response.status_code == 200:
    print("\nSuccess: response status code is", response.status_code)
else:
    print(response.status_code)
    print(response.text)
    assert False

row_list = response.json()

colnames = row_list[0]
datarows = row_list[1:]

acs_data = pd.DataFrame(columns=colnames, data=datarows)

acs_data = acs_data.rename(columns = {"B11001_001E":"Households",
                                      "B22001_002E":"Receipt of SNAP",
                                      "zip code tabulation area": "ZIP"})

if os.path.exists("2019_ACS_API_ZCTA_request.csv"):
    os.remove("2019_ACS_API_ZCTA_request.csv")

acs_data.to_csv("2019_ACS_API_ZCTA_request.csv", index=False)