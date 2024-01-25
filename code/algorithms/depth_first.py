# Import libraries
from typing import Any
import copy
from random import choice #BUG? veranderd maar werking nog niet gecheckt

# Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score
from code.classes.trajectory import Trajectory

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
        post: a stack with one station, an empty stack of trajectories, a is_timeframe 
        and a list of visited stations with one station
        """
        # Get the station data and their connections
        self.data = Load(level).objects

        # Initialise a self for other functions to use the variable
        # TODO check of deze weg kan (lijkt er wel op)
        self.level = level

        # Initialise stack for algorithm to use
        self.stack = []

        # Initialise list to store succesful trajectories
        self.trajectories_stack = []

        # Initialise boolean for time constraint
        self.is_timeframe = False

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
        Find a random station for the purpose of a starting point

        pre: data that a random station is picked from
        post: returns one station
        """
        random_station = choice(list(self.data))
        return random_station

    def get_next_trajectory(self):
        """
        Get the trajectory at the top of the stack
        
        pre: the stack to get information from
        post: returns a trajectory in the form of a list
        """
        print(f'L53; de totale stack:', self.stack, '\n')
        return self.stack.pop()

    def get_last_station(self, stack_trajectory):
        """ Get last station from given trajectory
        
        pre: trajectory in the form of a list
        post: returns one station
        """
        return stack_trajectory[-1]

    def generate_children(self, stack_trajectory, timeframe):
        """
        Creates new trajectories based on the passed trajectory. Copies the passed
        trajectory and adds one connection to the last station until connections run
        out.

        pre: one trajectory in the form of a list
        post: new trajectories have been created. Timeconstraint is checked before
        new trajectories are added to succesful trajectories.
        """
        #TEST
        print(f'Stack_trajectory:', stack_trajectory, '\n')

        # Check if given trajectory is one station or a list of multiple. Get last station
        if isinstance(stack_trajectory, list):
            new_station = copy.deepcopy(stack_trajectory)
            self.trajectories_stack.append(new_station)
            _station = self.get_last_station(stack_trajectory)
        else:
            _station = stack_trajectory

        #TEST
        print(f'Gekozen station van stack_trajectory', _station)

        # Get all connections for the current station
        stack_connections = self.data[_station].get_connections()

        # Filter out the stations that have already been visited
        unvisited_neighbours = [n for n in stack_connections if n not in self.visited_stations]

        print("toegevoegd aan stack:")
        # Add each unvisited connection to their own trajectory
        for connection in unvisited_neighbours:

            # Initialise a list for creation of new trajectory
            children = []

            # Check if given trajectory is one station or a list of multiple and copy to new trajectory
            if isinstance(stack_trajectory, list):
                for item in stack_trajectory:
                    children.append(item)
            else:
                children.append(stack_trajectory)

            # Add the station/connection to new trajectory
            children.append(connection)
            
            # Add station/connection to visited
            self.visited_stations.append(connection)

            # Add trajectory to Trajectory class
            self.add_to_trajectory_class(children)

            # Check if trajectory is under maximum time
            if self.check_time(timeframe):

                # Add trajectory to stack for algorithm to use for next run
                self.stack.append(children)
            
            #TEST
            print(children, self.archive.get_time())

    def add_to_trajectory_class(self, children) -> None:
        """
        Add trajectory to Trajectory class and calculate its duration

        pre: trajectory (list of stations)
        post: trajectory is added to Trajectory class and duration is set
        """
        self.archive = Trajectory(children, self.data)
        self.archive.calc_time()
    
    def check_time(self, timeframe: int) -> bool:
        """
        Check if time of trajectory is under timelimit
        
        pre: timeframe
        post: boolean if time is under timelimit
        """
        # Check if duration of trajectory is under timelimit
        if self.archive.get_time() > timeframe:
            # Trajectory is over timelimit, tell algorithm
            self.set_timeframe_passed()
            return False
        return True

    def set_timeframe_passed(self):
        """ 
        Sets variable to True if timelimit has been passed during generating trajectories
        """
        self.is_timeframe = True

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

        # Repeat until the desired number of trajectories is reached  or stack is empty (empty list == false)
        # TESTEN: idee 1: blijven runnen tot stack leeg is, maar kan tot grote statespace leiden wellicht bij nationale set?
        # idee 2: timeconstraint, maar testen of het dan niet stopt zodra 1 traject de 120 minuten heeft bereikt. Willen namelijk
        # álle trajecten hebben die 120 minuten hebben.
        while self.stack and not self.is_timeframe: #self.time_last_trajectory() < timeframe:

            # Get top of the stack
            stack_trajectory = self.get_next_trajectory()
            print("Running stack trajectory:", stack_trajectory)
            
            # Choose next connection
            self.generate_children(stack_trajectory, timeframe)

            print(f'tijdlimiet overschreden?:', self.is_timeframe)

            print('Eind van generate children gerund, \n')

        for item in self.stack:
            stack = self.trajectories_stack.append(item)
        return self.trajectories_stack

    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a railnetwork from one station as the starting point and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a railnetwork (list: [list]) and their quality score
        """
        # Run the depth-first search to generate trajectories from one starting station
        result = self.run(timeframe)

        # TEST
        print(f'L.164, result trajectories stack = {result}')

        for i in range(max_trajectory):
            pass

# wat je wil is dat het stopt met uitvoeren zodra de tijd overschreden wordt, maar je wilt ook dat die overschreden trajecten niet in de lijst terechtkomen
