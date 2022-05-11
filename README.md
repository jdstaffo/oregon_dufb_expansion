# Proposed Expansion of Oregon's Double Up Food Bucks (DUFB) Program
Julia Stafford
PAI 789 Final Project, Spring 2022
Maxwell School, Syracuse University

## Background

Double Up Food Bucks (DUFB) is a program that gives a dollar-for-dollar match for fresh fruit and vegetable purchases made by SNAP recipients at participating farmers markets. In Oregon, most participating farmers markets will match up to $20 per visit on qualifying purchases made with EBT (known locally as the Oregon Trail Card). The goal of the program is to reduce the cost of healthy, nutritious food for SNAP participants and, thus, incentivize increased produce purchases. However, farmers markets may not be reliable, accessible, or affordable sources of fresh produce for many people. In recognition of this, Oregon launched a pilot program in 2019 in which the DUFB matching model can be used at 17 grocery stores across the state.

## Project Objective

This project proposes a second phase of Oregon’s DUFB grocery store pilot program, focusing on grocery stores in zip codes in which a high percentage of households receive SNAP assistance.

## External Data

**Existing grocery store data:** The 17 grocery stores currently participating in the pilot program are listed here: https://doubleuporegon.org/grocery-stores/. The store names and addresses must be manually entered into a csv file with the following columns: Store name, Street address, City, State, Zip code. In this repository, this data is in “existing_grocery_stores.csv,” and the data was collected from the DUFB Oregon website on April 7, 2022.

**Zip code tabulation area geodata:** The geodata for Census-designated zip code tabulation areas (ZCTAs) can be downloaded here: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html. In this repository, this data is in “cb_2020_us_zcta520_500k.zip,” downloaded on April 30, 2022.

**All state boundaries:** The geodata for all state boundaries, used to clip Oregon ZCTAs, can be downloaded here: https://www.weather.gov/gis/USStates. In this repository, this data is in “s_22mr22.zip,” downloaded on April 30, 2022.

## Scripts

**(1) census_api.py:** This script calls an API request to pull data from the 2019 American Community Survey (ACS) at the ZCTA level for the state of Oregon. Data requested is the total number of households in each ZCTA and the number of households in each ZCTA that received SNAP in the past 12 months.

*Input files:* none

*Output files:* “2019_ACS_API_ZCTA_request.csv”

#

**(2) census_mapping.py:** This script uses the ACS data from script (1) to calculate the percentage of households receiving SNAP in each zip code. The script then reads in geodata files to merge SNAP household data with ZCTA geography, clipping the ZCTA geography at the Oregon state border (to restrict any zip codes that are partially outside of the state boundary to only that geography which is within the state).

*QGIS:* The output files from this script can be used to create a heatmap of SNAP receipt across the state. This map uses the following layers:
-	oregon_state_geodata – geometry
-	oregon_zip_geodata – ZIP
-	oregon_zip_geodata – Percent SNAP (graduated from dark green [lowest percentage of households receiving SNAP] to dark red [highest percentage of households receiving SNAP] in 8 natural breaks (jenks))
-	NOTE: The color scheme here uses reds and greens. To increase accessibility, an orange-purple graduated scale or a grayscale graduated scale may be more readable for colorblind users.

![statewide map of SNAP receipt, color-coded](SNAP_receipt_zips.png “statewide map of SNAP receipt”)

*Input files:* “2019_ACS_API_ZCTA_request.csv,” “cb_2020_us_zcta520_500k.zip,” “s_22mr22.zip”

*Output files:* “oregon_zip_geodata.gpkg,” “oregon_state_geodata.gpkg”, “oregon_zip_geodata.csv”

*QGIS output:* “SNAP_receipt_zips.qgz”

#

**(3) existing_stores.py:** This script calls an API request to openstreetmap.org to get coordinates for the grocery stores currently participating in the DUFB pilot program. The script finds duplicates and stores without coordinates; both of these errors must be addressed manually, and prompts are given in the script.

*QGIS:* The output file from this script can be used to add the existing grocery stores to the SNAP_receipt_zips map created in step (2).

