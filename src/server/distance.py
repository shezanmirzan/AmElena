import math
import numpy as np

from  src.server import constants

class DistanceCalculator:

    def __init__(self, distance_type="haversine"):
        self.distance_type = distance_type
    

    def get_node_distance(self,latitude_source,longitude_source,latitude_destination,longitude_destination):
		
        # Computes distance between two nodes

        if self.distance_type == "euclidean":
            return self.get_Euclidean_distance(latitude_source,longitude_source,latitude_destination,longitude_destination)
        
        elif self.distance_type == "manhattan":
            return self.get_Manhattan_distance(latitude_source,longitude_source,latitude_destination,longitude_destination)

        elif self.distance_type == "haversine":
            return self.get_Haversine_distance(latitude_source,longitude_source,latitude_destination,longitude_destination)

        else:
            raise ValueError("Invalid config parameter set for Distance type")
        
        pass


    def get_Manhattan_distance(self,latitude_source,longitude_source,latitude_destination,longitude_destination):

        return abs(latitude_source - latitude_destination) + abs(longitude_source - longitude_destination)


    def get_Euclidean_distance(self,latitude_source,longitude_source,latitude_destination,longitude_destination):

        return sqrt((latitude_source - latitude_destination)**2 + (longitude_source - longitude_destination)**2)


    def get_Haversine_distance(self,latitude_source,longitude_source,latitude_destination,longitude_destination):
        
        latitude_source, longitude_source = np.radians(latitude_source), np.radians(longitude_source)
        latitude_destination, longitude_destination = np.radians(latitude_destination),np.radians(longitude_destination)

        a = np.sin((latitude_destination - latitude_source) / 2)**2 + np.cos(latitude_source) * np.cos(latitude_destination) * np.sin((longitude_destination - longitude_source) / 2)**2

        
        return np.arctan2(np.sqrt(a), np.sqrt(1 - a)) * constants.DIAMETER 
