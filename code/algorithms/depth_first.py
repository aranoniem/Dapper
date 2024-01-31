# Import libraries
from typing import Any
import copy

# Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score
from code.classes.trajectory import Trajectory

# Import functions
from code.functions.elements import get_random_station

class Depth_first():
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
        self.level = level

        # Initialise stack for algorithm to use
        self.stack = []

        # Initialise list to store succesful trajectories
        self.trajectories_stack = []

        # Initialise boolean for time constraint
        self.is_timeframe = False

        self.best_value = 0

        # Get the starting station
        self.random_station = get_random_station(self.data)
        # FOR TESTING PURPOSES: self.random_station = 'Utrecht Centraal'

        # Add starting station to stack
        self.stack.append(self.random_station)

        # Add starting station to visited stations
        self.visited_stations = [self.random_station]

    def get_next_trajectory(self):
        """
        Get the trajectory at the top of the stack
        
        pre: the stack to get information from
        post: returns a trajectory in the form of a list
        """
        #TEST print(f'L53; de totale stack:', self.stack, '\n')
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
        #TEST print(f'Stack_trajectory:', stack_trajectory, '\n')
        # Check if given trajectory is one station or a list of multiple. Get last station
        if isinstance(stack_trajectory, list):
            new_station = copy.deepcopy(stack_trajectory)
            self.trajectories_stack.append(new_station)
            _station = self.get_last_station(stack_trajectory)
        else:
            _station = stack_trajectory

        #TEST print(f'Gekozen station van stack_trajectory', _station)
        # Get all connections for the current station
        stack_connections = self.data[_station].get_connections()

        # Filter out the stations that have already been visited
        unvisited_neighbours = [n for n in stack_connections if n not in self.visited_stations]

        #TEST print("toegevoegd aan stack:")
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
            
            #TEST print(children, self.archive.get_time())

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

        while self.stack and not self.is_timeframe:

            # Get top of the stack
            stack_trajectory = self.get_next_trajectory()
            #TEST print("Running stack trajectory:", stack_trajectory)
            
            # Choose next connection
            self.generate_children(stack_trajectory, timeframe)

            #TEST print(f'tijdlimiet overschreden?:', self.is_timeframe)
            #TEST print('Eind van generate children gerund, \n')

        for item in self.stack:
            stack = self.trajectories_stack.append(item)
        return self.trajectories_stack

    def improve(self):
        """ TODO, optional. deletes double connections at the beginning or end of a traject"""
        pass

    def check_solution(self, railnetwork, time):
        """Checks and accepts better solutions than the current solution"""
        new_value = Score(self.level, railnetwork, time).K
        #TEST print('new_value =', new_value)
        old_value = self.best_value
        #TEST print('old_value =', old_value)

        if new_value >= old_value:
            self.best_solution = railnetwork
            self.best_value = new_value
            #TEST print(f"New best value:", self.best_value)
            return True
        return False

    def solve(self, max_trajectory: int, timeframe: int) -> float:
        """
        Create a railnetwork from one station as the starting point and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a railnetwork (list: [list]) and their quality score
        """
        # Run the depth-first search to generate trajectories from one starting station
        results = self.run(timeframe)

        # TEST print(f'L.164, result trajectories stack = {results}')

        # Set up a list to store railnetwork
        railnetwork = []

        # Iterate over trajectories
        for i in range(len(results) - 1, -1, -1):
            # Get the last trajectory in list (aka the longest) and add it to railnetwork
            last_trajectory = results[i]
            railnetwork.append(last_trajectory)

            # Calculate total time of all trajectories in railnetwork
            time = self.calc_total_time(railnetwork)

            # Check if solution is better than previous iteration
            if self.check_solution(railnetwork, time):
                railnetwork.pop()

            # Quit if maximum amount of trajectories have been reached
            if len(railnetwork) >= max_trajectory:
                break
        print(f'railnetwork:', railnetwork, 'score:', self.best_value)
        return (self.best_value, railnetwork)

    def calc_total_time(self, railnetwork):
        total_time = 0
        _time = 0

        for trajectory in railnetwork:
            self.add_to_trajectory_class(trajectory)
            _time - self.archive.get_time()
            total_time += _time
        return total_time
# depth_first max_trajectories aantal keer laten runnen en dan steeds de laatste pakken??

