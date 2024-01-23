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
        print(f'L53; de totale stack:',self.stack, '\n')
        return self.stack.pop()

    def generate_children(self, stack_station):
        print(f'L57 station:', stack_station, '\n')
        if isinstance(stack_station, list):
            new_station = copy.deepcopy(stack_station)
            self.stack.append(new_station)
            _station = stack_station[-1] #!!!! let op met breadth first. verdeel get_next_station in twee.
        else:
            _station = stack_station

        print(f'L64', _station)

        # Get connections for the current station
        stack_connections = self.data[_station].get_connections()

        for connection in stack_connections:
            children = []
            #new_station = copy.deepcopy(stack_station)
            if isinstance(stack_station, list):
                for item in stack_station:
                    children.append(item)
            else:
                children.append(stack_station)
            children.append(connection)
            print(f'L74', children)
            self.stack.append(children)

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

        depth = 2
        i = 0
        # Repeat until the desired number of trajectories is reached  or stack is empty (empty list == false)
        while self.stack and i < depth:

            # Get top of the stack
            stack_station = self.get_next_station()
            print("L98, Current stack station:", stack_station)
            # Choose next connection

            self.generate_children(stack_station)
            print('L106, is door generate children gerund \n')
            i += 1

        stack = self.stack
        return stack

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
            print(f'L.135, result = {result}')

