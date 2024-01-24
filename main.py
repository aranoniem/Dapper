#import from libraries
from typing import Any
import sys
from sys import argv
import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns
from seaborn import kdeplot

#import from classes
sys.path.append('code')
from code.classes.load import Load
from code.algorithms.totally_random import Totally_random
from code.algorithms.semi_random import Semi_random
from code.algorithms.greedy import GreedySearch

#from railnetwork import Railnetwork

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


    # Create connections
    rail_nl = Load(level_name)

    print('Welcome to RailNL.\n')
    
    # Usage example:
    loader = Load(level_name)
    semi_random = Semi_random(level_name)
    totally_random = Totally_random(level_name)
    greedy = GreedySearch(level_name, 7, 120, 4)
    
    # Results for all three algorithms
    results_semi_random = [semi_random.solve(7, 120) for _ in range(2500)]
    results_totally_random = [totally_random.solve(7, 120) for _ in range(2500)]
    results_greedy = [greedy._solve() for _ in range(2500)]

    # Create a directory called 'images' if it doesn't exist
    output_directory = 'plots'
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, 'comparison')

    # Plot histograms as line graphs for all three algorithms with different colors
    plt.hist(results_semi_random, bins=50, edgecolor='blue', linewidth=1.2, alpha=0.7, label='Semi-random', density=False, histtype='step')
    plt.hist(results_totally_random, bins=50, edgecolor='green', linewidth=1.2, alpha=0.7, label='Totally random', density=False, histtype='step')
    plt.hist(results_greedy, bins=50, edgecolor='red', linewidth=1.2, alpha=0.7, label='Greedy', density=False, histtype='step')

    # Adjust linewidth and add legend
    plt.title('Line Graph of Algorithm Results')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend()

    plt.savefig(output_path)
    plt.show()

    # Print the path where the image is saved
    print(f"Histogram saved at: {output_path}")
    
    # Create a directory called 'result_csv' if it doesn't exist
    output_csv_directory = 'result_csv'
    os.makedirs(output_csv_directory, exist_ok=True)

    # Save the results in a CSV file
    output_csv_path = os.path.join(output_csv_directory, 'test')
    with open(output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Result'])  # Write header
        csvwriter.writerows([[result] for result in results])  # Write results
        


    #train_1 = rail_nl.generate_trajectory()
    #TEST STATEMENT print(train_1)
    #train_2 = rail_nl.generate_trajectory()
    #train_3 = rail_nl.generate_trajectory()

    #TEST STATEMENT print('train, stations')
    #print("trein,stations")
    #print(f'train_1, "{train_1}"')
    #print(f'train_2, "{train_2}"')  
    #print(f'train_3, "{train_3}"')




