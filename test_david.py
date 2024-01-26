#import from libraries
from typing import Any
import sys
from sys import argv
import matplotlib.pyplot as plt
import os

#import from classes
sys.path.append('code')
from code.classes.load import Load
from code.algorithms.totally_random import Totally_random
from code.algorithms.semi_random import Semi_random
from code.algorithms.greedy import GreedySearch
from code.algorithms.local_search1 import Local_search

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
    semi_random = Semi_random(level_name)
    totally_random = Totally_random(level_name)
    local_search = Local_search(level_name)
    
    # Results for all three algorithms
    #results_semi_random = [semi_random.solve(7, 120) for _ in range(2500)]
    #results_totally_random = [totally_random.solve(7, 120) for _ in range(2500)]
    #max_score, railnetwork, results = local_search.solve(180, 20, 100)
    results_local_search = [local_search.solve2(180, 20, 10)[0] for _ in range(1)]
    maximum = int(max(results_local_search))

    # Create a directory called 'images' if it doesn't exist
    output_directory = 'plots'
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, 'test_local_search_holland')
    plt.hist(results_local_search, bins = 50, edgecolor = 'black', linewidth = 1.2)

    # Adjust linewidth and add legend
    plt.title('test results local search')
    plt.xlabel(f'Score, max score = {maximum}')
    plt.ylabel('Frequency')
    plt.legend()

    plt.savefig(output_path)
    plt.show()