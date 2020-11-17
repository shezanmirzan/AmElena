import sys
import osmnx as ox
import networkx as nx
import pickle as p
import geopy
from geopy.geocoders import Nominatim

from src.server.abstraction import *
from src.server.algorithms import *
from src.server.control import get_geojson, get_data, get_coordinates

def Test(value = ""):
    def temp(function):
        def condition(*args, **kwargs):
            try:
                function(*args,**kwargs)
                print("Passed :)" ) # if a condition passes
                print()
            except Exception as error:
                print(error)
                print("Failed :(") # if a condition failed
                print()
        return condition
    return temp

@Test("")
def test_get_graph(end):
    print("# Testing the get_graph method in abstraction.py")

    loader = Graph_Loader()
    G = loader.get_graph(end)
    assert isinstance(G, nx.classes.multidigraph.MultiDiGraph)

@Test("")
def test_get_route(A):
    print("# Testing get_route method in algorithms.py")

    c = A.get_route({0 : 1, 1 : 2, 2 : -1}, 0)
    assert isinstance(c, list)
    assert c == [2, 1, 0]
