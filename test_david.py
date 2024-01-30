#import from libraries
from typing import Any
import sys
from sys import argv
import matplotlib.pyplot as plt
import os
import csv

#import from classes
sys.path.append('code')
from code.algorithms.totally_random import Totally_random
from code.algorithms.semi_random import Semi_random
from code.algorithms.greedy import GreedySearch
from code.algorithms.depth_first import DepthFirst
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.local_search import Local_search

sys.path.append('functions')
from functions.user_interface import get_user_input

#from railnetwork import Railnetwork

if __name__ == '__main__':
    
    print('Welcome to RailNL.\n')

    algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations  = get_user_input()
 
    algorithm = globals()[algorithm_choice.capitalize()](level_name)  # Adjust the parameters as needed

    results = []
    best_quality_score = 0
    if algorithm_choice in ["hillclimber", "local_search", "simulated_annealing"]:
        for i in range(iterations):
            quality_score, railnetwork, _ = algorithm.solve(trajectories, timeframe, max_iterations)
            results.append(quality_score)
            if quality_score > best_quality_score:
                best_quality_score = quality_score
                best_railnetwork = railnetwork
    else:
        for i in range(iterations):
            quality_score, railnetwork = algorithm.solve(trajectories, timeframe)
            results.append(quality_score)
            if quality_score > best_quality_score:
                best_quality_score = quality_score
                best_railnetwork = railnetwork

    # Create a directory called '' if it doesn't exist
    output_directory = 'plots'
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, 'nationaal_20_250_hillclimber')
    plt.hist(results, bins = 50, edgecolor = 'black', linewidth = 1.2)

    # Adjust linewidth and add legend
    plt.title(f'Optimizing Algorithm Performance: {algorithm_choice.capitalize()} Approach\nHistogram Analysis at {level_name.capitalize()} Level')
    plt.xlabel(f'Quality score, max score = {best_quality_score}')
    plt.ylabel(f'Frequency (N = {iterations})')

    plt.savefig(output_path)
    plt.show()

    # Save railnetwork to CSV
    railnetwork_csv_path = os.path.join(output_directory, 'max_solution_railnetwork_definite.csv')
    with open(railnetwork_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['train', 'stations'])
        for i, trajectory in enumerate(best_railnetwork, start=1):
            csv_writer.writerow([f'train_{i}', str(trajectory)])
        csv_writer.writerow(['score', best_quality_score])