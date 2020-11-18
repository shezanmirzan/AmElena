from flask import Flask, jsonify, session, g, request, url_for, flash, redirect, abort, render_template
from geopy.geocoders import Nominatim
import json
import numpy as np
from src.server.shortestPath import ShortestPath
from src.server.constants import *
from src.server.graphLoader import Graph_Loader

app = Flask(__name__, static_url_path='', static_folder="../client/static", template_folder="../client/templates")
app.config.from_object(__name__)

app.config.from_envvar('APP_CONFIG_FILE', silent=True)

ACCESS_KEY = API_KEY

init = False
G, M, algorithms = None, None, None


def get_coordinates(location_name):
    """
    Gets latitude and longitude given the address.
    :param location_name: (str) Address in the format "UMass, Amherst, Massachusetts, USA"
    :return:
    """
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(location_name)
    return ((location.latitude),(location.longitude))


def get_address(coordinates):
    """
    Gets address given the latitude and longitude.
    :param coordinates: (tuple) of (latitude,longitude)
    :return:
    """
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(coordinates)
    locate = location.address.split(',')

    len_location = len(locate)

    address = locate[0] + ',' + locate[1] + ',' + locate[2] + ',' + locate[len_location - 5] + ',' + locate[
        len_location - 3] + ', USA - ' + locate[len_location - 2]
    return address


def get_geojson(coordinates):
    geojson = {}
    geojson["properties"] = {}
    geojson["type"] = "Feature"
    geojson["geometry"] = {}
    geojson["geometry"]["type"] = "LineString"
    geojson["geometry"]["coordinates"] = coordinates
    return geojson


def get_data(coord_start, coord_end, thres, elevFlag, log=True):
    """
    Get data for plotting the route
    :param coord_start: (tuple) (Latitude, Longitude) of the starting point
    :param coord_end: (tuple) (Latitude, Longitude) of the end point
    :param thres:
    :param elevFlag:
    :param log:
    :return:
    """

    global init, G, M, shortestPathObj

    if log:
        print("Start: ", get_address(coord_start))
        print("End: ", get_address(coord_end))
        print("Percent of Total path: ", thres)
        print("Elevation: ", elevFlag)

    if not init:
        graph_loader = Graph_Loader()
        G = graph_loader.get_graph(coord_end)
        shortestPathObj = ShortestPath(G, x=thres, elev_type=elevFlag)
        init = True

    shortestPath, elevPath = shortestPathObj.get_shortest_path(coord_start, coord_end, thres, elev_type=elevFlag,
                                                               log=log)

    if shortestPath is None and elevPath is None:
        data = {"elevation_route": [], "shortest_route": []}
        data["shortDist"] = 0
        data["gainShort"] = 0
        data["dropShort"] = 0
        data["elenavDist"] = 0
        data["gainElenav"] = 0
        data["dropElenav"] = 0
        data["popup_flag"] = 0
        return data
    data = {"elevation_route": get_geojson(elevPath[0]), "shortest_route": get_geojson(shortestPath[0])}
    data["shortDist"] = shortestPath[1]
    data["gainShort"] = shortestPath[2]
    data["dropShort"] = shortestPath[3]
    data["start"] = get_address(coord_start)
    data["end"] = get_address(coord_end)
    data["elenavDist"] = elevPath[1]
    data["gainElenav"] = elevPath[2]
    data["dropElenav"] = elevPath[3]
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
    route_data = get_data((data['start_location']['lat'], data['start_location']['lng']),
                          (data['end_location']['lat'], data['end_location']['lng']), data['x'], data['min_max'])
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
