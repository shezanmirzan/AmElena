from src.server.constants import *
from src.server.shortestPath import ShortestPath
from src.server.graphLoader import Graph_Loader

import json
import numpy as np
from flask import Flask, request, render_template
from geopy.geocoders import Nominatim

ACCESS_KEY = API_KEY
init = False
G, M, algorithms = None, None, None

app = Flask(__name__, static_url_path='', static_folder="../client/static", template_folder="../client/templates")
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

def get_coordinates(location_name):
    """
    Gets latitude and longitude given the address.
    :param location_name: (str) Address in the format "UMass, Amherst, Massachusetts, USA"
    :return: (tuple) returns (latitude,longitude) in form of a tuple
    """
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(location_name)
    return ((location.latitude),(location.longitude))

def get_address(coordinates):
    """
    Gets address given the latitude and longitude.
    :param coordinates: (tuple) gets a tuple of (latitude,longitude)
    :return: (str) complete address of the provided coordinates
    """
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(coordinates)
    locate = location.address.split(',')
    len_location = len(locate)
    address = locate[0] + ',' + locate[1] + ',' + locate[len_location - 5] + ',' + locate[len_location - 3] + ', USA - ' + locate[len_location - 2]
    return address

def get_json(coordinates):
    """
    Json file for updating the data sent to UI
    :param coordinates: (tuple) tuple of latitude and longitude
    :return: (file) Json file
    """
    json = {}
    json["properties"], json["geometry"] = {}, {}
    json["type"], json["geometry"]["type"] = "Feature", "LineString"
    json["geometry"]["coordinates"] = coordinates
    return json

def update_data(sPath = None, ePath = None, start= None, end= None, null_data = False):
    """
    Helper function for the get_data function  to update data.
    :param sPath: (obj) shortest path object
    :param ePath: (obj) shortest path with elevation considered as per user updates
    :param start: (tuple) coordinates of the starting point
    :param end: (tuple) coordinates of the ending point
    :param null_data: (boolean) flag for indicating no shortest path found
    :return: (dict) data to update the UI
    """
    if null_data:
        data = {"elevation_route": [], "shortest_route": []}
        data["shortDist"], data["gainShort"], data["dropShort"]= 0, 0, 0
        data["elenavDist"], data["gainElenav"], data["dropElenav"] = 0, 0,0
        data["popup_flag"] = 0
        return data

    data = {"elevation_route": get_json(ePath[0]), "shortest_route": get_json(sPath[0])}
    data["shortDist"],  data["gainShort"], data["dropShort"]= sPath[1], sPath[2], sPath[3]
    data["start"], data["end"] = get_address(start), get_address(end)
    data["elenavDist"], data["gainElenav"], data["dropElenav"] = ePath[1], ePath[2], ePath[3]
    return data



def get_data(coord_start, coord_end, thres, elevFlag, log=True):
    """
    Get data for plotting the route using start and end coordinates of the place.
    :param coord_start: (tuple) (Latitude, Longitude) of the starting point
    :param coord_end: (tuple) (Latitude, Longitude) of the end point
    :param thres: (float)
    :param elevFlag: (str)
    :param log: (boolean)
    :return:
    """

    global init, G, M, shortestPathObj

    if log:
        print("Start Address: ", get_address(coord_start))
        print("End Address: ", get_address(coord_end))
        print("Percent of Total path: ", thres)
        print("Elevation: ", elevFlag)

    if not init:
        graph_loader = Graph_Loader()
        G = graph_loader.get_graph(coord_end)
        shortestPathObj = ShortestPath(G, x=thres, elev_type=elevFlag)
        init = True

    shortestPath, elevPath = shortestPathObj.get_shortest_path(coord_start, coord_end, thres, elev_type=elevFlag, log=log)

    if shortestPath is None and elevPath is None:
        data = update_data(True)
        return data

    data = update_data(shortestPath, elevPath, coord_start, coord_end, False)

    if len(elevPath[0]) == 0:
        data["popup_flag"] = 1
    else:
        data["popup_flag"] = 2
    return data

@app.route('/client')
def client():
    return render_template(
        'client.html',
        ACCESS_KEY=ACCESS_KEY
    )

@app.route('/route', methods=['POST'])
def get_route():
    data = request.get_json(force=True)
    # data will be following format: {'start_location': 'Hello', 'x': '0', 'end_location': 'World', 'min_max': 'minimize'}
    route_data = get_data((data['start_location']['lat'], data['start_location']['lng']),(data['end_location']['lat'], data['end_location']['lng']), data['x'], data['min_max'])
    return json.dumps(route_data)

@app.route('/route_address', methods=['POST'])
def get_routes_via_address():
    data = request.get_json(force=True)
    print(data['start_address'])
    print(data['end_address'])
    print(data)
    # data will be following format: {'start_address': 'Hello', 'x': '0', 'end_address': 'World', 'min_max': 'minimize'}
    route_data = get_data(get_coordinates(data['start_address']), get_coordinates(data['end_address']), np.float(data['x']),data['min_max'])
    return json.dumps(route_data)