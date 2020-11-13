import osmnx as ox
import networkx as nx
from  Elena.control import constants
from collections import deque, defaultdict
from Elena.control.algorithms2 import Algorithms
from heapq import *


class ShortestPath:

    def __init__(self, G, x = 0.0, elev_type = constants.MAXIMIZE):

        self.G = G
        self.elev_type = elev_type
        self.x = x
        self.best = [[], 0.0, float('-inf'), 0.0]
        self.start_node= None
        self.end_node =None


    def get_shortest_path(self, startpt, endpt, x, elev_type = constants.MAXIMIZE, log=True):
        
        # Calculates shortest path
        G = self.G
        self.x = x/100.0
        self.elev_type = elev_type
        self.start_node, self.end_node = None, None

        #self.best = [path, totalDist, totalElevGain, totalElevDrop]
        if elev_type == constants.MAXIMIZE: 
            self.best = [[], 0.0, float('-inf'), float('-inf')]
        else:
            self.best = [[], 0.0, float('inf'), float('-inf')]

        #get shortest path
        self.start_node, d1 = ox.get_nearest_node(G, point=startpt, return_dist = True)
        self.end_node, d2   = ox.get_nearest_node(G, point=endpt, return_dist = True)

        
        

        
        

        # returns the shortest route from start to end based on distance
        self.shortest_route = nx.shortest_path(G, source=self.start_node, target=self.end_node, weight='length')
        
        print("Shortest path fetched")

        # ox.get_route function returns list of edge length for above route
        self.shortest_dist  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortest_route, 'length'))
        
        shortest_route_latlong = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.shortest_route]

        print("Trying Algorithms init")
        algorithms = Algorithms(G, self.shortest_dist, x = self.x, elev_type = elev_type, start_node = self.start_node, end_node = self.end_node)
        
        shortestPathStats = [shortest_route_latlong, self.shortest_dist, \
                            algorithms.get_Elevation(self.shortest_route, constants.ELEVATION_GAIN), algorithms.get_Elevation(self.shortest_route, constants.ELEVATION_DROP)]

        

        if(x == 0):
            return shortestPathStats, shortestPathStats

       

        
        dijkstra_route = algorithms.dijkstra()
        if log:
            print()
            print("Dijkstra route statistics")
            print(dijkstra_route[1])
            print(dijkstra_route[2])
            print(dijkstra_route[3])

        if elev_type == constants.MAXIMIZE: 
            self.best = [[], 0.0, float('-inf'), float('-inf')]
        else:
            self.best = [[], 0.0, float('inf'), float('-inf')]

        
        a_star_route = algorithms.a_star()
        if log:
            print()
            print("A star route statistics")
            print(a_star_route[1])
            print(a_star_route[2])
            print(a_star_route[3])
            print()

        self.selectBestPath(dijkstra_route, a_star_route)

        # If dijkstra or A-star doesn't return a shortest path based on elevation requirements
        if (self.elev_type == constants.MAXIMIZE and self.best[2] == float('-inf')) or (self.elev_type == constants.MINIMIZE and self.best[3] == float('-inf')):            
            return shortestPathStats, [[], 0.0, 0, 0]
        
        self.best[0] = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.best[0]]

        # If the elevation path does not match the elevation requirements
        if((self.elev_type == constants.MAXIMIZE and self.best[2] < shortestPathStats[2]) or (self.elev_type == constants.MINIMIZE and self.best[2] > shortestPathStats[2])):
            self.best = shortestPathStats

        return shortestPathStats, self.best

    def selectBestPath(self,dijkstra_route, a_star_route, log=True):
        if self.elev_type == constants.MAXIMIZE:
            if (dijkstra_route[2] > a_star_route[2]) or (dijkstra_route[2] == a_star_route[2] and dijkstra_route[1] < a_star_route[1]):
                self.best = dijkstra_route
                if log:
                    print("Dijkstra chosen as best route")
                    print()
            else:
                self.best = a_star_route
                if log:
                    print("A star chosen as best route")
                    print()
        else:
            if (dijkstra_route[2] < a_star_route[2]) or (dijkstra_route[2] == a_star_route[2] and dijkstra_route[1] < a_star_route[1]):
                self.best = dijkstra_route
                if log:
                    print("Dijkstra chosen as best route")
                    print()
            else:
                self.best = a_star_route
                if log:
                    print("A star chosen as best route")
                    print()

    

