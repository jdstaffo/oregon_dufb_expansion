#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd
import requests
import json

# reading in input file of high need zip codes
high_need = pd.read_csv("high_need_geodata.csv")

# converting zip codes to strings
high_need["ZIP"] = high_need["ZIP"].astype(str)

# narrowing down to just the zip codes themselves
hn_zips = high_need["ZIP"].to_list()

print("\nHigh-need zip codes:")
print(hn_zips)

# setting up the API endpoint
api = "https://data.oregon.gov/resource/tckn-sxa6.json"

# setting up the payload
payload = {"state":"OR"}

# looping through zips of interest and collecting the results in a large dictionary
# using zip codes as keys

hn_zips = ['97233', '97204', '97014', '97329', '97907', '97905', '97741', '97761', '97001', '97880',
           '97622', '97639', '97621', '97731', '97733', '97463', '97914', '97147', '97480', '97324',
           '97390', '97343', '97380', '97344', '97371', '97534', '97497', '97406', '97465', '97481']

result = {}

for z in hn_zips:
    payload["zip"] = z
    response = requests.get(api,payload)
    print("\nResponse status code is", response.status_code)
    result[z] = pd.DataFrame.from_records(response.json())

# creating dataframe from results
high_need_businesses = pd.concat(result)

# dropping unnecessary columns
high_need_businesses = high_need_businesses.drop(columns = ["jurisdiction", "first_name", "middle_name", "last_name",
                                                            "suffix", "entity_of_record_reg_number", "entity_of_record_name"])

# writing to output file
high_need_businesses.to_csv("high_need_businesses.csv", index=False)