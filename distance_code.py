#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:28:21 2019

@author: sophiahodson
"""

import pandas as pd
from math import cos, asin, sqrt
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
    #row['closest_census_loc'] = closest(c_loc, point)



indexz2 = indexz
distances2 = distances

census_locations = pd.DataFrame(list(zip(indexz2, distances2)), columns =['index', 'distance']) 

final_out = arrests.head(100661)
final_out["BlockLocation"] = distances2

final_out.to_csv("arrests_w_census_loc.csv")
