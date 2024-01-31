#import from libraries
from typing import Any
import sys
from sys import argv
import matplotlib.pyplot as plt
import os
import csv

# Import from classes
sys.path.append('code')
from code.algorithms.totally_random import Totally_random
from code.algorithms.semi_random import Semi_random
from code.algorithms.greedy_search import Greedy_search
from code.algorithms.depth_first import Depth_first
from code.algorithms.breadth_first import Breadth_first
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.local_search import Local_search
from code.algorithms.simulated_annealing import Simulated_annealing

sys.path.append('functions')
from functions.helpers import get_user_input, finetune_railnetwork
from functions.elements import get_random_station

sys.path.append('visualisation')
from visualisation.coordinates import Railroadmap

if __name__ == '__main__':

    # Check command line arguments
    if len(argv) not in [1,2]:
        print('Usage python3 station.py [name]')
        exit(1)

    # Load the requested connections or else use Holland
    if len(argv) == 1: 
        level_name = 'Holland'
    elif len(argv) == 2:
        level_name = argv[1]

    print('Welcome to RailNL.\n')

    algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations = get_user_input()

    algorithm = globals()[algorithm_choice.capitalize()](level_name)  # Adjust the parameters as needed

    results = []
    best_quality_score = 0

    for i in range(iterations):
        if algorithm_choice == "hillclimber" or algorithm_choice == "local_search":
            print("in if")
            quality_score, railnetwork = algorithm.solve(trajectories, timeframe, max_iterations)
        elif algorithm_choice == "simulated_annealing":
            quality_score, railnetwork, temperature = algorithm.solve(trajectories, timeframe, 8000, 0.1)
        else:
            quality_score, railnetwork = algorithm.solve(trajectories, timeframe)

        railnetwork = finetune_railnetwork(railnetwork)
        if i == 0:
            best_railnetwork = railnetwork.copy()

        #create results and find maximum solution
        results.append(quality_score)
        if quality_score > best_quality_score:
            best_quality_score = quality_score
            best_railnetwork = railnetwork


    # Create a directory called '' if it doesn't exist
    output_directory = 'plots'
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, f'{level_name}_{iterations}_{algorithm_choice}')
    plt.hist(results, bins=50, edgecolor='black', linewidth=1.2)

    # Adjust linewidth and add legend
    plt.title(f'Optimizing Algorithm Performance: {algorithm_choice.capitalize()} Approach\nHistogram Analysis at {level_name.capitalize()} Level')
    plt.xlabel(f'Quality score, max score = {best_quality_score}')
    plt.ylabel(f'Frequency (N = {iterations})')

    plt.savefig(output_path)
    plt.show()

    # Create a directory called '' if it doesn't exist
    output_directory = 'csv_files'
    os.makedirs(output_directory, exist_ok=True)

    # Save railnetwork to CSV
    #railnetwork_csv_path = os.path.join(output_directory, f'{level_name}_{iterations}_{algorithm_choice}.csv')
    railnetwork_csv_path = os.path.join(output_directory, f'output.csv')
    with open(railnetwork_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['train', 'stations'])
        for i in range(len(best_railnetwork)):
            csv_writer.writerow([f'train_{i + 1}', str(best_railnetwork[i])])
        csv_writer.writerow(['score', best_quality_score])
    print("in csv")
    
    railroad_map = Railroadmap(level_name)
    railroad_map.main(best_railnetwork)
