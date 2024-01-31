# Import libraries
import random
from typing import Any, Tuple, List

# Import classes
from code.classes.load import Load
from code.classes.score import Score

# Import functions
from code.functions.elements import get_random_station


class Semi_random():
    """
    create a solution based on making random trajectories and calculate
    their quality
    """

    def __init__(self, level: str):
        """
        Initalize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """

        self.data = Load(level).objects
        self.level = level

    def solve(self, max_trajectory: int,
               timeframe: int) -> Tuple[float, List[List[str]]]:
        """
        Create a random railnetwork and calculate their score

        pre: choose a level, a maximum amount of trajectories and a timeframe
        post: returns a random railnetwork and their quality score
        """
        total_time, railnetwork = self.generate_railnetwork(max_trajectory,
                                                            timeframe)

        # Show the trajectory of the random algorithm
        print(railnetwork)
        quality_score = float(Score(self.level, railnetwork, total_time).K)
        # Print(quality_score)
        return quality_score, railnetwork

    def generate_railnetwork(self, max_trajectory: int, 
                             timeframe: int) -> Tuple[float, List[List[str]]]:
        """
        generate a railnetwork based on semi-randomly generated trajectories

        pre: a maximum of trajectories and a timeframe for the trajectories
        post: return a semi-randomly generated railnetwork
        """
        railnetwork = []
        total_time = 0
        # Choose a random amount of trajectories between 1
        # and the maximum amount of trajectories
        self.trajectory_count = random.randint(1, max_trajectory)

        # Create trajectories for the amount chosen
        for i in range(self.trajectory_count):
            duration, trajectory = self.generate_trajectory(timeframe)

            # Add trajectory to railnetwork
            railnetwork.append(trajectory)

            # Add time to total time of railnetwork
            total_time += duration

        return total_time, railnetwork

    def generate_trajectory(self, timeframe):
        """
        Generate a random trajectory based on a random starting station
        but unless it is not possible it will not visit the same station
        twice

        pre: give a timeframe of which the duration can't exceed
        post: return a random trajectory
        """

        station = get_random_station(self.data)
        trajectory = [station]
        visited_stations = {station}
        duration = 0

        while timeframe > duration:
            neighbours = self.data[station].get_connections()

            # Filter out visited stations
            unvisited_neighbours = [n for n in neighbours if n not in visited_stations]

            if not unvisited_neighbours:
                # If all neighbors have been visited, choose a random one
                random_neighbour = random.choice(neighbours)
            else:
                # Choose a random unvisited neighbor
                random_neighbour = random.choice(unvisited_neighbours)

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

        print(trajectory)
        return duration, trajectory
