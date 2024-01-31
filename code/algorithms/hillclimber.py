# Import libraries
from typing import Any, List, Tuple

# Import classes
from .semi_random import Semi_random
from code.classes.score import Score

class Hillclimber(Semi_random):
    def __init__(self, level: str):
        """
        Initialize the parent algorithm which is semi_random

        pre: use the semi_random class
        post: all definitions from the semi_random class and the data are now usable 
        """
        super().__init__(level)

    def solve(self, max_trajectory: int, timeframe: int, max_iterations: int) -> Tuple[int, List[Any]]:
        """
        Searches for the highest score by deleting, adding, or swapping trajectories,
        but stops when there is no alteration for the max amount of iterations

        pre: a timeframe is needed, a maximum amount of trajectories, and a max amount of iterations
        post: it returns a solution which has altered a semi_random solution
        """
        #initialize start of iterations
        self.iterations = 0

        # calculate quality score for the random rail network
        total_time, railnetwork = self.generate_railnetwork(max_trajectory, timeframe)
        quality_score = float(Score(self.level, railnetwork, total_time).K)

        # when there is no change in max_iterations, the algorithm will stop
        while self.iterations <= max_iterations:

            # generate a random trajectory
            self.duration, self.new_trajectory = self.generate_trajectory(timeframe)

            #if there is no swap or addition there is no need to check for possible deletions multiple times
            if self.iterations <= 1:
            # Search for better solutions when trajectories are removed
                quality_score, railnetwork, total_time = self.remove_trajectory(quality_score, railnetwork, total_time)

            # Search for better solutions when a new trajectory is added
            quality_score, railnetwork, total_time = self.add_trajectory(quality_score, railnetwork, total_time, max_trajectory)

            # don't perform a swap if already added to lower the runtime 
            if self.added is False:
                # Search for higher solutions when swapping
                quality_score, railnetwork, total_time = self.swap_trajectory(quality_score, railnetwork, total_time)

            self.iterations += 1
            
            
            print(self.iterations)

        print(quality_score, railnetwork)
        return quality_score, railnetwork

    def remove_trajectory(self, quality_score: float, railnetwork: List[Any], total_time: int) -> Tuple[float, List[Any], int]:
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
            temp_quality_score = float(Score(self.level, temp_railnetwork, (total_time - deleted_time)).K)

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

    def add_trajectory(self, quality_score: float, railnetwork: List[Any], total_time: int, max_trajectory: int) -> Tuple[float, List[Any], int]:
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
            temp_quality_score = float(Score(self.level, temp_railnetwork, temp_total_time).K)

            # if addition returns a better solution, add
            if temp_quality_score > quality_score:
                quality_score = temp_quality_score
                railnetwork = temp_railnetwork
                total_time = temp_total_time
                self.added = True
                self.iterations = 0

        return quality_score, railnetwork, total_time

    def swap_trajectory(self, quality_score: float, railnetwork: List[Any], total_time: int) -> Tuple[float, List[Any], int]:
        """
        Looks for a better score when a trajectory is swapped with a 
        random trajectory in a rail network

        pre: a rail network with its quality score and total time is needed,
             with a randomly generated rail network
        post: if a swap leads to a better result, a trajectory is swapped
        """
        # initialize variables
        trajectory_count = len(railnetwork)
        best_swap_score = 0

        for i in range(trajectory_count):
            # calculate a new score when swapping each trajectory
            temp_railnetwork = railnetwork.copy()
            trajectory_time = self.calculate_time(temp_railnetwork[i])
            temp_railnetwork[i] = self.new_trajectory
            temp_total_time = total_time - trajectory_time + self.duration
            temp_quality_score = float(Score(self.level, temp_railnetwork, temp_total_time).K)

            # searches for the best solution in all swaps
            if temp_quality_score > best_swap_score:
                best_swap_score = temp_quality_score
                best_swap_railnetwork = temp_railnetwork
                best_swap_total_time = temp_total_time

        # make a swap if there is a better solution 
        if best_swap_score > quality_score:
            quality_score = best_swap_score
            railnetwork = best_swap_railnetwork
            total_time = best_swap_total_time
            self.iterations = 0

        return quality_score, railnetwork, total_time

    def calculate_time(self, trajectory: List[Any]) -> int:
        """
        Retrieves the sum of the distances between stations.

        pre: a trajectory where the distances need to be calculated
        post: the total distance in minutes is returned
        """
        return sum([self.data[trajectory[i]].get_distance(trajectory[i + 1]) for i in range(len(trajectory) - 1)])
