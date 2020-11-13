import osmnx as ox
import networkx as nx
from  Elena.control import constants
from collections import deque, defaultdict
from heapq import *

class Algorithms:
    def __init__(self, G, shortest_dist, x = 0.0, elev_type = constants.MAXIMIZE, start_node = None, end_node = None):

        self.G = G
        self.elev_type = elev_type
        self.x = x
        self.best = [[], 0.0, float('-inf'), 0.0]
        self.start_node= start_node
        self.end_node =end_node
        self.shortest_dist = shortest_dist

        if elev_type == constants.MAXIMIZE: 
            self.best = [[], 0.0, float('-inf'), float('-inf')]
        else:
            self.best = [[], 0.0, float('inf'), float('-inf')]
        print("Algorithm init succesful")

    def reload(self, G):
        # Reinitialize with modified G
        self.G = G


    def get_cost(self, node1, node2, cost_type = constants.NORMAL):
        
        # Compute cost between two given nodes node1, node2 with the given cost_type .
        G = self.G
        if node1 is None or node2 is None : 
            return 
        if cost_type == constants.NORMAL:
            try : 
                return G.edges[node1, node2 ,0]["length"]
            except : 
                return G.edges[node1, node2]["weight"]
        elif cost_type == constants.ELEVATION_DIFFERENCE:
            return G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"]
        elif cost_type == constants.ELEVATION_GAIN:
            return max(0.0, G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"])
        elif cost_type == constants.ELEVATION_DROP:
            return max(0.0, G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])
        else:
            return abs(G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])
        


    def get_Elevation(self, route, cost_type = constants.BOTH, isPiecewise = False):
        # Compute total cost or piecewise cost for a given route
        total = 0
        if isPiecewise : 
            piece_elevation = []
        for i in range(len(route)-1):
            if cost_type == constants.BOTH:
                diff = self.get_cost(route[i],route[i+1],constants.ELEVATION_DIFFERENCE)	
            elif cost_type == constants.ELEVATION_GAIN:
                diff = self.get_cost(route[i],route[i+1],constants.ELEVATION_GAIN)
            elif cost_type == constants.ELEVATION_DROP:
                diff = self.get_cost(route[i],route[i+1],constants.ELEVATION_DROP)
            elif cost_type == constants.NORMAL:
                diff = self.get_cost(route[i],route[i+1],constants.NORMAL)
            total += diff
            if isPiecewise : 
                piece_elevation.append(diff)
        if isPiecewise:
            return total, piece_elevation
        else:
            return total

    

    def get_route(self, parent_node, dest):
        "returns the path given a parent mapping and the final dest"
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
            #Implements Dijkstra's Algorithm

        print("Implementing Djisktra")
        
        if not self.check_nodes() : 
            return
        G, x, shortest, elev_type = self.G, self.x, self.shortest_dist, self.elev_type
        start_node, end_node = self.start_node, self.end_node

        temp = [(0.0, 0.0, start_node)]
        seen = set()
        prior_info = {start_node: 0}
        parent_node = defaultdict(int)
        parent_node[start_node] = -1

        while temp:
            curr_priority, curr_distance, curr_node = heappop(temp)
            
            if curr_node not in seen:
                seen.add(curr_node)
                if curr_node == end_node:
                    break

                for n in G.neighbors(curr_node):
                    if n in seen: 
                        continue
                    
                    prev = prior_info.get(n, None) # get past priority of the node
                    edge_len = self.get_cost(curr_node, n, constants.NORMAL)
                    
                    # Update distance btw the nodes depending on maximize(subtract) or minimize elevation(add)
                    if elev_type == constants.MAXIMIZE:
                        if x <= 0.5:
                            nxt = edge_len*0.1 + self.get_cost(curr_node, n, constants.ELEVATION_DROP)
                            nxt += curr_priority
                        else:
                            nxt = (edge_len*0.1 - self.get_cost(curr_node, n, constants.ELEVATION_DIFFERENCE))* edge_len*0.1
                    else:
                        nxt = edge_len*0.1 + self.get_cost(curr_node, n, constants.ELEVATION_GAIN)
                        nxt += curr_priority
                    
                    nxt_distance = curr_distance + edge_len
                    
                    if nxt_distance <= shortest*(1.0+x) and (prev is None or nxt < prev):
                        parent_node[n] = curr_node
                        prior_info[n] = nxt
                        heappush(temp, (nxt, nxt_distance, n))        
        
        if not curr_distance : 
            return

        route = self.get_route(parent_node, end_node)
        elevation_dist, dropDist = self.get_Elevation(route, constants.ELEVATION_GAIN), self.get_Elevation(route, constants.ELEVATION_DROP)

        return [route[:], curr_distance, elevation_dist, dropDist]


    def retrace_path(self, from_node, curr_node):
        # Reconstructs the path and plots it.
        if not from_node or not curr_node : return
        total = [curr_node]
        while curr_node in from_node:
            curr_node = from_node[curr_node]
            total.append(curr_node)
        
        return [total[:], self.get_Elevation(total, constants.NORMAL), self.get_Elevation(total, constants.ELEVATION_GAIN), self.get_Elevation(total, constants.ELEVATION_DROP)]




    def a_star(self):
        # Implements A* algorithm for calculating distances. 
        evaluated = set() #evaluated node set      
        toEval = set() # nodes that are not evaluated
        best_node = {} # best cost to end
        costToStart = {} # cost of node to start node
        costToStart1 = {}
        final_score = {} # dist between start node and end node thru a particular node


        if not self.check_nodes() : 
            return
        G, min_dist = self.G, self.shortest_dist
        x, elev_type = self.x, self.elev_type
        start_node= self.start_node
        end_node = self.end_node
        
        toEval.add(start_node)
   
        for node in G.nodes():
            costToStart[node] = float("inf")
        
        costToStart[start_node] = 0 

        for node in G.nodes():
            costToStart1[node] = float("inf")
        costToStart1[start_node] = 0

        final_score[start_node] = G.nodes[start_node]['dist_from_dest']*0.1
        
        while len(toEval):
            curr_node = min([(node,final_score[node]) for node in toEval], key=lambda t: t[1])[0]            
            if curr_node == end_node:
                return self.retrace_path(best_node, curr_node)

            
            toEval.remove(curr_node)
            evaluated.add(curr_node)
            for n in G.neighbors(curr_node):
                if n in evaluated: 
                    continue 
                if elev_type == constants.MINIMIZE:
                    pred_costToStart = costToStart[curr_node] + self.get_cost(curr_node, n, constants.ELEVATION_GAIN)
                elif elev_type == constants.MAXIMIZE:
                    pred_costToStart = costToStart[curr_node] + self.get_cost(curr_node, n, constants.ELEVATION_DROP)

                pred_costToStart1 = costToStart1[curr_node] + self.get_cost(curr_node, n, constants.NORMAL)

                if n not in toEval and pred_costToStart1<=(1+x)*min_dist:# Discover a new node
                    toEval.add(n)
                else: 
                    if (pred_costToStart >= costToStart[n]) or (pred_costToStart1>=(1+x)*min_dist):
                        continue 

                best_node[n] = curr_node
                costToStart[n] = pred_costToStart
                costToStart1[n] = pred_costToStart1
                final_score[n] = costToStart[n] + G.nodes[n]['dist_from_dest']*0.1
        
        return self.best

