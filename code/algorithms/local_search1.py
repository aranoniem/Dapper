# Import libraries
from typing import Any

# Import classes
from .semi_random import Semi_random # Import Semi_random class
from code.classes.score import Score

class Local_search(Semi_random):
    def __init__(self, level: str):
        """
        Initialize the algorithm and load all station objects

        pre: use the Load class
        post: a dictionary with all objects is initialized
        """
        super().__init__(level)  # Call the constructor of the parent class

    def solve(self, timeframe, max_trajectory, max_iterations: int):
        iterations = 0
        total_time, railnetwork = self.generate_railnetwork(max_trajectory, timeframe)
        quality_score = int(Score(self.level, railnetwork, total_time).K)
        print(self.trajectory_count)
        print(f"railnetwork:", [railnetwork], "\n")


        while iterations <= max_iterations:
            new_trajectory = self.generate_trajectory(timeframe)[1]  # Use generate_trajectory from Semi_random
            print(f"possible new trajectory:", [new_trajectory], "\n")
            temp_railnetwork = railnetwork  
            print(f"qualityscore:", {quality_score},"\n")

            for i in range(self.trajectory_count):
                temp_railnetwork[i] = new_trajectory
                temp_quality_score = int(Score(self.level, temp_railnetwork, timeframe).K)
                print("temp quality score:",{temp_quality_score}, "\n")
                if temp_quality_score > quality_score:
                    quality_score = temp_quality_score
                    railnetwork = temp_railnetwork  
                    iterations = 0
                    print("make change")
                else:
                    print(f"iterations:", {iterations}, "\n")
                    temp_railnetwork = railnetwork
            
            iterations += 1

        return quality_score, railnetwork
    