# import libraries
from typing import Any, List, Tuple

# Import classes
from .hillclimber import Hillclimber  # Import hillclimber class
from code.classes.score import Score

class Local_search(Hillclimber):
    def __init__(self, level: str):
        """
        Initialize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """
        super().__init__(level)  # Call the constructor of the parent class
    

    def solve(self, timeframe: int, max_trajectory: int, max_iterations: int) -> Tuple[float, List[Any]]:
        """
        Create a solution where the beginning station and end station are removed for a better score

        pre: give a solution from the hillclimber algorithm
        post: return possibly improved railnetwork and score
        """

        quality_score, railnetwork, total_time = Hillclimber.solve(max_trajectory,timeframe, max_iterations)
        print(f"qs", quality_score)
        iterations = 0
        print(f"total time", total_time)

        while iterations <= 1:
            # start with the best solution
            temp_railnetwork = railnetwork.copy()

            for i in range(len(temp_railnetwork)):
                # search if deleting the first station will improve the solution
                temp_trajectory = temp_railnetwork[i].copy()
                print(temp_trajectory)
                deleted_time = self.data[temp_trajectory[0]].get_distance(temp_trajectory[1])
                temp_trajectory.pop(0)
                print(temp_trajectory)
                temp_total_time = total_time - deleted_time
                print(f"temp, tot, del", temp_total_time, total_time, deleted_time)
                temp_quality_score = Score(self.level, railnetwork, temp_total_time).K
                print("temp_score", temp_quality_score)
                print(temp_quality_score)

                if temp_quality_score > quality_score:
                    print("in if")
                    railnetwork[i] = temp_trajectory
                    total_time = temp_total_time
                    quality_score = temp_quality_score
                    iterations = 0

                # search if deleting the last station will improve the solution
                temp_trajectory = temp_railnetwork[i].copy()
                print(temp_trajectory)
                length_trajectory = len(temp_trajectory) - 1
                deleted_time = self.data[temp_trajectory[length_trajectory]].get_distance(temp_trajectory[length_trajectory - 1])
                temp_trajectory.pop()
                print(temp_trajectory)
                temp_total_time = total_time - deleted_time
                print(f"temp, tot, del", temp_total_time, total_time, deleted_time)
                temp_quality_score = Score(self.level, railnetwork, temp_total_time).K
                print("temp_score", temp_quality_score)
                print(temp_quality_score)

                if temp_quality_score > quality_score:
                    print("in if")
                    railnetwork[i] = temp_trajectory
                    total_time = temp_total_time
                    quality_score = temp_quality_score
                    iterations = 0
            iterations += 1
            print(iterations)

        return quality_score, railnetwork           

