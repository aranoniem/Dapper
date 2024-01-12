from typing import Any

class Connection:
    
    def __init__(self, arrival_station: str, distance: Any) -> None:
        """
        Initialises connections between intercity stations
        
        post: sets up variables to store information about the stations and their
        connections and sets up dictionary to store distance between connecting stations
        """
        self.arrival_station: str = arrival_station
        self.distance: Any = distance #TODO typehint verbeteren (float, of int?)
        self.connections = {}
        self.connection_update = {}

    def add_connection(self, arrival_station: str, distance: Any):
        """
        adds destination and distance from departure station
        """
        if arrival_station in self.connections:
            raise Exception("Add_connection fout, Arrival station already in dict")

        self.connections[arrival_station] = distance

    def update_connection(self, arrival_station: str, distance: Any):
        """
        updates the dictionary in case of the departure station already being 
        present in the connection dictionary
        """
        self.connection_update[arrival_station] = distance
        self.connections.update(self.connection_update)

    def has_connection(self, arrival_station: Any) -> bool:
        """
        TODO
        """
        return arrival_station in self.connections
    
    def get_connection(self, arrival_station: str) -> Any:
        """
        TODO
        """
        if self.has_connection:
            return self.connections[arrival_station]
        else:
            return None

    # BUG: bij 1 station is de output: Dordrecht: (Rotterdam Centraal: 17, ) Met een spatie teveel.
    def __str__(self):
        """post: returns description and list"""
        items_str = ", ".join(f'{station}: {distance}' for station, distance in self.connections.items())
        return f'({self.arrival_station}: {self.distance}, {items_str})'




        