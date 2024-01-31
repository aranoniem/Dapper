# Import libraries
import random
import math

# Import classes
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

# Import functions
from code.functions.elements import get_random_station

class Simulated_annealing:
    def __init__(self, level: str):
        self.data = Load(level).objects
        self.level = level
        self.total_time = 0

    def solve(self, num_trajectories: int, timeframe: int, initial_temperature: float, cooling_rate: float) -> tuple:
        best_score = None
        best_railnetwork = None

        current_temperature = initial_temperature

        railnetwork = self.initial_solution(num_trajectories, timeframe)
        current_score = float(str(Score(self.level, railnetwork, self.total_time)))
        
        temperatures = []  # Store temperatures
        
        while current_temperature > 10:
            new_railnetwork = self.random_neighbor(railnetwork)
            new_score = float(str(Score(self.level, new_railnetwork, self.total_time)))
            
            # if the randomly generated number between 0 and 1 is smaller than the acceptance probability
            if self.acceptance_probability(current_score, new_score, current_temperature) > random.random():
                railnetwork = new_railnetwork
                current_score = new_score

            temperatures.append(current_temperature)  # Store current temperature
            
            print(railnetwork)
            print(current_score)
                
            # update the temperature because the cooling rate is basically the percentage that is removed each iteration so 1 - cooling rate is the growth factor
            current_temperature *= (1 - cooling_rate)

            if best_score is None or current_score > best_score:
                best_score = current_score
                best_railnetwork = railnetwork

        if best_score is not None:
            return best_score, best_railnetwork, temperatures
        else:
            return float('inf'), None, temperatures

    def initial_solution(self, num_trajectories: int, timeframe: int) -> list:
        railnetwork = []
        self.total_time = 0
        
        # for every route
        for _ in range(num_trajectories):
            trajectory = []
            visited_stations = set()
            duration = 0
    
            while True:
                # start from a random station not visited before
                if not trajectory:
                    station = get_random_station(self.data)
                else:
                    neighbors = self.data[trajectory[-1]].get_connections()
                    unvisited_neighbors = [n for n in neighbors if n not in visited_stations]
    
                    if not unvisited_neighbors:
                        break  # no unvisited neighbors, end the trajectory
                    station = random.choice(unvisited_neighbors)
    
                # calculate the distance to the new station
                if trajectory:
                    distance = self.data[trajectory[-1]].get_distance(station)
                    duration += distance
                    self.total_time += distance
    
                # check if the trajectory exceeds the timeframe
                if duration > timeframe:
                    break
    
                # add the station to the trajectory and update visited stations
                trajectory.append(station)
                visited_stations.add(station)
    
            railnetwork.append(trajectory)
    
        return railnetwork

    def random_neighbor(self, railnetwork: list) -> list:
        # make a copy to be able to adjust a single route
        new_railnetwork = railnetwork.copy()

        # choose a random trajectory and replace it with a new one
        random_trajectory_index = random.randint(0, len(new_railnetwork) - 1)
        new_railnetwork[random_trajectory_index] = self.initial_solution(1, float('inf'))[0]

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
