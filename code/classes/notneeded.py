""""
from typing import Any

#this file is not needed anymore but kept just in case

class Connection:
    """
    #Contains all the connecting stations and their distances to the departure station defined in the Station 
"""
    
    def __init__(self, arrival_station: str, distance: Any) -> None:
        """
        #Initialises connections between intercity stations
        
        #post: sets up variables to store information about the stations and their
        #connections and sets up dictionary to store distance between connecting stations
"""
        self.arrival_station: str = arrival_station
        self.distance: Any = distance #TODO specify typehint if possible
        self.connections = []

    # TODO we need to check wheter we use this or the update, or both
    def add_connection(self, arrival_station: str, distance: Any):
        """
        #adds destination and distance from departure station
"""
        #if arrival_station in self.connections:
            #raise Exception("Add_connection fout, Arrival station already in dict")

        self.connections.append(arrival_station, distance)

    # TODO we need to check wheter we use this or the update, or both
    def update_connection(self, arrival_station: str, distance: Any):
        """
        #updates the dictionary in case of the departure station already being 
        #present in the connection dictionary
"""
        self.connection_update[arrival_station] = distance
        self.connections.update(self.connection_update)
    
    def get_connection(self) -> Any:
        """
        #Returns all stations connected to primary station
"""
        #TEST STATEMENT print(self.connections)
        return self.connections

    # BUG: With one statement the output has one space too many after the distance
    def __str__(self):
        """#post: returns description and list"""
        #items_str = ", ".join(f'{station}: {distance}' for station, distance in self.connections.items())
        #return f'({self.arrival_station}: {self.distance}, {items_str})'


#"""