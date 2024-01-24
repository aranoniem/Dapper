from typing import Any

class Station:
    
    def __init__(self, id, name, latitude, longitude) -> None:
        """
        Initialize a station as an object with an id, coordinates and a name

        post: Initialized station object and empty list of connections
        """
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connections = {}

    def add_connection(self, connection, distance) -> None:
        """
        Add connection to station object

        post: Initialized station object and empty list of connections
        """
        self.connections[connection] = distance

    def get_connections(self) -> list:
        """
        Get distance to a specific destination station

        pre: Name of the destination station
        post: Distance to the specified destination in minutes
        """
        
        return list(self.connections.keys())

    def get_distance(self, arrival_station) -> Any:
        """
        Get distance to a specific destination station

        pre: Name of the destination station
        post: Distance to the specified destination in minutes
        """
        return self.connections.get(arrival_station)
    
    def __str__(self):
        return f"{self.name}"
