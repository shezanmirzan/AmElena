import osmnx as ox
import os
import numpy as np
import pickle as p
from src.server.constants import API
from  src.server import constants
import logging

class Graph_Loader:
    def __init__(self):

        logging.basicConfig(format = constants.LOGGING_FORMAT, level = constants.LOGGING_LEVEL)
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing Map Loader")
        self.GOOGLEAPIKEY=API[constants.GOOGLEAPIKEY]


        self.logger.info("Loading Map from cache : " + constants.CACHED_MAP_FILENAME)

        if os.path.exists("./"+ constants.CACHED_MAP_FILENAME):
            self.G = p.load( open(constants.CACHED_MAP_FILENAME, "rb" ) )
            self.cached = True
            self.logger.info("Map Loaded succesfully from cache")
        else:
            self.logger.warning("Map cannot be loaded succesfully from cache")
            self.cached = False

    def dist_nodes(self,lat1,long1,lat2,long2):
		# Given latitudes and longitudes of two nodes, returns the distance between them.
        radius=6371008.8 # Earth radius

        lat1, long1 = np.radians(lat1), np.radians(long1)
        lat2, long2 = np.radians(lat2),np.radians(long2)

        dlong,dlat = long2 - long1,lat2 - lat1

        temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
        temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
        return radius * temp2

    def update_endPoint_distance(self,G,endpt):
        #Distance from all nodes in the graph to the final destination is added
        end_node=G.nodes[ox.get_nearest_node(G, point=endpt)]
        lat1, long1 =end_node["y"],end_node["x"]
        for node,data in G.nodes(data=True):
            lat2=G.nodes[node]['y']
            long2=G.nodes[node]['x']
            distance=self.dist_nodes(lat1,long1,lat2,long2)
            data[constants.DESTINATION_DISTANCE] = distance
        return G

    def get_graph(self, endpt):
        #Returns elevation data with the graph.

        if not self.cached:
            download_Map() #If the map is not cached, download the map!

        self.G = self.update_endPoint_distance(self.G,endpt)
        return self.G

    def download_Map(self, endpt):
        #Returns elevation data with the graph.

        start = [42.384803, -72.529262]
        self.logger.warning("Downloading the Map")
        self.G = ox.graph_from_point(start, distance=20000, network_type='walk')
        self.G = ox.add_node_elevations(self.G, api_key=self.GOOGLEAPIKEY)
        p.dump( self.G, open( constants.CACHED_MAP_FILENAME, "wb" ) )
        self.cached = True
        self.logger.info("The Graph has been saved")
