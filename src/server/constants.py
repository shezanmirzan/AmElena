import logging

#Logging congig
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


#Elevation type constants
MAXIMIZE = "maximize"
MINIMIZE = "minimize"

#Cost type constants
NORMAL = "normal"
ELEVATION_DIFFERENCE = "elevation_difference"
ELEVATION_DROP = "elevation_drop"
ELEVATION_GAIN = "elevation_gain"
BOTH = "both"

#API-Key constants
GOOGLEAPIKEY = "googleapikey"


#Cached Map Name
CACHED_MAP_FILENAME = "cachedmap.p"

#Graph data attributes
DESTINATION_DISTANCE = 'dist_from_dest'
WEIGHT = 'weight'
ELEVATION = 'elevation'
LENGTH = 'length'

#Algorithms tag
EMPTY = "empty"
DJIKSTRA = "djikstra"
A_STAR = "A-star"