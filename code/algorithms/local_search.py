# Import libraries
from typing import Any, List, Tuple

# Import classes
from .hillclimber import Hillclimber
from code.classes.score import Score
from code.classes.trajectory import Trajectory


class Local_search(Hillclimber):
    """
    Local search will take a hillclimber solution and search if there are
    starting- and ending stations that can be removed to improve the score
    """
    def __init__(self, level: str):
        """
        Initialize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """
        # Call the constructor of the parent class
        super().__init__(level)

    def solve(self, timeframe: int, max_trajectory: int, max_iterations: int) -> Tuple[float, List[Any]]:
        """
        Create a solution where the beginning station and end station are
        removed for a better score

        pre: give a solution from the hillclimber algorithm
        post: return possibly improved railnetwork and score
        """
        quality_score, railnetwork = super().solve(timeframe, max_trajectory, max_iterations)
        iterations = 0

        # Calculate total time of the trajectory
        total_time = 0
        for i in range(len(railnetwork)):
            trajectory = Trajectory(railnetwork[i], self.data)
            trajectory.calc_time()
            time = trajectory.get_time()
            total_time += time

        while iterations <= 1:
            # Start with the best solution
            temp_railnetwork = railnetwork.copy()

            for i in range(len(temp_railnetwork)):
                # Search if deleting the first station will improve the
                # solution
                temp_trajectory = temp_railnetwork[i].copy()
                deleted_time = self.data[temp_trajectory[0]].get_distance(temp_trajectory[1])
                temp_trajectory.pop(0)
                temp_total_time = total_time - deleted_time
                temp_railnetwork[i] = temp_trajectory
                temp_quality_score = Score(self.level, temp_railnetwork, temp_total_time).K

                if temp_quality_score > quality_score:
                    temp_railnetwork[i] = temp_trajectory.copy()
                    railnetwork = temp_railnetwork
                    total_time = temp_total_time
                    quality_score = temp_quality_score
                    iterations = 0

            iterations += 1
        iterations = 0

        while iterations <= 1:
            # Start with the best solution
            temp_railnetwork = railnetwork.copy()

            for i in range(len(temp_railnetwork)):
                # Search if deleting the last station will improve the solution
                temp_trajectory = temp_railnetwork[i].copy()
                length_trajectory = len(temp_trajectory) - 1
                deleted_time = self.data[temp_trajectory[length_trajectory]].get_distance(temp_trajectory[length_trajectory - 1])
                temp_trajectory.pop()
                temp_total_time = total_time - deleted_time
                temp_railnetwork[i] = temp_trajectory
                temp_quality_score = Score(self.level, temp_railnetwork, temp_total_time).K

                if temp_quality_score > quality_score:
                    temp_railnetwork[i] = temp_trajectory.copy()
                    railnetwork = temp_railnetwork
                    total_time = temp_total_time
                    quality_score = temp_quality_score
                    iterations = 0

            iterations += 1

        return quality_score, railnetwork
