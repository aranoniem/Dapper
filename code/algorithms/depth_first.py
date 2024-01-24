# Import libraries
from typing import Any
import copy
import random

# Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

# Import functions
from .semi_random import Random

class DepthFirst():
    """
    Create a solution based on children of a random station

    pre: choose a level, a maximum amount of trajectories and a timeframe
    post: return the railnetwork of the outcome and a quality score
    """
    def __init__(self, level: str):
        """
        Initalize the algorithm and load all station objects

        pre: use the Load class
        post: a stack with one station is initialised
        """
        # Get the station data and their connections
        self.data = Load(level).objects

        self.level = level

        # Initialise stack for algorithm
        self.stack = []

        # Get the starting station
        random_station = self.random_station()

        # Add starting station to stack
        self.stack.append(random_station)

    def random_station(self): 
        """
        find a random station for the purpose of a starting point

        pre: enter the data that a random station is picked from
        post: returns a random station
        """
        random_station = random.choice(list(self.data.keys()))
        return random_station

    def get_next_station(self):
        print(f'(next_station) de totale stack:',self.stack, '\n')
        return self.stack.pop()

    def generate_children(self, stack_station, stack_connections):
        print(f'(generate), station:', stack_station, '\n')
        children = []
        for connection in stack_connections:
            new_station = [copy.deepcopy(stack_station)]
            new_station.append(connection)
            self.stack.append(new_station)

    def calculate_time(trajectory):
        """
        Calculate the total time for a given trajectory
        """
        total_time = 0
        for i in range(len(trajectory) - 1):
            connection_time = self.data[trajectory[i]].get_distance(trajectory[i+1])
            total_time += connection_time
        return total_time

    def run(self, timeframe: int):
        """
        Fills the stack with the stations, with a max depth of timeframe
        """
        # Initialise a list to store trajectories
        trajectories = []

        # Repeat until the desired number of trajectories is reached  or stack is empty (empty list == false)
        while self.stack:

            # Get top of the stack
            stack_station = self.get_next_station()
            print("Current stack station:", stack_station)
            # Choose next connection
            stack_connections = self.data[stack_station].get_connections()

            # If we have (a) connection(s):
            if stack_connections:
                print(f'run, connecties:', stack_connections)
                self.generate_children(stack_station, stack_connections)
                print('is door generate children gerund \n')
            else:
                current_stack = self.stack
                print(f'current stack is {current_stack}')
                return current_stack
                # dit klopt niet denk ik, in principe is deze dus leeg. kijk naar ontwerp
                # gebruik van solve en run?? misschien stack niet lijst van lijst, maar 
                # elk traject 1 lijst en dan weer weg. check ook github

    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a railnetwork from one station as the starting point and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a railnetwork (list: [list]) and their quality score
        """
        # Initialise a list to store valid trajectories
        valid_trajectories = []
        
        for _ in range(max_trajectory):
            # Run the depth-first search to generate trajectories
            result = self.run(timeframe)

            # Check if results is not None (no trajectory found)
            if result is None:
                continue # Try again with a new random starting point
            print(f'result = {result}')
            # Calculate the total time for the entire trajectory
            total_time = calculate_time(result)
            print(f'totale tijd = {total_time}')

        # iterate over stack, calculate times and see which are under timeframe? 
        # or incorporate it into run(), and then take the longest trajectories in the stack
        # hoe ziet een stack eruit, is dit een lijst van lijsten??
