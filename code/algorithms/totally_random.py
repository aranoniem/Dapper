#Import libraries
import random
from typing import Any

#Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

class Totally_random():
    """
    create a solution based on making random trajectories and calculate their quality

    pre: choose a level, a maximum amount of trajectories and a timeframe
    post: return the railnetwork of the outcome and a quality score
    """

    def __init__(self, level: str):
        """
        Initalize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """

        self.data = Load(level).objects
        self.level = level

        
    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a random railnetwork and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a random railnetwork and their quality score
        """
        railnetwork = []
        total_time = 0

        #create trajectories for the amount chosen 
        for i in range(max_trajectory):
            station = self.random_station(self.data)
            trajectory = [station]
            visited_stations = {station}
            duration = 0

            while True:
                neighbours = self.data[station].get_connections()

            
                random_neighbour = random.choice(neighbours)

                #stop making connections when timeframe is reached
                duration += self.data[station].get_distance(random_neighbour)
                if duration > timeframe:
                    break

                #add station to trajectory
                trajectory.append(random_neighbour)

                #remember stations that are visited in trajectory
                visited_stations.add(random_neighbour)
                station = random_neighbour
            
            #add trajectory to railnetwork
            railnetwork.append(trajectory)

            #add time to total time of railnetwork
            total_time += duration
            

        #show the trajectory of the random algorithm
        #print(railnetwork)
        quality_score = Score(self.level, railnetwork, timeframe)
        print(quality_score)
        #print(quality_score)
        return float(quality_score.K)
    

    def random_station(self, data: dict): 
        """
        find a random station for the purpose of a starting point

        pre: enter the data that a random station is picked from
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

        #if their are more connections, choose a random one
        if len(neighbours) > 1:
            random_index = random.randint(1, len(neighbours))
            #TEST STATEMENT print(random_index)
            random_neighbour = neighbours[random_index - 1]
            #TEST STATEMENT print(random_neighbour)
        #if there is only one connection, make that one
        else:
            random_neighbour = neighbours[0]
        return random_neighbour