# Import libraries
from typing import Any, List, Tuple

# Import classes
from .local_search1 import Local_search1 # Import Semi_random class
from code.classes.score import Score

class Local_search2(Local_search1):
    def __init__(self, level: str):
        """
        Initialize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """
        super().__init__(level)  # Call the constructor of the parent class
    

    def solve2(self, timeframe, max_trajectory, max_iterations: int):
        quality_score, railnetwork, _ = self.solve(timeframe, max_trajectory, max_iterations)
        for i in range(len(railnetwork) - 1):
            duration = self.calculate_time(railnetwork[i])
            total_time += duration
            print(duration)

        print(total_time)

        temp_railnetwork = railnetwork.copy()
        for i, trajectory in enumerate(temp_railnetwork):
            temp_railnetwork[i] = trajectory.pop(0)
            deleted_time = self.calculate_time(trajectory[0])
            temp_total_time = total_time - deleted_time
            temp_quality_score = int(Score(self.level, railnetwork, temp_total_time).K)

            if temp_quality_score > quality_score:
                railnetwork = temp_railnetwork
                total_time = temp_total_time
                quality_score = temp_quality_score

        for i, trajectory in enumerate(temp_railnetwork):
            temp_railnetwork[i] = trajectory.pop()
            deleted_time = self.calculate_time(trajectory[0])
            temp_total_time = total_time - deleted_time
            temp_quality_score = int(Score(self.level, railnetwork, temp_total_time).K)

            if temp_quality_score > quality_score:
                railnetwork = temp_railnetwork
                total_time = temp_total_time
                quality_score = temp_quality_score

        return quality_score, railnetwork
                

            
                

