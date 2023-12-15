import pandas as pd
import numpy as np
import json

# load and preprocess data
location = pd.read_csv("data/EDUCATIONAL_LOCATIONS.csv")
location.dropna(
    subset=["POINT_X", "POINT_Y", "OBJECTID", "Site_Zipcode", "Mail_Zipcode"],
    inplace=True,
)

idList = location["OBJECTID"].astype(int).tolist()
siteList = location["Site_Zipcode"].astype(int).tolist()
mailList = location["Mail_Zipcode"].astype(int).tolist()
graphList = {}
zipcodeSet = set()
locSet = set()

# set up the graph
for i in range(len(idList)):
    if siteList[i] not in zipcodeSet:
        graphList[siteList[i]] = set()
        zipcodeSet.add(siteList[i])
    graphList[siteList[i]].add(idList[i])
    if mailList[i] not in zipcodeSet:
        graphList[mailList[i]] = set()
        zipcodeSet.add(mailList[i])
    graphList[mailList[i]].add(idList[i])
    graphList[idList[i]] = {siteList[i], mailList[i]}
    locSet.add(idList[i])

# export to file
graphAll = {}
graphAll["graph"] = {key: list(value) for key, value in graphList.items()}
graphAll["zipcode"] = list(zipcodeSet)
graphAll["location"] = list(locSet)
with open("data/cache_graph.json", "w") as f:
    json.dump(graphAll, f)
