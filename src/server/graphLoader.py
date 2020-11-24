import osmnx as ox
import os
import pickle as pkl
import logging

from src.server.constants import API
from  src.server import constants
from src.server import config
from src.server.distance import DistanceCalculator

class Graph_Loader:
    
    def __init__(self):

        logging.basicConfig(format = constants.LOGGING_FORMAT, level = constants.LOGGING_LEVEL)
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing Map Loader")
        self.GOOGLEAPIKEY=API[constants.GOOGLEAPIKEY]

        self.distance_calculator = DistanceCalculator(config.DIST_TYPE)

        self.logger.info("Loading Map from cache : " + constants.CACHED_MAP_FILENAME)

        if os.path.exists("./"+ constants.CACHED_MAP_FILENAME):
            self.G = pkl.load( open(constants.CACHED_MAP_FILENAME, "rb" ) )
            self.cached = True
            self.logger.info("Map Loaded succesfully from cache")
        else:
            self.logger.warning("Map cannot be loaded succesfully from cache")
            self.cached = False

    def get_graph(self, loc):
        
        # Updates the graph with distance from end point and returns it.
        
        if not self.cached:
            self.download_Map() #If the map is not cached, download the map!

        self.G = self.update_endPoint_distance(self.G,loc)
        return self.G

    def update_endPoint_distance(self,G,loc):

        #Graph is updated with Distance from all nodes in the graph to the final destination
        
        end_node=G.nodes[ox.get_nearest_node(G, point=loc)]
        for node,data in G.nodes(data=True):
            data[constants.DESTINATION_DISTANCE] = self.distance_calculator.get_node_distance(end_node[constants.Y_COORDINATE],end_node[constants.X_COORDINATE],G.nodes[node][constants.Y_COORDINATE],G.nodes[node][constants.X_COORDINATE])
        return G

    def download_Map(self):
        
        #Download Map from OSMNX around the fixed center(can be changed in config.py) if cache map is not available

        self.logger.warning("Downloading the Map")
        self.G = ox.graph_from_point(config.MAP_CENTER, dist=20000, network_type='walk')
        self.G = ox.add_node_elevations(self.G, api_key=self.GOOGLEAPIKEY)
        pkl.dump( self.G, open( constants.CACHED_MAP_FILENAME, "wb" ) )
        self.cached = True
        self.logger.info("The Graph has been saved")