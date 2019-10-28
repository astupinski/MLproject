import pandas as pd
import re
def arrest2census(arrest_data):
    arrest_data.PERP_RACE[arrest_data.PERP_RACE.str.contains("WHITE")]=0
    arrest_data.PERP_RACE[arrest_data.PERP_RACE != 0]=1
    arrest_data = arrest_data.groupby(["PERP_RACE","BlockLocation"]).size().reset_index(name='counts')
    blockLocation = arrest_data["BlockLocation"]
    blockLat = [float(re.findall(r'[-\d\.]+', bl)[0]) for bl in blockLocation]
    blockLon = [float(re.findall(r'[-\d\.]+', bl)[1]) for bl in blockLocation]
    arrest_data["blockLat"]=blockLat
    arrest_data["blockLon"]=blockLon
    arrest_data = arrest_data.drop("BlockLocation", axis=1)
    arrest_data = arrest_data.rename(columns={"counts": "Num_Arrests", "PERP_RACE": "Race"})
    block_data = pd.read_csv("census_block_loc.csv")
    block_data = pd.merge(left=arrest_data, right=block_data,
                          left_on=["blockLat","blockLon"], right_on=["Latitude","Longitude"])
    census_data = pd.read_csv("nyc_census_tracts.csv")
    tracts = block_data["BlockCode"]
    tracts = [int(str(tract)[:-4]) for tract in tracts]
    block_data["tracts"]=tracts
    block_data = block_data.drop(columns=["Latitude","Longitude","BlockCode","County","blockLat","blockLon"])
    merged_data = pd.merge(left=block_data, right=census_data, left_on="tracts", right_on="CensusTract")
    merged_data = merged_data.drop("tracts", axis=1)
    return merged_data

#here is me putting null values for the lat and lon temporarily to make sure it works
arrest_data = pd.read_csv("arrests_w_census_loc.csv")
merged_data = arrest2census(arrest_data)