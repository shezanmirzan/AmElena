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
API={}
API['googleapikey']="AIzaSyCJgTZU8StpSFsIulOvO40iF684-g6m4IA"

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


#X-Y Coordinates
X_COORDINATE = 'x'
Y_COORDINATE = 'y'

#Earth Constants
DIAMETER = 12742000 # Earth Diameter