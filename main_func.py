import pandas as pd
import numpy as np
import json
from collections import deque
import requests
import matplotlib.pyplot as plt

# change this with your own API key if necessary
api_code = "0AKTgTLgFCgVsKbiogZSMtKognshM9OhhiU9Q33inCcRgzVaTiXoyFtepBKyoaHSkfbHujfwCVtQ7w0xWHZkfVqCmdFCLa3Yc7p9D7fg-vqLHH5oHiS5MdmE4bE-ZXYx"

my_apikey = "Bearer " + api_code


def cache_location_load(path="data/EDUCATIONAL_LOCATIONS.csv"):
    """
    load the location data from csv file

    Parameters
    ----------
    path : str
        the file path

    Returns
    ----------
    location : dataframe
        the dataframe of the location data

    """
    location = pd.read_csv(path)
    location.dropna(
        subset=[
            "Name_Full",
            "POINT_X",
            "POINT_Y",
            "OBJECTID",
            "Site_Zipcode",
            "Mail_Zipcode",
        ],
        inplace=True,
    )
    location["name_low"] = location["Name_Full"].str.lower()
    location["Mail_Zipcode"] = location["Mail_Zipcode"].astype(int)
    location["Site_Zipcode"] = location["Site_Zipcode"].astype(int)
    location["Website"] = location["Website"].fillna("unknown")
    return location


def cache_graph_load(path="data/cache_graph.json"):
    """
    load the graph from json cache file

    Parameters
    ----------
    path : str
        the file path

    Returns
    ----------
    graphSet : dict
        the graph content
    graphKey : set
        the set of zipcode
    graphLoc : set
        the set of location id

    """
    with open(path) as f:
        graph = json.load(f)
    graphVal = graph["graph"]
    graphZipcode = set(graph["zipcode"])
    graphLoc = set(graph["location"])
    graphMap = {int(key): set(value) for key, value in graphVal.items()}
    return graphMap, graphZipcode, graphLoc


def cache_yelp_load(path="data/cache_yelp.json"):
    """
    load the yelp search results from json cache file

    Parameters
    ----------
    path : str
        the file path

    Returns
    ----------
    cache_dict : dict
        the yelp search results

    """
    with open(path) as f:
        cache_dict = json.load(f)
    return cache_dict


def yelp_search(lat, long, apikey=my_apikey):
    """
    search a location on yelp

    Parameters
    ----------
    lat: float
        latitude of the location
    long: float
        longitude of the location
    apikey: str
        the authentication key of yelp API

    Returns
    ----------
    results_json: dict
        the search results

    """
    url_custom = (
        "https://api.yelp.com/v3/businesses/search?latitude="
        + str(lat)
        + "&longitude="
        + str(long)
        + "&term=food$limit=20"
    )
    headers = {"Authorization": apikey, "accept": "application/json"}
    results = requests.get(url_custom, headers=headers)
    results_json = json.loads(results.text)
    return results_json


def yelp_print_single(single):
    """
    print the search results of a single location

    Parameters
    ----------
    single: dict
        one of the search results

    Returns
    ----------
    result_text: str
        the formatted text of the single result

    """
    name, categories, rating, address = (
        single.get("name", "unknown"),
        single.get("categories", "unknown"),
        single.get("rating", "unknown"),
        single.get("display_address", ["unknown"]),
    )
    result_text = ""
    result_text += (
        str(name)
        + "\n|\tcategories: "
        + (
            str.join(", ", [ele["title"] for ele in categories])
            if categories != "unknown"
            else "unknown"
        )
        + "\n|\trating: "
        + str(rating)
        + "\n|\tlocation: "
        + str.join(", ", address)
    )
    return result_text


