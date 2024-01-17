#import libraries
import pandas as pd

# import classes
from classes.station import Station

class Load():

    def __init__(self, level) -> None:
        """
        Load stations, connections between stations, and coordinates of stations.

        Pre: part of filename of railwaydata is specified.
        Post: all data (stations, connections, coordinates) from csv is loaded into memory.
        """
        self.objects = {}
        self.bitgraph = {}
        self.tracks = set() 

        self.load_stations(f'data/Stations{level}.csv')
        self.load_connections(f'data/Connecties{level}.csv')
        self.load_tracks(f'data/Connecties{level}.csv')
        

    def load_stations(self, filename) -> dict:
        """
        Load stations and its coordinates.

        Pre: filename of railway data is specified.
        Post: stations, longitude, latitude are loaded into memory.
        """
        # Read the CSV file
        df = pd.read_csv(filename)

        # Keep track of iterations for loop for id per station
        id = 0

        # Iterate through the rows
        for index, row in df.iterrows():
            _station = row['station']
            latitude = row['y']
            longitude = row['x']

            self.objects[_station] = Station(id, _station, latitude, longitude)
            self.bitgraph[_station] = {}  # Initialize nested dictionary for the station
            id += 1

        #test print(self.objects)

        return self.objects

    def load_connections(self, filename) -> dict:
        """
        Load connections into memory

        Pre: filename of railway data is specified
        Post: stations and distances are all loaded into memory and connected
        """
  
        # Read the CSV file
        df = pd.read_csv(filename)

        # Iterate through the rows
        for index, row in df.iterrows():
            departure_station = row['station1']
            arrival_station = row['station2']
            distance = row['distance']

            # Connecting both stations to each other, with the distance between them (tuples)
            self.objects[departure_station].add_connection(arrival_station, distance)
            self.objects[arrival_station].add_connection(departure_station, distance)
            #TEST print(self.objects[departure_station])

        return self.objects

    def load_tracks(self, filename) -> dict:
        """Calculate number of used tracks"""
        # Read the CSV file

        df = pd.read_csv(filename)

        # Iterate through the rows
        for index, row in df.iterrows():
            departure_station = row['station1']
            arrival_station = row['station2']
            distance = row['distance']

            # Sort the stations alphabetically
            sorted_stations = (departure_station, arrival_station)
            sorted_stations = tuple(sorted(sorted_stations))

            # Connecting both stations to each other, with the distance between them (tuples)
            self.tracks.add(sorted_stations)
            #TEST STATEMENT print(self.tracks[sorted_stations[0]], sorted_stations[0])

        return self.tracks

            
