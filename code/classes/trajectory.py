# Import libraries
from typing import Any

class Trajectory():

    def __init__(self, trajectory, data):
        self.trajectory = trajectory
        self.time = 0
        self.data = data # Data from stations class

    def get_time(self):
        """Returns time of trajectory"""
        return self.time
    
    def calc_time(self) -> None:
        """Calculate time of the trajectory"""
        # Make sure self.time doesn't get corrupted
        if self.time == 0:

            # Iterate over the indices of the stations
            for i in range(len(self.trajectory) - 1):

                # Get the time between two stations and add to total
                connection_time = self.data[self.trajectory[i]].get_distance(self.trajectory[i+1])
                self.time += connection_time
