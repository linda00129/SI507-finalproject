import pandas as pd
import numpy as np
import requests
import json

# Load the dataframe for location to search
location = pd.read_csv("data/EDUCATIONAL_LOCATIONS.csv")
location.dropna(
    subset=["POINT_X", "POINT_Y", "OBJECTID", "Site_Zipcode", "Mail_Zipcode"],
    inplace=True,
)
longList = location["POINT_X"].tolist()
latList = location["POINT_Y"].tolist()
idList = location["OBJECTID"].tolist()

# set up the authentication
# change this with your own API key if necessary
api_code = "0AKTgTLgFCgVsKbiogZSMtKognshM9OhhiU9Q33inCcRgzVaTiXoyFtepBKyoaHSkfbHujfwCVtQ7w0xWHZkfVqCmdFCLa3Yc7p9D7fg-vqLHH5oHiS5MdmE4bE-ZXYx"
apikey = "Bearer " + api_code
headers = {"Authorization": apikey, "accept": "application/json"}

# cache the first 400 search results
cache_dict = {}
num = 400
for i in range(num):
    url_custom = (
        "https://api.yelp.com/v3/businesses/search?latitude="
        + str(latList[i])
        + "&longitude="
        + str(longList[i])
        + "&term=food$limit=20"
    )
    test = requests.get(url_custom, headers=headers)
    testjson = json.loads(test.text)
    cache_dict[idList[i]] = testjson

# export to file
with open("data/cache_yelp.json", "w") as f:
    json.dump(cache_dict, f)
