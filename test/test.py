import sys
sys.path.insert(1, sys.path[0][:-5])
import osmnx as ox
import networkx as nx
import pickle as p
import geopy
from geopy.geocoders import Nominatim

from src.server.graphLoader import *
from src.server.algorithms import *
from src.server.shortestPath import *
from src.server.requesthandler import get_json, get_data, get_coordinates, get_address

def Test(value = ""):
    def temp(function):
        def condition(*args, **kwargs):
            try:
                function(*args,**kwargs)
                print("Test Passed" ) # if a condition passes
            except Exception as error:
                print("Test Failed")  # if a condition failed
                print(error)
        return condition
    return temp

@Test("")
def test_get_graph(end):
    print("# Testing the get_graph method in graphloader.py")

    loader = Graph_Loader()
    G = loader.get_graph(end)
    assert isinstance(G, nx.classes.multidigraph.MultiDiGraph)

@Test("")
def test_get_route(A):
    print("Testing get_route method in algorithms.py")
    c = A.get_route({0 : 1, 1 : 2, 2 : -1}, 0)
    assert isinstance(c, list)
    assert c == [2, 1, 0]

@Test("")
def test_get_path_weight(A):
    print("Testing get_path_weight method in algorithms.py")

    route = [0, 3, 4, 2]
    c, p = A.get_path_weight(route, weight_attribute = "both", isPiecewise = True)
    assert isinstance(c, float)
    assert isinstance(p, list)
    assert c == 0.0
    assert p == [1.0, 0.0, -1.0]

    c = A.get_path_weight(route, weight_attribute = "both")
    assert isinstance(c, float)
    assert c == 0.0

    c, p = A.get_path_weight(route, weight_attribute = "elevation_gain", isPiecewise = True)
    assert isinstance(c, float)
    assert isinstance(p, list)
    assert c == 1.0
    assert p == [1.0, 0.0, 0.0]

    c, p = A.get_path_weight(route, weight_attribute = "elevation_drop", isPiecewise = True)
    assert isinstance(c, float)
    assert isinstance(p, list)
    assert c == 1.0
    assert p == [0.0, 0.0, 1.0]

    c, p = A.get_path_weight(route, weight_attribute = "normal", isPiecewise = True)
    assert isinstance(c, float)
    assert isinstance(p, list)
    assert c == 6.726999999999999
    assert p == [1.414, 4.0, 1.313]

@Test("")
def test_get_edge_weight(A, node1=0, node2=1):
    print("Testing get_edge_weight method in algorithms.py")

    c = A.get_edge_weight(0, 1, weight_attribute="normal")
    assert isinstance(c, float)
    assert c == 3.0

    c = A.get_edge_weight(0, 3, weight_attribute="elevation_difference")
    assert isinstance(c, float)
    assert c == 1.0

    c = A.get_edge_weight(5, 4, weight_attribute="elevation_difference")
    assert isinstance(c, float)
    assert c == -2.0

    c = A.get_edge_weight(1, 4, weight_attribute="elevation_gain")
    assert isinstance(c, float)
    assert c == 1.0

    c = A.get_edge_weight(4, 1, weight_attribute="elevation_gain")
    assert isinstance(c, float)
    assert c == 0.0

    c = A.get_edge_weight(6, 2, weight_attribute="elevation_drop")
    assert isinstance(c, float)
    assert c == 4.0

    c = A.get_edge_weight(2, 6, weight_attribute="elevation_drop")
    assert isinstance(c, float)
    assert c == 0.0

    c = A.get_edge_weight(2, 6, weight_attribute="abs")
    assert isinstance(c, float)
    assert c == 4.0

    c = A.get_edge_weight(6, 2, weight_attribute="abs")
    assert isinstance(c, float)
    assert c == 4.0

