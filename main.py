import main_func as f
import json

if __name__ == "__main__":
    location = f.cache_location_load()
    graphMap, graphZipcode, graphLoc = f.cache_graph_load()
    yelp = f.cache_yelp_load()
    print("Welcome to the Oregon Eucational Institue Nearby Food Search System!")
    print("Please enter which choice you want to contnue with:")
    print(
        "1\tEnter the name of an educational institude to see its detailed information"
    )
    print(
        "2\tEnter the name of an educational institude to get some recommendaded nearby educational institudes"
    )
    print(
        "3\tEnter the name of an educational institude to search for nearby food places"
    )
    print("q\tEnter q to quit")
    inp = input("Your choice: ")
    while inp != "q":
        if inp == "1":
            name = input(
                "\nPlease enter the FULL NAME of an educational institude, case doesn't matter: "
            )
            if name.lower() not in location["name_low"].tolist():
                print(
                    "Sorry, we cannot find the educational institude you entered. Please try again."
                )
            else:
                df_print = location[location["name_low"] == name.lower()]
                print(f.location_print_single(df_print))
        elif inp == "2":
            name = input(
                "\nPlease enter the FULL NAME of an educational institude, case doesn't matter: "
            )
            if name.lower() not in location["name_low"].tolist():
                print(
                    "Sorry, we cannot find the educational institude you entered. Please try again."
                )
            else:
                nameid = location[location["name_low"] == name.lower()][
                    "OBJECTID"
                ].tolist()[0]
                distance = f.graph_distance(graphMap, nameid, graphLoc)
                dist = {
                    key: val
                    for key, val in distance.items()
                    if val != -1 and key in graphLoc
                }
                if len(distance) > 0:
                    dist_below = {key: val for key, val in dist.items() if val <= 10 and key != nameid}
                    if len(dist_below) > 0:
                        print(
                            "Here are several educational institudes nearest to you: "
                        )
                        dist_sorted = sorted(dist_below.keys(), key=dist_below.get)[:5]
                        for i in dist_sorted:
                            print(
                                location[location["OBJECTID"] == i][
                                    "Name_Full"
                                ].tolist()[0]
                            )
                else:
                    print(
                        "Sorry, there doesn't seem to be any other educational institudes near you."
                    )
        elif inp == "3":
            name = input(
                "Please enter the FULL NAME of an educational institude, case doesn't matter: "
            )
            if name.lower() not in location["name_low"].tolist():
                print(
                    "Sorry, we cannot find the educational institude you entered. Please try again."
                )
            else:
                df_print = location[location["name_low"] == name.lower()]
                nameid = df_print["OBJECTID"].tolist()[0]
                if str(nameid) in yelp.keys():
                    foods = yelp[str(nameid)]
                else:
                    lattmp = df_print["POINT_Y"].tolist()[0]
                    longtmp = df_print["POINT_X"].tolist()[0]
                    try:
                        foods = f.yelp_search(lattmp, longtmp)
                        if "error" in foods.keys():
                            print(
                                "Sorry, something wrong happened. Please try again later"
                            )
                            continue
                    except:
                        print("Sorry, something wrong happened. Please try again later")
                        continue
                    yelp[str(nameid)] = foods
                    with open("data/cache_yelp.json", "w") as t:
                        json.dump(yelp, t)
                if len(foods["businesses"]) < 1:
                    print("Sorry, there doesn't seem to be any food places near you.")
                    continue
                foodList = [ele for ele in foods["businesses"]]
                num = len(foodList)
                for i in range(num):
                    ele = foodList[i]
                    print(str(i + 1) + ": ")
                    print(f.yelp_print_single(ele))
                print("\nPlease enter which choice you want to contnue with:")
                print(
                    "1 - "
                    + str(num)
                    + ":\tEnter the number of the food place you want to see more information"
                )
                print("0\tEnter 0 to see the histogram of their overall ratings")
                print("q\tEnter q to go back to the main menu")
                inp = input("Your choice: ")
                if inp == "0":
                    f.yelp_histRating(foodList)
                elif inp.isdigit() and int(inp) >= 1 and int(inp) <= num:
                    print(f.yelp_print_detailed(foodList[int(inp) - 1]))
                else:
                    pass
        print("\nPlease enter which choice you want to contnue with:")
        print(
            "1\tEnter the name of an educational institude to see its detailed information"
        )
        print(
            "2\tEnter the name of an educational institude to get some recommendaded nearby educational institudes"
        )
        print(
            "3\tEnter the name of an educational institude to search for nearby food places"
        )
        print("q\tEnter q to quit")
        inp = input("Your choice: ")
    print("Thank you for your using! Bye!")
