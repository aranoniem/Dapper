# Import from libraries
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

# Import from functions
sys.path.append('functions')
from functions.helpers import get_user_input, finetune_railnetwork
from functions.elements import get_random_station

sys.path.append('visualisation')
from visualisation.coordinates import Railroadmap

if __name__ == '__main__':

    print('Welcome to RailNL.\n')

    algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations = get_user_input()

    algorithm = globals()[algorithm_choice.capitalize()](level_name)  # Adjust the parameters as needed

    # Initalize
    results = []
    best_quality_score = 0

    # Run algorithm of choice
    for i in range(iterations):
        if algorithm_choice == "hillclimber" or algorithm_choice == "local_search":
            quality_score, railnetwork = algorithm.solve(trajectories, timeframe, max_iterations)
        else:
            quality_score, railnetwork = algorithm.solve(trajectories, timeframe)

        # If no better railnetwork, use default
        if i == 0:
            best_railnetwork = railnetwork.copy()

        # Create results and find maximum solution
        results.append(quality_score)
        if quality_score > best_quality_score:
            best_quality_score = quality_score
            best_railnetwork = railnetwork

    # Create a directory called maps
    output_directory = 'results/maps'
    os.makedirs(output_directory, exist_ok=True)

    # Create visualisation
    railroad_map = Railroadmap(level_name)
    railroad_map.main(best_railnetwork)

    output_path = os.path.join(output_directory, f'{level_name}_{iterations}_{algorithm_choice}_map')
    plt.title(f'Optimizing Algorithm Performance: {algorithm_choice.capitalize()} Approach\nVisualisation at {level_name.capitalize()} Level')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.grid(True)
    plt.savefig(output_path)
    plt.clf()

    # Create a directory plots
    output_directory = 'results/plots'
    os.makedirs(output_directory, exist_ok=True)

    # Adjust the plot to liking
    output_path = os.path.join(output_directory, f'{level_name}_{iterations}_{algorithm_choice}')
    plt.hist(results, bins=50, edgecolor='black', linewidth=1.2)
    plt.title(f'Optimizing Algorithm Performance: {algorithm_choice.capitalize()} Approach\nHistogram Analysis at {level_name.capitalize()} Level')
    plt.xlabel(f'Quality score, max score = {best_quality_score}')
    plt.ylabel(f'Frequency (N = {iterations})')
    plt.savefig(output_path)
    plt.clf()

    # Create a directory called csv_files
    output_directory = 'results/csv_files'
    os.makedirs(output_directory, exist_ok=True)

    # Finetune output
    railnetwork = finetune_railnetwork(railnetwork)

    # Save railnetwork to CSV
    railnetwork_csv_path = os.path.join(output_directory, f'{level_name}_{iterations}_{algorithm_choice}.csv')
    with open(railnetwork_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['train', 'stations'])
        for i in range(len(best_railnetwork)):
            csv_writer.writerow([f'train_{i + 1}', str(best_railnetwork[i])])
        csv_writer.writerow(['score', best_quality_score])
