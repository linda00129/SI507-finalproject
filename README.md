# SI507-final project

## Oregon Educational Institute Nearby Food Search System
### About the program
This program enables users to:

1. input a name of educational institute and get more details of it

2. get several other educational institute nearby

3. get a list of food services (restaurants, food delivery, etc.) nearby

   3.1. choose to see more details of a certain results by entering the corresponding number

   3.2. see the histogram for these food services' overall ratings.

To use it, please run the main.py file. If any error occurs, check whether all the .py files and data/ folder are in the same path.

The program can only work with command lines up to now. You can type your options following the instructions in program.

### About the API

Since this program is built upon Yelp's API with a limit of 500 calls/day, if anything goes wrong when searching for food services nearby, you can apply your own API on Yelp's official website and replace the ***api_code*** variable in main_func.py with yours.

### About the files

main.py: the main function of the whole program. Run it when using the program.

main_func.py: all the supporting functions. No need to run it at any time.

cache_location_save: program for caching the data structure. Run it if anything goes wrong with the cache files.

cache_yelp_save: program for caching the search result. **Don't run it if there are no errors with the cache files**: since it will make 400 searches, the API service will very possibly reach the daily limit and return wrong results. Apply your own API on Yelp's official website and replace the ***api_code*** variable in it with yours if you do need to run it.

All files in data/: the necessary data or cache files. Explore them freely without modifying any of them.

### About the data structure

There is a graph describing the connection of all the educational institutes' (locations') site zip code and mail zip code. each location are connected with one (if their two zip codes are the same) or two zip codes. BFS is used when calculating how many steps does it need to start from one location and reach another. The number of step is used in nearby location recommendation (option 2).
