#import from libraries
from typing import Any
import sys
from sys import argv
import os
import csv

#import from classes
sys.path.append('code')
from code.classes.load import Load
from code.algorithms.depth_first import DepthFirst

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
    algoritm = DepthFirst(level_name)
    algoritm.solve(3, 120)
    
    # results = [random.solve(7, 120) for _ in range(100)]
    #print(results)


