import osmnx as ox
import networkx as nx
from  src.server import constants
from collections import deque, defaultdict
from heapq import *
import logging
from src.server.algorithms import Djikstra, AStar


class ShortestPath:

    def __init__(self, G, x = 0.0, elev_type = constants.MAXIMIZE):
        self.logger = logging.getLogger(__name__)
        self.G = G
        self.elev_type = elev_type
        self.x = x
        self.optimal_path = [[], 0.0, float('-inf'), 0.0, constants.EMPTY]
        self.start_node= None
        self.end_node =None


    def get_shortest_path(self, startpt, endpt, x, elev_type = constants.MAXIMIZE, log=True):

        # Calculates shortest path
        G = self.G
        self.x = x/100.0
        self.elev_type = elev_type
        self.start_node, self.end_node = None, None

        #get shortest path
        self.start_node, d1 = ox.get_nearest_node(G, point=startpt, return_dist = True)
        self.end_node, d2   = ox.get_nearest_node(G, point=endpt, return_dist = True)


        # returns the shortest route from start to end based on distance
        self.shortest_route = nx.shortest_path(G, source=self.start_node, target=self.end_node, weight='length')

        print("Shortest path fetched")

        # ox.get_route function returns list of edge length for above route
        self.shortest_dist  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortest_route, 'length'))

        shortest_route_latlong = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.shortest_route]

        djikstra = Djikstra(G, self.shortest_dist, thresh = self.x, elev_type = elev_type, start_node = self.start_node, end_node = self.end_node)

        shortestPathStats = [shortest_route_latlong, self.shortest_dist, djikstra.get_path_weight(self.shortest_route, constants.ELEVATION_GAIN), djikstra.get_path_weight(self.shortest_route, constants.ELEVATION_DROP)]



        if(x == 0):
            return shortestPathStats, shortestPathStats

        #Get route using Djikstra's algorithm
        self.resetBestPath()
        djikstra_route = djikstra.shortest_path()
        self.print_route_statistics(djikstra_route)


        #Get route using A* algorithm
        a_star = AStar(G, self.shortest_dist, thresh = self.x, elev_type = elev_type, start_node = self.start_node, end_node = self.end_node)
        self.resetBestPath()
        a_star_route = a_star.shortest_path()
        self.print_route_statistics(a_star_route)

        self.selectBestPath(djikstra_route, a_star_route)

        # If dijkstra or A-star doesn't return a shortest path based on elevation requirements
        if (self.elev_type == constants.MAXIMIZE and self.optimal_path[2] == float('-inf')) or (self.elev_type == constants.MINIMIZE and self.optimal_path[3] == float('-inf')):
            return shortestPathStats, [[], 0.0, 0, 0, constants.EMPTY]

        self.optimal_path[0] = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.optimal_path[0]]

        # If the elevation path does not match the elevation requirements
        if((self.elev_type == constants.MAXIMIZE and self.optimal_path[2] < shortestPathStats[2]) or (self.elev_type == constants.MINIMIZE and self.optimal_path[2] > shortestPathStats[2])):
            self.optimal_path = shortestPathStats

        return shortestPathStats, self.optimal_path

    def selectBestPath(self,djikstra_route, a_star_route, log=True):

        if self.elev_type == constants.MAXIMIZE:
            self.optimal_path = djikstra_route if (djikstra_route[2] > a_star_route[2]) or (djikstra_route[2] == a_star_route[2] and djikstra_route[1] < a_star_route[1]) else a_star_route
        else:
            self.optimal_path = djikstra_route if (djikstra_route[2] < a_star_route[2]) or (djikstra_route[2] == a_star_route[2] and djikstra_route[1] < a_star_route[1]) else a_star_route

        self.logger.info("Best selected route is " + self.optimal_path[4])

    def resetBestPath(self):
        if self.elev_type == constants.MAXIMIZE:
            self.optimal_path = [[], 0.0, float('-inf'), float('-inf'), constants.EMPTY]
        else:
            self.optimal_path = [[], 0.0, float('inf'), float('-inf'), constants.EMPTY]

    def print_route_statistics(self, route):
        print("************************************************")
        print("Algorithm :" + route[4])
        print("Total Distance: " + str(route[1]))
        print("Elevation Gain: " + str(route[2]))
        print("Elevation Drop: " + str(route[3]))
