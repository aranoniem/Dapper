#import from libraries
from typing import Any
import sys
from sys import argv
import matplotlib.pyplot as plt
import os
import csv

#import from classes
sys.path.append('code')
from code.classes.load import Load
from code.algorithms.totally_random import Totally_random

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
    random = Totally_random(level_name)
    
    results = [random.solve(7, 120) for _ in range(10000)]
    print(results)

    
    # Create a directory called 'images' if it doesn't exist
    output_directory = 'plots'
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, 'histogram_10000_random.png')
    plt.hist(results, bins=50, edgecolor='black', linewidth=1.2)  # Adjust bins and linewidth
    plt.title('Histogram of Algorithm Results')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.savefig(output_path)

    # Print the path where the image is saved
    print(f"Histogram saved at: {output_path}")

    # Create a directory called 'result_csv' if it doesn't exist
    output_csv_directory = 'result_csv'
    os.makedirs(output_csv_directory, exist_ok=True)

    # Save the results in a CSV file
    output_csv_path = os.path.join(output_csv_directory, 'results_10000_random.csv')
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




