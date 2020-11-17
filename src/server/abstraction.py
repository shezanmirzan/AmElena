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

    def get_graph(self, endpt):
        
        # Updates the graph with distance from end point and returns it.
        
        if not self.cached:
            download_Map() #If the map is not cached, download the map!

        self.G = self.update_endPoint_distance(self.G,endpt)
        return self.G
    
    def download_Map(self, endpt):
        
        #Download Map from OSMNX around the fixed center if cache map is not available

        map_center = [42.384803, -72.529262]
        self.logger.warning("Downloading the Map")
        self.G = ox.graph_from_point(map_center, distance=20000, network_type='walk')
        self.G = ox.add_node_elevations(self.G, api_key=self.GOOGLEAPIKEY)
        p.dump( self.G, open( constants.CACHED_MAP_FILENAME, "wb" ) )
        self.cached = True
        self.logger.info("The Graph has been saved")

    def get_node_distance(self,latitude_source,longitude_source,latitude_destination,longitude_destination):
		
        # Computes distance between two nodes
        
        latitude_source, longitude_source = np.radians(latitude_source), np.radians(longitude_source)
        latitude_destination, longitude_destination = np.radians(latitude_destination),np.radians(longitude_destination)

        delta_longitude = longitude_destination - longitude_source
        delta_latitude = latitude_destination - latitude_source

        a = np.sin(delta_latitude / 2)**2 + np.cos(latitude_source) * np.cos(latitude_destination) * np.sin(delta_longitude / 2)**2

        radius=6371008.8 # Earth radius
        return radius * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    def update_endPoint_distance(self,G,endpt):

        #Graph is updated with Distance from all nodes in the graph to the final destination
        
        end_node=G.nodes[ox.get_nearest_node(G, point=endpt)]
        for node,data in G.nodes(data=True):
            data[constants.DESTINATION_DISTANCE] = self.get_node_distance(end_node[constants.Y_COORDINATE],end_node[constants.X_COORDINATE],G.nodes[node][constants.Y_COORDINATE],G.nodes[node][constants.X_COORDINATE])
        return G




