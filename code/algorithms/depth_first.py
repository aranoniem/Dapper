#Import libraries
from typing import Any

#Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

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
        random_data = Random() # TODO!! functie maken in calculations.py en die aanroepen in random algoritmes en deze
        random_station = random_data.random_station()

        # Add starting station to stack
        self.stack.append(random_station)

    def get_next_station(self):
        return self.stack.pop()

    def generate_neighbours(self, stack_station, stack_connections):
        for connection in stack_connections:
            new_station = copy.deepcopy(stack_station)
            new_station += connection
            self.stack.append(new_station)

    def run(self, timeframe: int):
        """
        Fills the stack with the stations, with a max depth of timeframe
        """
        # TODO! Integreren timeframe??

        # Repeat until stack is empty (empty list == false)
        while self.stack:
            # Get top of the stack
            stack_station = self.get_next_station()

            # Choose next connection
            stack_connections = self.data[stack_station].get_connections()

            # If we have (a) connection(s):
            if stack_connections:
                self.generate_neighbours(stack_station, stack_connection)
            else:
                self.stack = stack
                return stack

    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a railnetwork from one station as the starting point and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a railnetwork (list: [list]) and their quality score
        """
        # TODO!