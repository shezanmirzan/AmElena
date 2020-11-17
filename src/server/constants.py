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

## API-Key
API_KEY = 'pk.eyJ1Ijoia2V2aW5qb3NlcGgxOTk1IiwiYSI6ImNqbzUxc2kwaDAybm4zanRjdm9mbndqZW8ifQ.wdJv5gB84BWVy1dAoNN6ew'

#X-Y Coordinates
X_COORDINATE = 'x'
Y_COORDINATE = 'y'