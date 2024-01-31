# Import libraries
from typing import Any, List, Tuple, Set

# Import classes
from code.classes.load import Load
from code.classes.score import Score

# Import functions
from code.functions.elements import get_random_station


class Greedy_search:
    """
    Creates a railnetwork from random stations with the shortest time
    between stations as the first chosen connections, up until a time
    maximum is reached
    """
    def __init__(self, level):
        """
        Initialse variables needed for algorithm and load all data

        pre: file name for data loading
        post: loads (the connections between) stations into memory,
        initializes a trajectories list of found trajectories and a
        time counter.
        """
        self.level = level

        # Load data into memory
        self.connections = Load(level).objects

        # Counter for the score calculation
        self.total_time_for_trajectories = 0

        # List to keep track of found trajectories in railnetwork
        self.trajectories = []

    def solve(self, max_trajectories, timeframe) -> Tuple:
        """
        Generates (max_trajectories) number of trajectories and adds it
        to the list of trajectories.

        pre: amount of trajectories, amount of time for one trajectory
        post: qualityscore (K) and all trajectories (lists in a list)
        """
        # Iterate over number of allowed trajectories
        for i in range(max_trajectories):

            # Add a new trajectory to railnetwork
            trajectory = self.generate_greedy_trajectory(timeframe)
            self.trajectories.append(trajectory)
            self.calculate_time_trajectory(trajectory)

        # Calculate qualityscore of railnetwork
        score = Score(self.level, self.trajectories, self.total_time_for_trajectories)
        return (float(score.K), self.trajectories)

    def generate_greedy_trajectory(self, timeframe) -> List[str]:
        """
        Creates a new trajectory from a random starting station within
        the timeframe. Trajectory does not have the same connection twice.

        pre: maximum amount of time trajectory may be
        post: returns a trajectory without duplicates
        """
        # Get starting station and add to trajectory
        current_station = get_random_station(self.connections)
        trajectory = [current_station]

        # Keep track of time
        total_time = 0
        visited_stations: Set[str] = set()

        while total_time <= timeframe:
            next_station = self.choose_next_station(current_station, visited_stations)

            # If a dead end is reached
            if next_station is None:
                break

            connection_distance = self.connections[current_station].get_distance(next_station)

            if total_time + connection_distance <= timeframe:
                trajectory.append(next_station)
                total_time += connection_distance
                visited_stations.add(current_station)
                current_station = next_station
            else:
                break

        return trajectory

    def choose_next_station(self, current_station, visited_stations) -> Any:
        """
        Adds a new station to the trajectory if it's the closest
        neighbor and the station was not visited previously.

        pre: one stations and a list of stations
        post: return
        """
        # Retrieves stations that are connected to current station
        connections_list = self.connections[current_station].get_connections()

        # Create a list of connections to current station that have not
        # yet been visited
        unvisited_neighbors = [neighbor for neighbor in connections_list if neighbor not in visited_stations]

        # If a dead end is reached
        if not unvisited_neighbors:
            return None

        # Return the closest univisited station to the current station
        return min(unvisited_neighbors, key=lambda x: self.connections[current_station].get_distance(x))

    def calculate_time_trajectory(self, trajectory) -> None:
        """
        Calculates total amount of time of the trajectory

        pre: list of connected stations
        """
        self.total_time_for_trajectories += sum(self.time_between_stations(trajectory))

    def time_between_stations(self, trajectory) -> List[int]:
        """
        Returns a list of the distances between stations.

        pre: list of connected stations
        post: list of times between stations
        """
        return [self.connections[trajectory[i]].get_distance(trajectory[i + 1]) for i in range(len(trajectory) - 1)]
