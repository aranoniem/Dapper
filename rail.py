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
                departure_station = data[0]
                arrival_station = data[1]
                distance = data[2]

                if not lines:
                    break

                if departure_station not in self.trajectories:
                """
                als departure niet in self.trajectories is, dan departure station toevoegen
                als departure wel in self.trajectories, dan arrival_station en distance toevoegen aan trajctory
                class onder departure station
                """

            


                    self.trajectories.add_trajectory(arrival_station, distance)
                else:
                    trajectory = Trajectory(arrival_station, distance)
                    self.trajectories[departure_station] = trajectory
                
                

            assert self.trajectories["Alkmaar"].departure_station == "Alkmaar"
            assert self.trajectories["Alkmaar"].arrival_station == "Den Helder"
            assert self.trajectories["Alkmaar"].distance == "36"
            print(self.trajectories["Alkmaar"].arrival_station)
    
    def get_description(self):
            

            
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




    