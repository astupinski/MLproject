#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:28:21 2019

@author: sophiahodson
"""

import pandas as pd
from math import sqrt
import math


block = pd.read_csv("census_block_loc.csv", delimiter = ',')
tracts = pd.read_csv("nyc_census_tracts.csv",  delimiter = ',')
arrests = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv",  delimiter = ',')


def distance(lat1, lon1, lat2, lon2):
    return sqrt(math.pow((lat1-lat2),2) + math.pow((lon1-lon2),2))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

c_loc = []
for index, row in block.iterrows():
   c_loc.append({'lat':row['Latitude'],'lon':row['Longitude']})

indexz = []
distances = []
for index, row in arrests.iterrows():
    point = {'lat': row['Latitude'], 'lon': row['Longitude']}
    indexz.append(index)
    distances.append(closest(c_loc, point))
    if index%200==0:
        print(index/arrests.size)
        
census_locations = pd.DataFrame(list(zip(indexz, distances)), columns =['index', 'distance']) 

total = arrests.head(indexz[-1]+1)
total["BlockLocation"] = distances

total.to_csv("arrests_w_census_loc.csv")