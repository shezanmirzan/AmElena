# AmElena : Elevation Based Navigation System for Amherst, MA, USA
We plan to develop a system EleNa, to tell the user a route that maximizes/minimizes the elevation within the user specified limit of the percentage of shortest path, given the start and end locations in the town of Amherst.

# Set-up

### Installing OSMnx, NetworkX and Geopy
with pip:
```
pip install osmnx, networkx, geopy
```
or simply run ```requirements.txt```


# Running and testing the application

### Using the application
- Run ```start.sh``` to set-up the flask application.
- Head over to `http://127.0.0.1:5000/client` on your preferred browser to use the web interface.

Please refer to the video presentation for a simple demo involving the project know-hows and run strategies. 

### Testing 
- To run the tests run `python test/test.py` from the home directory.
- Manual UI testing available in ```UI_tests.pdf```

# Learnings

### Design Principles
- Open/Closed principle : Used ```config.py``` to set configurable parameters eg. API key, map center etc.
### Design Patterns
- Factory pattern : to set distance metric ie either Haversine(default), Manhattan or Eucliedean
- Strategy pattern : to choose different algorithms i.e Djisktra or A-star algorithm



# Contributors

- `Ankita Naik`
- `Apurva Swarnakar`
- `Prabodh Shetty`
- `Saurabh Kumar Shashidhar`
- `Shezan Rohinton Mirzan`