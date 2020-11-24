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

# Requesthandler parameters
FEATURE = "Feature"
LINESTRING = "LineString"

# RequestHandler attributes
PROPERTIES = "properties"
GEOMETRY = "geometry"
TYPE = "type"
COORDINATES = "coordinates"
ELEVATION_ROUTE = "elevation_route"
SHORTEST_ROUTE = "shortest_route"
SHORTEST_DIST = "shortDist"
SHORTEST_GAIN = "gainShort"
SHORTEST_DROP = "dropShort"
ELE_DISTANCE = "elenavDist"
ELE_GAIN = "gainElenav"
ELE_DROP = "dropElenav"
POPUP_FLAG = "popup_flag"
START_ADDRESS = "start"
END_ADDRESS = "end"