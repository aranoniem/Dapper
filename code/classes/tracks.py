#import libraries
import pandas as pd

class Tracks:
    """Keeps a record of tracks within a trajectory"""

    def __init__(self, departure_station, arrival_station):
        """
        Establish simple dictionary of available tracks

        pre: part of filename of the data, arrival and departure
        post: returns a dictionary with departure stations (station1) as keys
        and arrival stations as values (station2)
        """
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.tracks = {}
        self.trajectories = []

    def add_track(self, departure_station, arrival_station) -> None:
        """Add track to dictionary"""
        self.tracks[departure_station] = arrival_station

