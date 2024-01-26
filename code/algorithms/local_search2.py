# Import libraries
from typing import Any, List, Tuple
import random

# Import classes
from .semi_random import Semi_random # Import Semi_random class
from code.classes.score import Score

class Local_search2(Semi_random):
    def __init__(self, level: str):
        """
        Initialize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """
        super().__init__(level)  # Call the constructor of the parent class

    def solve(self, timeframe, max_trajectory, max_iterations: int):
        #initialize start of iterations
        self.iterations = 0

        # calculate quality score for the random rail network
        total_time, railnetwork = self.generate_railnetwork(max_trajectory, timeframe)
        quality_score = int(Score(self.level, railnetwork, total_time).K)

        # search for a right amount of trajectories to start with for higher solutions
        while new_quality_score != quality_score:
            # Search for better solutions when trajectories are removed
            new_quality_score, railnetwork, total_time = self.remove_trajectory(quality_score, railnetwork, total_time)


        while new_quality_score != quality_score: 
            # generate a random trajectory
            self.duration, self.new_trajectory = self.generate_trajectory(timeframe)
            # Search for better solutions when a new trajectory is added
            quality_score, railnetwork, total_time = self.add_trajectory(quality_score, railnetwork, total_time, max_trajectory)

        # when there is no change in max_iterations, the algorithm will stop
        while self.iterations <= max_iterations:

    
    def remove_trajectory(self, quality_score: int, railnetwork: List[Any], total_time: int) -> Tuple[int, List[Any], int]:
        """
        Looks for a better score when a trajectory is deleted from a rail network

        pre: a rail network with its quality score and total time is needed
        post: if a deletion leads to a better result, a trajectory is deleted
        """
        # initialize variables
        trajectory_count = len(railnetwork)
        best_deleted_score = 0

        # calculate all solutions when one trajectory is deleted
        for i in range(trajectory_count):
            temp_railnetwork = railnetwork.copy()
            deleted_time = self.calculate_time(temp_railnetwork[i])
            del temp_railnetwork[i]
            temp_quality_score = int(Score(self.level, temp_railnetwork, (total_time - deleted_time)).K)

            # search for the trajectory that will make the highest score when deleted
            if temp_quality_score > best_deleted_score:
                best_deleted_score = temp_quality_score
                best_deleted_railnetwork = temp_railnetwork
                best_deleted_time = deleted_time

        # if there is a better solution, delete the trajectory
        if best_deleted_score > quality_score:
            quality_score = best_deleted_score
            railnetwork = best_deleted_railnetwork
            total_time = total_time - best_deleted_time
            self.iterations = 0

        return quality_score, railnetwork, total_time
    
    def add_trajectory(self, quality_score: int, railnetwork: List[Any], total_time: int, max_trajectory: int) -> Tuple[int, List[Any], int]:
        """
        Looks for a better score when a trajectory is added to a rail network

        pre: a rail network with its quality score and total time is needed,
             with a randomly generated rail network
        post: if an addition leads to a better result, a trajectory is added
        """
        self.added = False

        # check if it is allowed to add a trajectory
        if len(railnetwork) < max_trajectory:
            # calculate if addition will return a higher quality score
            temp_railnetwork = railnetwork.copy()
            temp_railnetwork.append(self.new_trajectory)
            temp_total_time = total_time
            temp_total_time += self.duration
            temp_quality_score = int(Score(self.level, temp_railnetwork, temp_total_time).K)

            # if addition returns a better solution, add
            if temp_quality_score > quality_score:
                quality_score = temp_quality_score
                railnetwork = temp_railnetwork
                total_time = temp_total_time
                self.added = True
                self.iterations = 0

        return quality_score, railnetwork, total_time
    
    def calculate_time(self, trajectory: List[Any]) -> int:
        """
        Retrieves the sum of the distances between stations.

        pre: a trajectory where the distances need to be calculated
        post: the total distance in minutes is returned
        """
        return sum([self.data[trajectory[i]].get_distance(trajectory[i + 1]) for i in range(len(trajectory) - 1)])

    def modify_third_to_last(self, railnetwork: List[List]) -> List:
        # Step 1: Select a random trajectory
        random_trajectory_index = random.randint(0, len(railnetwork) - 1)
        random_trajectory = self.railnetwork[random_trajectory_index]

        #length of trajectory
        length_trajectory = len(random_trajectory)

        #location fouth to last station so it wont go to the previous station
        previous_station = random_trajectory[-4]

        #pick the modification station third to last
        modification_station = random_trajectory[-3]
        if len(modification_station.get_connections()) <= 2:
            return None

        #pick the next station so it wont pick the same route again
        original_next_station = random_trajectory[-2]

        # Get the neighbors of the station at the third-to-last position
        neighbors = self.data[modification_station].get_connections()

        # Choose a new station that is a neighbor and different from the original and the second to last station
        new_station = random.choice([n for n in neighbors if n != original_next_station and n != previous_station])