def yelp_print_detailed(single):
    """
    print the search results of a single location

    Parameters
    ----------
    single: dict
        one of the search results

    Returns
    ----------
    result_text: str
        the formatted text of the single result

    """
    name, categories, rating, address, close, web, reviews, phone, dist = (
        single.get("name", "unknown"),
        single.get("categories", "unknown"),
        single.get("rating", "unknown"),
        single.get("display_address", ["unknown"]),
        single.get("is_closed", "unknown"),
        single.get("url", "unknown"),
        single.get("review_count", "unknown"),
        single.get("display_phone", "unknown"),
        single.get("distance", "unknown"),
    )
    result_text = ""
    result_text += (
        str(name)
        + "\n|\tcategories: "
        + (
            str.join(", ", [ele["title"] for ele in categories])
            if categories != "unknown"
            else "unknown"
        )
        + "\n|\trating: "
        + str(rating)
        + "\n|\tnumber of reviews: "
        + str(reviews)
        + "\n|\tis it closed: "
        + ("No" if close == False else "Yes")
        + "\n|\tlocation: "
        + str.join(", ", address)
        + "\n|\tdistance from here: "
        + (
            "unknown"
            if dist == "unknown"
            else str(round(float(dist) / 1609.344, 2)) + " miles"
        )
        + "\n|\tphone number: "
        + str(phone)
        + "\n|\tYelp webpage: "
        + str(web)
    )
    return result_text


def yelp_avgRating(lists):
    """
    calculate the average rating of all search results

    Parameters
    ----------
    lists: list(dict)
        a list of search results

    Returns
    ----------
    avgRating: float
        the average rating of the list of search results

    """
    sumRating = 0
    countRating = 0
    for ele in lists:
        if ele.get("rating", "unknown") != "unknown":
            sumRating += ele["rating"]
            countRating += 1
    if countRating == 0:
        return "unknown"
    else:
        return round(sumRating / countRating, 2)


def yelp_histRating(lists):
    """
    show the histogram of the ratings for all search results

    Parameters
    ----------
    lists: list(dict)
        a list of search results

    """
    ratingList = []
    for ele in lists:
        if ele.get("rating", "unknown") != "unknown":
            ratingList.append(ele["rating"])
    bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    plt.hist(ratingList, bins=bins, edgecolor="black")
    plt.xlabel("Ratings")
    plt.ylabel("Number of ratings")
    plt.title("Rating Distribution")
    plt.show()
    return


def location_print_single(df):
    """
    print the location information of a single location

    Parameters
    ----------
    df: dataframe
        one of the location data

    Returns
    ----------
    result_text: str
        the formatted text of the single location

    """
    result_text = ""
    result_text += (
        str(df["Name_Full"].tolist()[0])
        + "\n|\tcurrent status: "
        + str(df["STATUS"].tolist()[0])
        + "\n|\taddress: "
        + str(df["Site_Address_Line1"].tolist()[0])
        + ", "
        + str(df["Site_City"].tolist()[0])
        + "\n|\tmailing zipcode: "
        + str(df["Mail_Zipcode"].tolist()[0])
        + "\n|\tcontact phone: "
        + str(df["Phone"].tolist()[0])
        + "\n|\tcontact e-mail: "
        + str(df["Email"].tolist()[0])
        + "\n|\twebsite: "
        + str(df["Website"].tolist()[0])
    )
    return result_text


def graph_distance(graph, A, locs):
    """
    use BFS to get the distance from A to all points

    Parameters
    ----------
    graph : dict
        the dictionary of nodes and their adjacent nodes
    locs : set
        a set of all nodes currently in graph
    A : int
        the starter

    Returns
    ----------
    dist : dict
        the dictionary of distance from starter A to other nodes

    """
    dist = {key: -1 for key in locs}
    dist[A] = 0
    visited = set()
    queue = deque()
    visited.add(A)
    queue.append(A)
    while queue:
        curr = queue.popleft()
        for ele in graph[curr]:
            if ele not in visited:
                dist[ele] = dist[curr] + 1
                queue.append(ele)
                visited.add(ele)
    return dist


# if __name__ == "__main__":
#     pass
