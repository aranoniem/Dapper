# Import libraries
from typing import Any
import copy

#TODO, import random.choice only instead of the whole random module
import random

# Import classes
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

        # Initialise a self for other functions to use the variable
        self.level = level

        # Initialise stack for algorithm
        self.stack = []
        self.trajectories_stack = []

        # Get the starting station
        #FINAL: random_station = self.random_station()
        # FOR TESTING PURPOSES: TODO, CHANGE THIS BACK TO RANDOM
        self.random_station = 'Amsterdam Sloterdijk'

        # Add starting station to stack
        self.stack.append(self.random_station)

        # Add starting station to visited stations
        self.visited_stations = [self.random_station]

    def random_station(self): 
        """
        find a random station for the purpose of a starting point

        pre: enter the data that a random station is picked from
        post: returns a random station
        """
        random_station = random.choice(list(self.data))
        return random_station

    def get_next_station(self):
        print(f'L53; de totale stack:', self.stack, '\n')
        return self.stack.pop()

    def get_last_station(self, stack_station):
        """ Get last station from given trajectory"""
        return stack_station[-1]

    def generate_children(self, stack_station):
        #TEST
        print(f'Stack_station:', stack_station, '\n')

        # Check if given variable is one station or a list of multiple
        if isinstance(stack_station, list):
            new_station = copy.deepcopy(stack_station)
            self.trajectories_stack.append(new_station)
            _station = self.get_last_station(stack_station)
        else:
            _station = stack_station

        #TEST
        print(f'Gekozen station van stack_station', _station)

        # Get connections for the current station
        stack_connections = self.data[_station].get_connections()

        # Filter out the stations that have already been visited
        unvisited_neighbours = [n for n in stack_connections if n not in self.visited_stations]

        print("toegevoegd aan stack:")
        # Add each unvisited connection to their own trajectory
        for connection in unvisited_neighbours:

            # Initialise a list for creation of new trajectory
            children = []

            # Check if given variable is one station or a list of multiple and add to new trajectory
            if isinstance(stack_station, list):
                for item in stack_station:
                    children.append(item)
            else:
                children.append(stack_station)
            # Add new connection to trajectory
            children.append(connection)
            
            # Add station to visited
            self.visited_stations.append(connection)

            # Add trajectory to stack
            self.stack.append(children)
            
            #TEST
            print(children)

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

        # runnen zodat elke connectie van start station wordt gerund. dus eigenlijk moet depth 
        # gelijk zijn aan aantal connecties start station +1 (+1 ivm eerst connecties 
        # van startstation erin zetten, vervolgens de connecties zelfe.)
        #starting_station_connections = self.data[self.random_station].get_connections()
        #print(len(starting_station_connections))
        #depth = len(starting_station_connections)
        depth = 4
        i = 0
        # Repeat until the desired number of trajectories is reached  or stack is empty (empty list == false)
        while self.stack and i < depth:

            # Get top of the stack
            stack_station = self.get_next_station()
            print("Running stack station:", stack_station)
            
            # Choose next connection
            self.generate_children(stack_station)

            print('Eind van generate children gerund, iteratie:', i, '\n')
            i += 1

        for item in self.stack:
            stack = self.trajectories_stack.append(item)
        return stack

    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a railnetwork from one station as the starting point and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a railnetwork (list: [list]) and their quality score
        """
        # Run the depth-first search to generate trajectories
        result = self.run(timeframe)
        print('L.135, result stack =', result, '\n')
        print(f'L.164, result trajectories stack = {self.trajectories_stack}')
        print(f'visited stations: = {self.visited_stations}')
        #for _ in range(max_trajectory):
            # Check if results is not None (no trajectory found)
            #if result is None:
            #    continue # Try again with a new random starting point
            #print(f'L.135, result = {result}')

        for i in range(max_trajectory):
            pass

