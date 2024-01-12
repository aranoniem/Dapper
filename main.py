from typing import Any
from station import Station
#from railnetwork import Railnetwork

if __name__ == '__main__':

    from sys import argv

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
    rail_nl = Station(level_name)

    #TEST STATEMENT rail_nl.print_station_overview()
    print('Welcome to RailNL.\n')


    train_1 = rail_nl.generate_trajectory()
    #TEST STATEMENT print(train_1)
    train_2 = rail_nl.generate_trajectory()
    train_3 = rail_nl.generate_trajectory()

    #TEST STATEMENT print('train, stations')
    print("trein,stations")
    print(f'train_1, "{train_1}"')
    print(f'train_2, "{train_2}"')  
    print(f'train_3, "{train_3}"')