![existing DUFB grocery stores on statewide map of SNAP receipt](Existing_grocery_stores.png “existing DUFB grocery stores”)

*Input files:* “existing_grocery_stores.csv”

*Output files:* “existing_store_geodata.csv”

*QGIS output:* “Existing_grocery_stores.qgz”

#

**(4) high_snap.py:** This script uses the ACS data as edited in script (2) to select the 30 zip codes with the highest percentage of households receiving SNAP. The script then joins those zip codes onto the ZCTA geodata.

*QGIS:* The output files from this script can be used to create a map of the 30 highest SNAP zip codes and the existing DUFB grocery stores. This map uses the following layers:
-	oregon_state_geodata – geometry
-	oregon_zip_geodata – ZIP
-	existing_store_geodata
-	high_snap_geodata – Percent SNAP (no graduated color)

The map shows how the locations of existing grocery stores do – or do not – overlap with areas of high SNAP participation.

![existing DUFB grocery stores on map of high SNAP zip codes](High_SNAP_existing_grocery_stores.png “high SNAP zips, existing stores”)

*Input files:* “oregon_zip_geodata.csv,” “oregon_zip_geodata.gpkg”

*Output files:* “high_snap.csv,” “high_snap_geodata.gpkg,” “high_snap_geodata.csv”

*QGIS output:* “High_SNAP_existing_grocery_stores.qgz”

#

**(5) oregon_api.py:** This script uses the high SNAP zip codes from script (4) to call an API request to the Oregon Open Data Portal to request active businesses in the 30 high SNAP zip codes. 

*Input files:* “high_snap_geodata.csv”

*Output files:* “high_snap_businesses.csv”

#

**(6) proposed_stores.py:** This script uses the data collected from the API in script (5) to select appropriate grocery store businesses in the high SNAP zip codes. The script cleans the data and selects stores with common grocery store words. These stores must then be sorted through manually to determine if they sell fresh fruit and vegetables and would be good candidates to participate in the DUFB pilot program; guidance is given in the script.

Once the proposed grocery stores have been selected, the script then calls another API request to openstreetmap.org to get their coordinates. The script finds duplicates and stores without coordinates; as in script (3), both of these errors must be addressed manually, and prompts are given in the script.

*QGIS:* The output file from this script can be used to add the proposed grocery stores to the High_SNAP_existing_grocery_stores map created in step (4).

This map shows the grocery stores that serve high SNAP zip codes. It shows the populations that would be newly served by the proposed grocery store expansion, while also demonstrating that many high SNAP zip codes do not have grocery stores that sell produce.

![proposed and existing grocery stores on map of high SNAP zip codes](ALL_high_SNAP_grocery_stores.png “high SNAP zips, proposed and existing stores”)

*Input files:* “high_snap_businesses.csv” 

*Output files:* “initial_sort_hs_biz_geodata.csv,” “proposed_hs_biz_geodata.csv”

*QGIS output:* “ALL_high_SNAP_grocery_stores.qgz”

## Policy Recommendation

This analysis proposes that the following 18 grocery stores be added to Oregon’s Double Up Food Bucks grocery store pilot program. By allowing SNAP participants to get a dollar-for-dollar match on fresh produce purchased at these stores, the Oregon DUFB program can make further progress towards increased food security in the state.

-	B & D DEXTER MARKET, INC.
-	EL PORVENIR MINI MARKET CORP.
-	ERICKSON SUPER MARKET
-	EXTREME GROCERY DISCOUNTERS, LLC
-	FALLS CITY MARKET
-	GROCERY OUTLET OF MADRAS
-	GUERRERO'S MARKET
-	I & E FAMILY MARKET INC.
-	IZOBILIE EURO FOODS LLC
-	J & D FAMILY MARKET INC.
-	MALLARD GROCERY
-	MINGALA INTERNATIONAL MARKET
-	ONTARIO MINI MARKET AND PRODUCE LLC
-	OREGON NATURAL MARKET
-	ORIENTAL FOOD VALUE SUPERMARKET, INC.
-	TAKILMA FOOD COOP
-	YADANAR HALAL MARKET LLC
-	ZWE KA BIN GROCERY, LLC