@Test("")
def test_get_shortest_path(startpt, endpt):
    print("Testing get_shortest_path method in shortestPath.py")
    x = 100.0

    # startpt = (42.350541, -72.528715)
    # endpt = (42.350541, -72.528715)
    #
    loader = Graph_Loader()
    G = loader.get_graph(endpt)
    A = ShortestPath(G, 100.0)

    shortest_path, best_path = A.get_shortest_path(startpt, endpt, x, elev_type="maximize", log=False)
    assert best_path[1] <= (1 + x / 100.0) * shortest_path[1]
    assert best_path[2] >= shortest_path[2]

    shortest_path, best_path = A.get_shortest_path(startpt, endpt, x, elev_type="minimize", log=False)
    assert best_path[1] <= (1 + x / 100.0) * shortest_path[1]
    assert best_path[2] <= shortest_path[2]

@Test("")
def test_get_json(location):
    print("Testing get_json method in requesthandler.py")

    json = get_json(location)
    assert isinstance(json, dict)
    assert all(k in ["properties", "type", "geometry"] for k in json.keys())

@Test("")
def test_get_data(start, end, thres = 100, elevFlag = "maximize"):
    print("Testing get_data method in requesthandler.py")

    d = get_data(start, end, thres, elevFlag, log=False)
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(start)
    locate = location.address.split(',')

    len_location = len(locate)

    start_loc = locate[0] + ',' + locate[1] + ',' + locate[2] + ',' + locate[len_location-5] + ',' + locate[len_location-3] + ', USA - ' + locate[len_location-2]

    location = locator.reverse(end)
    locate = location.address.split(',')
    len_location = len(locate)

    end_loc = locate[0] + ',' + locate[1] + ',' + locate[2] + ',' + locate[len_location-5] + ',' + locate[len_location-3] + ', USA - ' + locate[len_location-2]

    assert isinstance(d, dict)
    assert start_loc == d["start"]
    assert end_loc == d["end"]

@Test("")
def test_check_nodes(A):
    print("Testing check_nodes method in algorithms.py")
    assert A.check_nodes() == False

@Test("")
def test_resetBestPath(G):
    print("Testing resetBestPath in shortestPath.py")

    S = ShortestPath(G, 100.0,elev_type = "maximize")
    S.resetBestPath()
    assert S.optimal_path == [[], 0.0, float('-inf'), float('-inf'), "empty"]

    S = ShortestPath(G, 100.0, elev_type="minimize")
    S.resetBestPath()
    assert S.optimal_path == [[], 0.0, float('inf'), float('-inf'), "empty"]

@Test("")
def test_get_coordinates():
    print("Testing get_coordinates method in requesthandler.py")

    location = "UMass, Amherst, Massachusetts, USA"
    output = get_coordinates(location)
    assert output == (42.3869382, -72.52991477067445)

@Test("")
def test_get_address(coordinates):
    print("Testing get_address method in requesthandler.py")
    assert get_address(coordinates) == "East Hadley Road, Mill Valley, Amherst, Massachusetts, USA -  01004"


if __name__ == "__main__":
    start, end = (42.350541, -72.528715), (42.350541, -72.528715)

    G = nx.Graph()
    # Create toy graph with nodes 0-5
    [G.add_node(i, elevation=0.0) for i in range(5)]
    edgeList = [(0, 1, 3.0), (1, 2, 3.0), (0, 3, 1.414), (3, 4, 4.0), (4, 2, 1.313)]
    G.add_weighted_edges_from(edgeList)
    elev = [0.0, 0.0, 1.0, 3.0, 4.0]

    for i, e in enumerate(elev):
        G.nodes[i]["elevation"] = e

    A = Algorithms(G, shortest_dist=0.0)
    S = ShortestPath(G, 100.0)

    # Tests #####
    # test_get_graph(end)
    test_check_nodes(A)
    test_get_route(A)
    test_get_edge_weight(A)
    test_get_path_weight(A)
    # test_get_shortest_path(start, end)
    test_get_json(start)
    # test_get_data(start, end)
    test_resetBestPath(G)
    test_get_coordinates()
    test_get_address(start)
