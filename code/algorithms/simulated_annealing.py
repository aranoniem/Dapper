# Import libraries
import random
import math

# Import classes
from code.classes.station import Station
from code.classes.score import Score

# Import parent
from .semi_random import Semi_random

class Simulated_annealing(Semi_random):

    def __init__(self, level: str):
        super().__init__(level)


    def solve(self, max_trajectory: int, timeframe: int, initial_temperature: float, cooling_rate: float) -> tuple:
        best_score = 0
        best_railnetwork = None

        current_temperature = initial_temperature

        railnetwork, total_time = self.generate_railnetwork(max_trajectory, timeframe)
        current_score = float(str(Score(self.level, railnetwork, total_time)))
        
        temperatures = []  # Store temperatures
        
        while current_temperature > 10:
            new_railnetwork = self.swap_trajectory(railnetwork, timeframe)
            new_score = float(str(Score(self.level, new_railnetwork, total_time)))
            
            # if the randomly generated number between 0 and 1 is smaller than the acceptance probability
            if self.acceptance_probability(current_score, new_score, current_temperature) > random.random():
                railnetwork = new_railnetwork
                current_score = new_score

            temperatures.append(current_temperature)  # Store current temperature
            
            print(railnetwork)
            print(current_score)
                
            # Update the temperature because the cooling rate is basically the percentage that is removed each iteration so 1 - cooling rate is the growth factor
            current_temperature *= (1 - cooling_rate)

            if best_score is None or current_score > best_score:
                best_score = current_score
                best_railnetwork = railnetwork

        if best_score is not None:
            return best_score, best_railnetwork
        else:
            return float('inf'), None, temperatures

    def swap_trajectory(self, railnetwork: list, timeframe: int) -> list:
        # Make a copy to be able to adjust a single route
        new_railnetwork = railnetwork.copy()

        # Choose a random trajectory and replace it with a new one
        random_trajectory_index = random.randint(0, len(new_railnetwork) - 1)
        new_railnetwork[random_trajectory_index] = self.generate_trajectory(timeframe)

        return new_railnetwork

    def acceptance_probability(self, current_score: float, new_score: float, temperature: float) -> float:
        """
        Determines the probability that a solution will be accepted. The value of this function is compared to random.random() that generates a random number between 0 and 1
        this is why it returns 1 if the current solution is better than the previous solution because it always accepts it in that way. Because the temperature decreases it becomes 
        less likely a bad solution will be accepted because the fraction of the exponent will be bigger.
        """
        if new_score > current_score:
            return 1.0
        return math.exp((new_score - current_score) / temperature)
