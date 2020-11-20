import osmnx as ox
import networkx as nx
from heapq import *
from collections import deque, defaultdict
from .algorithms_abstract import AlgorithmsAbstract
from .constants import *
from .edge_weight_calculator import *


class AStar(AlgorithmsAbstract):
    def __init__(self, G, shortest_dist, thresh = 0.0, elev_type = MAXIMIZE, start_node = None, end_node = None):
        super(AStar, self).__init__(G, shortest_dist, thresh, elev_type, start_node, end_node)

    def retrace_path(self, parent_dict, this_node):
        # Reconstructs the path and plots it.
        if not parent_dict or not this_node : return
        path = [this_node]
        while this_node in parent_dict:
            this_node = parent_dict[this_node]
            path.append(this_node)

        return path

    def g(self, this_node, n):
        elev_type = self.elev_type

        if elev_type == MINIMIZE:
            return EdgeWeightCalculator.get_weight(self.G, this_node, n, ELEVATION_GAIN)
        elif elev_type == MAXIMIZE:
            return EdgeWeightCalculator.get_weight(self.G, this_node, n, ELEVATION_DROP)

    def h(self, n):
        return self.G.nodes[n][DESTINATION_DISTANCE]*0.1

    def shortest_path(self):
        # Implements A* algorithm for calculating distances with hueristics as distance from Destination node(calculated using latitudes and longitudes)
        #Followed the algorithm idea from https://dhruvs.space/posts/understanding-the-a-star-algorithm/

        #Create set for already visited and unvisited nodes
        visited = set() #visited node set
        unvisited = set() # nodes that are not visited

        parent_dict = {} # Dictionary to hold the parent node

        path_score = {} # Dictionaries to score the g-score for each node
        path_score1 = {}

        total_score = {} # dist between start node and end node thru a particular node

        if not self.check_nodes() :
            return

        G, shortest_path_weight = self.G, self.shortest_path_total_weight
        thresh, elev_type = self.thresh, self.elev_type
        start_node= self.start_node
        end_node = self.end_node

        #Start with the unvisited consisting of a single node, which is the start node.
        unvisited.add(start_node)

        #Set up g-scores for all nodes to infinity except the start node, which is set to zero. As a result, f-scores for all nodes except the start node is also infinity.
        for node in G.nodes():
            path_score[node] = float("inf")
            path_score1[node] = float("inf")

        path_score[start_node] = 0
        path_score1[start_node] = 0

        total_score[start_node] = G.nodes[start_node][DESTINATION_DISTANCE]*0.1 #Start node total score will be simply the hueristic score for the start node

        while len(unvisited):

            this_node = min([(node,total_score[node]) for node in unvisited], key=lambda t: t[1])[0]

            #IF end node is reached, retrace to get the path
            if this_node == end_node:
                route = self.retrace_path(parent_dict, this_node)
                curr_distance = self.get_path_weight(route, NORMAL)
                gain = self.get_path_weight(route, ELEVATION_GAIN)
                drop = self.get_path_weight(route, ELEVATION_DROP)
                return [route[:], curr_distance, gain, drop, A_STAR]

            #Mark the current node to be visited
            unvisited.remove(this_node)
            visited.add(this_node)

            #For all nodes that are neighbouring to the current node, update it's g-score and f-score using the formula f = g + h
            for n in G.neighbors(this_node):
                #Continue if the neighbour node is already visited
                if n in visited:
                    continue

                pred_path_score = path_score[this_node] + self.g(this_node, n)
                pred_path_score1 = path_score1[this_node] + EdgeWeightCalculator.get_weight(self.G, this_node, n, NORMAL)

                if n not in unvisited and pred_path_score1<=(1+thresh)*shortest_path_weight: # Discover a new node
                    unvisited.add(n)
                else:
                    if (pred_path_score >= path_score[n]) or (pred_path_score1>=(1+thresh)*shortest_path_weight):
                        continue

                parent_dict[n] = this_node
                path_score[n] = pred_path_score
                path_score1[n] = pred_path_score1
                total_score[n] = path_score[n] + self.h(n)

        return self.optimal_path
