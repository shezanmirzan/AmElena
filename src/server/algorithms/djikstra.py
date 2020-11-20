import osmnx as ox
import networkx as nx
from heapq import *
from collections import deque, defaultdict
from .algorithms_abstract import AlgorithmsAbstract
from .constants import *
from .edge_weight_calculator import *


class Djikstra(AlgorithmsAbstract):
    def __init__(self, G, shortest_dist, thresh = 0.0, elev_type = MAXIMIZE, start_node = None, end_node = None):
        super(Djikstra, self).__init__(G, shortest_dist, thresh, elev_type, start_node, end_node)

    def get_route(self, parent_node, dest):
        #"returns the path given a parent mapping and the final dest"
        path = [dest]
        curr = parent_node[dest]
        while curr!=-1:
            path.append(curr)
            curr = parent_node[curr]
        return path[::-1]

    def get_updated_priority(self, node_1, node_2, edge_len, curr_priority):
        elev_type = self.elev_type
        thresh = self.thresh

        if elev_type == MAXIMIZE:
            if thresh <= 0.5:
                return edge_len*0.1 + EdgeWeightCalculator.get_weight(self.G, node_1, node_2, ELEVATION_DROP) + curr_priority
            else:
                return (edge_len*0.1 - EdgeWeightCalculator.get_weight(self.G, node_1, node_2, ELEVATION_DIFFERENCE))*edge_len*0.1
        else:
            return edge_len*0.1 + EdgeWeightCalculator.get_weight(self.G, node_1, node_2, ELEVATION_GAIN) + curr_priority

    def shortest_path(self):
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INSIDE DJIKSTRA SHORTEST PATH 0")
        if not self.check_nodes() :
            return
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INSIDE DJIKSTRA SHORTEST PATH 1")
        G, thresh, shortest_path_weight, elev_type = self.G, self.thresh, self.shortest_path_total_weight, self.elev_type
        start_node, end_node = self.start_node, self.end_node

        temp = [(0.0, 0.0, start_node)]
        seen = set()
        prior_info = {start_node: 0}
        parent_node = defaultdict(int)
        parent_node[start_node] = -1

        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INSIDE DJIKSTRA SHORTEST PATH 2")


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
                    edge_len = EdgeWeightCalculator.get_weight(self.G, this_node, n, NORMAL)

                    # Update distance btw the nodes depending on maximize(subtract) or minimize elevation(add)
                    new_priority = self.get_updated_priority(this_node, n, edge_len, curr_priority)

                    nxt_distance = curr_distance + edge_len

                    if nxt_distance <= shortest_path_weight*(1.0+thresh) and (prev is None or new_priority < prev):
                        parent_node[n] = this_node
                        prior_info[n] = new_priority
                        heappush(temp, (new_priority, nxt_distance, n))
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INSIDE DJIKSTRA SHORTEST PATH 3")

        if not curr_distance:
            return
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INSIDE DJIKSTRA SHORTEST PATH 4")

        route = self.get_route(parent_node, end_node)
        gain = self.get_path_weight(route, ELEVATION_GAIN)
        drop = self.get_path_weight(route, ELEVATION_DROP)

        # TODO: Need to remove DJIKSTRA
        return [route[:], curr_distance, gain, drop, DJIKSTRA]
