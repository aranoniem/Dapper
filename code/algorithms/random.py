#Import libraries
import random
from typing import Any

#Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

class Random():

    def __init__(self, level, max_trajectory: int, timeframe: int):
        #import the station objects
        self.data = Load(level).objects
        self.max_trajectory = max_trajectory
        self.timeframe = timeframe
        self.level = level
        self.random()
        

    def random(self) -> Any:
        railnetwork = []
        total_time = 0
        for i in range(self.max_trajectory):
            station = self.random_station(self.data)
            trajectory = [station]
            visited_stations = {station}
            duration = 0

            while True:
                neighbours = self.data[station].get_connections()

                # Filter out visited stations
                unvisited_neighbours = [n for n in neighbours if n not in visited_stations]

                if not unvisited_neighbours:
                    # If all neighbors have been visited, choose a random one
                    random_neighbour = random.choice(neighbours)
                else:
                    # Choose a random unvisited neighbor
                    random_neighbour = random.choice(unvisited_neighbours)

                duration += self.data[station].get_distance(random_neighbour)
                if duration > self.timeframe:
                    break

                trajectory.append(random_neighbour)
                visited_stations.add(random_neighbour)
                station = random_neighbour
            
            total_time += duration
            railnetwork.append(trajectory)
        #show the trajectory of the random algorithm
        print(railnetwork)
        K = Score(self.level, railnetwork, self.timeframe)
        print(K)
        return K
    

    def random_station(self, data: dict): 
        """
        find a random station for the purpose of a starting point

        post: returns a random station
        """
        random_station = random.choice(list(data.keys()))
        return random_station

    def random_connection(self, data: dict, station: str):
        """
        find a random connection for the purpose of making a trajectory

        pre: enter a departure station
        post: returns a station connected with the departure station 
        """
        neighbours = list(data[station].get_connections())

        if len(neighbours) > 1:
            random_index = random.randint(1, len(neighbours))
            #TEST STATEMENT print(random_index)
            random_neighbour = neighbours[random_index - 1]
            #TEST STATEMENT print(random_neighbour)
        else:
            random_neighbour = neighbours[0]
        return random_neighbour

    

        



