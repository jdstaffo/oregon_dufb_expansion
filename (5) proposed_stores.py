#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd
from sodapy import Socrata
import requests
import json
import os


# reading in input file of high need zip codes
high_need = pd.read_csv("high_need_geodata.csv")

# converting zip codes to strings
high_need["ZIP"] = high_need["ZIP"].astype(str)

# narrowing down to just the zip codes themselves
hn_zips = high_need["ZIP"].to_list()

print("\nHigh-need zip codes:")
print(hn_zips)

#%% OREGON API

# setting up the API endpoint
api = "https://data.oregon.gov/resource/tckn-sxa6.json"

# setting up the payload
payload = {"entity_type":"DOMESTIC BUSINESS CORPORATION"}

# looping through zips of interest and collecting the results in a large dictionary
# using zip codes as keys

hn_zips = ['97233', '97204', '97014', '97329', '97907', '97905', '97741', '97761', '97001', '97880',
           '97622', '97639', '97621', '97731', '97733', '97463', '97914', '97147', '97480', '97324',
           '97390', '97343', '97380', '97344', '97371', '97534', '97497', '97406', '97465', '97481']

result = {}

for z in hn_zips:
    payload["zip"] = z
    response = requests.get(api,payload)
    print(response.status_code)
    result[z] = response.json() 

#%% writing dictionary of results to output csv file

import csv

# setting up fields for the dataframe
fields = ["registry_number", "business_name", "entity_type", "registry_date", "associated_name_type", "first_name",
          "last name", "address", "city", "state", "zip", "jurisdiction", "business_details"]

# opening output file for writing
fh = open("high_need_businesses.csv", "w", newline = "")

# setting up the writer object
writer = csv.DictWriter(fh, fields)

# calling writer to write the field names in the first line of the output file
writer.writeheader()

# writing the rows based on the values in result
for key in result:
    writer.writerow(result[key])

fh.close()

