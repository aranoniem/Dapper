from typing import Any

class Trajectory:
    
    def __init__(self, arrival_station: str, distance: Any) -> None:
        """
        Initialises trajectories between intercity stations
        
        post: sets up variables to store information about the stations and their
        connections and sets up dictionary to store distance between connecting stations
        """
        self.arrival_station: str = arrival_station
        self.distance: Any = distance #TODO typehint verbeteren (float, of int?)
        self.trajectories = {}

    def add_trajectory(self, arrival_station: str, distance: Any):
        """
        adds destination and distance from departure station
        """
        self.trajectories[arrival_station] = distance

    def has_trajectory(self, arrival_station: Any) -> bool:
        """
        TODO
        """
        return arrival_station in self.trajectories
    
    def get_trajectory(self, arrival_station: str) -> Any:
        """
        TODO
        """
        if self.has_trajectory:
            return self.trajectories[arrival_station]
        else:
            return None




        