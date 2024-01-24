#Import libraries
import random
from typing import Any

#Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score
from totally_random import Totally_random

class Local_search():
    def __init__(self, level: str):
        """
        Initalize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """

        self.data = Load(level).objects
        self.level = level

    def solve(self, timeframe, max_trajectory, max_iterations):

        while iterations <= max_iterations:
            railnetwork = self.random_startnetwork(timeframe, max_trajectory)
            new_trajectory = self.random_trajectory(timeframe)
            temp_railnetwork = railnetwork
            iterations = 0

            for i in range(max_trajectory):
                temp_railnetwork[i] = new_trajectory
                temp_quality_score = Score(self.level, railnetwork, timeframe)
                if temp_quality_score > quality_score:
                    quality_score = temp_quality_score 
                    railnetwork = temp_railnetwork
                    print(railnetwork)
                    iterations = 0
                else:
                    iterations += 1
                    temp_railnetwork = railnetwork
                    print(temp_railnetwork)

        return quality_score

    def random_startnetwork(self, timeframe, max_trajectory):
        """
        Create a random railnetwork and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a random railnetwork and their quality score
        """
        railnetwork = []

        #create trajectories for the amount chosen 
        for i in range(random.randint(1, max_trajectory)):
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

        return railnetwork
    
    def random_trajectory(self, timeframe):
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

        return trajectory    

    def random_station(self, data: dict): 
        """
        find a random station for the purpose of a starting point

        pre: enter the data that a random station is picked from
        post: returns a random station
        """
        random_station = random.choice(list(data.keys()))
        return random_station        

    