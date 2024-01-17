#Import libraries
import random

#Import classes
from code.classes.load import Load
from code.classes.station import Station


class Random(self):

    def __init__(self, level, max_trajectory: int, timeframe: int):
        #import the station objects
        self.data = Load(level).objects
        self.max_trajectory = max_trajectory
        self.timeframe = timeframe

    def random(self) -> Any:
        for(i in self.max_trajectory):
            i += 1
            station = random_station(data)
            trajectory = [station]
            while True:
                neighbour = random_connection(data, station)
                total_time += station.get_distance(neighbour)
                if total_time > self.timeframe:
                    break
                trajectory.append(neighbour)
                station = neighbour

    def random_station(data):
        """
        find a random station for the purpose of a starting point

        post: returns a random station
        """
        random_station = random.choice(list(self.data.keys()))
        return random_station

    def random_connection(data, )
    

        



