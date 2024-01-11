from typing import Any

class Trajectory:
    
    def __init__(self, departure_station: str, arrival_station: str, distance: Any) -> None:
        """
        Initialises trajectories between intercity stations
        
        post: sets up variables to store information about the stations and their
        connections and sets up dictionary to store distance between connecting stations
        """

        self.departure_station: str = departure_station
        self.arrival_station: str = arrival_station
        self.distance: Any = distance #TODO typehint verbeteren (float, of int?)
        self.trajectories = {}

    def add_trajectory(self, distance: Any, arrival_station: str):
        """
        TODO
        """
        self.trajectories[distance] = arrival_station

    def has_trajectory(self, departure_station: Any) -> bool:
        """
        TODO
        """
        return departure_station in self.trajectories
    
    def get_trajectory(self, departure_station: Any) -> Any:
        """
        TODO
        """
        if self.has_trajectory:
            return self.trajectories[departure_station]
        else:
            return None
        