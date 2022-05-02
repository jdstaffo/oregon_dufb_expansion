#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:19:49 2022

@author: juliadstafford
"""

import pandas as pd
from sodapy import Socrata
import requests
import os


## OREGON API FOR GROCERY STORES IN HIGH NEED ZIP CODES
# use input file to print list of zip codes
# and then do oregon api
# somehow narrow down to stores with "grocery" or "food" or "market" or "co-op"


# reading in input file of high need zip codes
high_need = pd.read_csv("high_need_geodata.csv", dtype=str)

# narrowing down to just the zip codes themselves
hn_zips = high_need["ZIP"]

print("\nHigh-need zip codes:")
print(hn_zips)

#%% OREGON API

# setting the api destination - url and specific data set
data_url = "data.oregon.gov"
data_set = "tckn-sxa6.json?zip="

# pointing to the api endpoint
client = Socrata(data_url, None, timeout=20)

# setting up for loop
for z in hn_zips:
    response = client.get(data_set, where="zip == z", limit=1000)
    if response.status_code == 200:
        print("\nSuccess: response status code is", response.status_code)
    else:
        print(response.status_code)
        print(response.text)
        assert False
    row_list = response.json()