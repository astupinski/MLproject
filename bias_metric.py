#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:11:28 2019

@author: sophiahodson
"""

import pandas as pd

tracts = pd.read_csv("nyc_census_tracts.csv",  delimiter = ',')

def bias(pred_white,pred_non_white, tract_number):
    area = tracts[tracts['CensusTract']== tract_number]
    percent_white = area["White"]
    percent_non_white = 100 - area["White"]
    bias_metric = (pred_white/percent_white) - (pred_non_white/percent_non_white)
    return bias_metric

