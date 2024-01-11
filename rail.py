import csv
from trajectory import Trajectory

class Rail():

    def __init__(self, level):
        """
        Initialises connections for the appropriate 'railnetwork' version.

        post: sets up variables to store information about trajectories
        TODO: EIND: check beschrijving
        """
        #initialize an empty trajectory dictionary
        self.trajectories = {}

        #load connections between stations
        self.load_connections(f"data/Connecties{level}.csv")

    def load_connections(self, filename):
        """
        Parses information into memory

        pre: filename of railway data is specified
        post: stations and distances are all loaded into memory and connected
        """
        with open(filename, "r") as csv_file:
            # Skip the header line
            csv_file.readline()


            # Loading stations connections
            while True:
                lines = csv_file.readline()
                data = lines.split(",")

                if not lines:
                    break

                departure_station, arrival_station, distance = map(str.strip, data)
                trajectory = Trajectory(departure_station, arrival_station, distance)
                if trajectory not in self.trajectories:
                    self.trajectories[departure_station] = trajectory

            #assert self.trajectories[0].departure_station == "Alkmaar"
            #assert self.trajectories[0].arrival_station == "Hoorn"
            #assert self.trajectories[0].distance == 24
    
    def get_description(self):
        print(self.trajectories)
        for i in self.trajectories:
            print(self.trajectories[i])
        return True

            
if __name__ == "__main__":

    from sys import argv

    # Check command line arguments
    if len(argv) not in [1,2]:
        print("Usage python3 rail.py [name]")
        exit(1)

    # Load the requested connections or else use Holland
    if len(argv) == 1: 
        level_name = "Holland"
    elif len(argv) == 2:
        level_name = argv[1]

    # Create connections
    rail_nl = Rail(level_name)

    print("Welcome to RailNL.\n")

    rail_nl.get_description()




    