import osmnx as ox
import networkx as nx
from  src.server import constants
from collections import deque, defaultdict
from heapq import *

class Algorithms:
    
    def __init__(self, G, shortest_dist, thresh = 0.0, elev_type = constants.MAXIMIZE, start_node = None, end_node = None):

        self.G = G
        self.elev_type = elev_type
        self.thresh = thresh
        self.optimal_path = [[], 0.0, float('-inf'), float('-inf'), constants.EMPTY]
        self.start_node= start_node
        self.end_node =end_node
        self.shortest_path_total_weight = shortest_dist

        if elev_type == constants.MINIMIZE:
            self.optimal_path[2] = float('inf')

    def reload(self, G):
        # Reinitialize with modified G
        self.G = G

    def get_edge_weight(self, node1, node2, weight_attribute = constants.NORMAL):

        # Compute cost between two given nodes node1, node2 with the given weight_attribute .

        G = self.G

        if node1 is None or node2 is None :
            return
        if weight_attribute == constants.NORMAL:
            try :
                return G.edges[node1, node2 ,0][constants.LENGTH]
            except :
                return G.edges[node1, node2][constants.WEIGHT]
        elif weight_attribute == constants.ELEVATION_DIFFERENCE:
            return G.nodes[node2][constants.ELEVATION] - G.nodes[node1][constants.ELEVATION]
        elif weight_attribute == constants.ELEVATION_GAIN:
            return max(0.0, G.nodes[node2][constants.ELEVATION] - G.nodes[node1][constants.ELEVATION])
        elif weight_attribute == constants.ELEVATION_DROP:
            return max(0.0, G.nodes[node1][constants.ELEVATION] - G.nodes[node2][constants.ELEVATION])
        else:
            return abs(G.nodes[node1][constants.ELEVATION] - G.nodes[node2][constants.ELEVATION])

    def get_path_weight(self, route, weight_attribute = constants.BOTH, isPiecewise = False):
        # Compute total weight for a  complete given route
        total = 0
        if isPiecewise :
            piece_elevation = []
        for i in range(len(route)-1):
            if weight_attribute == constants.BOTH:
                diff = self.get_edge_weight(route[i],route[i+1],constants.ELEVATION_DIFFERENCE)
            elif weight_attribute == constants.ELEVATION_GAIN:
                diff = self.get_edge_weight(route[i],route[i+1],constants.ELEVATION_GAIN)
            elif weight_attribute == constants.ELEVATION_DROP:
                diff = self.get_edge_weight(route[i],route[i+1],constants.ELEVATION_DROP)
            elif weight_attribute == constants.NORMAL:
                diff = self.get_edge_weight(route[i],route[i+1],constants.NORMAL)
            total += diff
            if isPiecewise :
                piece_elevation.append(diff)
        if isPiecewise:
            return total, piece_elevation
        else:
            return total

    def get_route(self, parent_node, dest):
        #"returns the path given a parent mapping and the final dest"
        path = [dest]
        curr = parent_node[dest]
        while curr!=-1:
            path.append(curr)
            curr = parent_node[curr]
        return path[::-1]

    def check_nodes(self):
        # Checks if start or end nodes are None values
        if self.start_node is None or self.end_node is None:
            return False
        return True

    # Run the dijkstra algorithm
    def dijkstra(self):
        
        #Implements Djikstra's Algorithm

        if not self.check_nodes() :
            return
        G, thresh, shortest_path_weight, elev_type = self.G, self.thresh, self.shortest_path_total_weight, self.elev_type
        start_node, end_node = self.start_node, self.end_node

        temp = [(0.0, 0.0, start_node)]
        seen = set()
        prior_info = {start_node: 0}
        parent_node = defaultdict(int)
        parent_node[start_node] = -1

        while temp:
            curr_priority, curr_distance, this_node = heappop(temp)

            if this_node not in seen:
                seen.add(this_node)
                if this_node == end_node:
                    break

                for n in G.neighbors(this_node):
                    if n in seen:
                        continue

                    prev = prior_info.get(n, None) # get past priority of the node
                    edge_len = self.get_edge_weight(this_node, n, constants.NORMAL)

                    # Update distance btw the nodes depending on maximize(subtract) or minimize elevation(add)
                    if elev_type == constants.MAXIMIZE:
                        if thresh <= 0.5:
                            nxt = edge_len*0.1 + self.get_edge_weight(this_node, n, constants.ELEVATION_DROP)
                            nxt += curr_priority
                        else:
                            nxt = (edge_len*0.1    - self.get_edge_weight(this_node, n, constants.ELEVATION_DIFFERENCE))* edge_len*0.1
                    else:
                        nxt = edge_len*0.1 + self.get_edge_weight(this_node, n, constants.ELEVATION_GAIN)
                        nxt += curr_priority

                    nxt_distance = curr_distance + edge_len

                    if nxt_distance <= shortest_path_weight*(1.0+thresh) and (prev is None or nxt < prev):
                        parent_node[n] = this_node
                        prior_info[n] = nxt
                        heappush(temp, (nxt, nxt_distance, n))

        if not curr_distance :
            return

        route = self.get_route(parent_node, end_node)
        elevation_dist, dropDist = self.get_path_weight(route, constants.ELEVATION_GAIN), self.get_path_weight(route, constants.ELEVATION_DROP)

        return [route[:], curr_distance, elevation_dist, dropDist, constants.DJIKSTRA]

    def retrace_path(self, parent_dict, this_node):
        # Reconstructs the path and plots it.
        if not parent_dict or not this_node : return
        path = [this_node]
        while this_node in parent_dict:
            this_node = parent_dict[this_node]
            path.append(this_node)

        return [path[:], self.get_path_weight(path, constants.NORMAL), self.get_path_weight(path, constants.ELEVATION_GAIN), self.get_path_weight(path, constants.ELEVATION_DROP), constants.A_STAR]

    def a_star(self):

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

        total_score[start_node] = G.nodes[start_node][constants.DESTINATION_DISTANCE]*0.1 #Start node total score will be simply the hueristic score for the start node

        while len(unvisited):

            this_node = min([(node,total_score[node]) for node in unvisited], key=lambda t: t[1])[0]

            #IF end node is reached, retrace to get the path
            if this_node == end_node:
                return self.retrace_path(parent_dict, this_node)

            #Mark the current node to be visited
            unvisited.remove(this_node)
            visited.add(this_node)

            #For all nodes that are neighbouring to the current node, update it's g-score and f-score using the formula f = g + h 
            for n in G.neighbors(this_node):
                #Continue if the neighbour node is already visited
                if n in visited:
                    continue
                
                if elev_type == constants.MINIMIZE:
                    pred_path_score = path_score[this_node] + self.get_edge_weight(this_node, n, constants.ELEVATION_GAIN)
                elif elev_type == constants.MAXIMIZE:
                    pred_path_score = path_score[this_node] + self.get_edge_weight(this_node, n, constants.ELEVATION_DROP)

                pred_path_score1 = path_score1[this_node] + self.get_edge_weight(this_node, n, constants.NORMAL)

                if n not in unvisited and pred_path_score1<=(1+thresh)*shortest_path_weight: # Discover a new node
                    unvisited.add(n)
                else:
                    if (pred_path_score >= path_score[n]) or (pred_path_score1>=(1+thresh)*shortest_path_weight):
                        continue

                parent_dict[n] = this_node
                path_score[n] = pred_path_score
                path_score1[n] = pred_path_score1
                total_score[n] = path_score[n] + G.nodes[n][constants.DESTINATION_DISTANCE]*0.1

        return self.optimal_path
