# Import libraries
import random
from typing import List, Tuple

# Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

# Import functions
from code.functions.elements import get_random_station


class Totally_random():

    """
    create a solution based on making random trajectories
    and calculate their quality

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

    def solve(self, max_trajectory: int, timeframe: int) -> Tuple[float, List[List[str]]]:
        """
        Create a random railnetwork and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a random railnetwork and their quality score
        """
        total_time, railnetwork = self.generate_railnetwork(max_trajectory,
                                                            timeframe)

        # Show the trajectory of the random algorithm
        quality_score = Score(self.level, railnetwork, total_time).K

        return quality_score, railnetwork

    def generate_railnetwork(self, max_trajectory: int,
                             timeframe: int) -> Tuple[float, List[List[str]]]:
        """
        generate a railnetwork based on randomly generated trajectories

        pre: a maximum of trajectories and a timeframe for the trajectories
        post: return a randomly generated railnetwork
        """
        railnetwork = []
        total_time = 0
        # Choose a random amount of trajectories between 1 and the chosen max
        self.trajectory_count = random.randint(1, max_trajectory)

        # Create trajectories for the amount chosen
        for i in range(self.trajectory_count):
            duration, trajectory = self.generate_trajectory(timeframe)

            # Add trajectory to railnetwork
            railnetwork.append(trajectory)

            # Add time to total time of railnetwork
            total_time += duration

        return total_time, railnetwork

    def generate_trajectory(self, timeframe: int) -> Tuple[int, List[str]]:
        """
        Generate a random trajectory based on a random starting station
        and random neighbours

        pre: give a timeframe of which the duration can't exceed
        post: return a random trajectory
        """

        # Initialize
        station = get_random_station(self.data)
        trajectory = [station]
        visited_stations = {station}
        duration = 0

        while True:
            # Choose a random neighbour
            neighbours = self.data[station].get_connections()
            random_neighbour = random.choice(neighbours)

            # Stop making connections when timeframe is reached
            distance = self.data[station].get_distance(random_neighbour)
            duration += distance
            if duration > timeframe:
                duration = duration - distance
                break

            # Add station to trajectory
            trajectory.append(random_neighbour)

            # Remember stations that are visited in trajectory
            visited_stations.add(random_neighbour)
            station = random_neighbour

        return duration, trajectory
