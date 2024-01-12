from connection import Connection
import random

class Station():
    """
    Contains all the departure stations, and is linked to the 
    arrivals stations through the Connection class
    """
    def __init__(self, level):
        """
        Initialises connections for the appropriate 'railnetwork' version.

        post: sets up variables to store information about connections
        TODO: EIND: check beschrijving
        """
        #initialize an empty connection dictionary
        self.stations = {}

        #load connections between stations
        # TODO move this function into load_connections to be able to use the station class in other classes and code?
        self.load_connections(f'data/Connecties{level}.csv')

    def load_connections(self, filename) -> None:
        """
        Parses information into memory

        pre: filename of railway data is specified
        post: stations and distances are all loaded into memory and connected
        """
        with open(filename, 'r') as csv_file:
            # Skip the header line
            csv_file.readline()

            # TODO use panda to load csv_file instead of while true loop
            # Loading stations connections
            while True:
                
                lines = csv_file.readline().strip()
                data = lines.split(',')
                if not lines:
                    break
                departure_station = data[0]
                arrival_station = data[1]
                distance = data[2]
                #TEST STATEMENT print(data)

                if departure_station not in self.stations:
                    # als departure niet in self.stations is, dan departure station toevoegen
                    # als departure wel in self.stations, dan arrival_station en distance toevoegen aan trajctory
                    # class onder departure station
                    
                    self.stations[departure_station] = Connection(arrival_station, distance)
                else:
                    connection = Connection(arrival_station, distance)
                    self.stations[departure_station].update_connection(arrival_station, distance)
                
                # Omdat alle trajecten beide kanten omgaan, draaien we de arrivals en departures om, zodat elk station alle connecties heeft opgeslagen
                departure_station = data[1]
                arrival_station = data[0]
                distance = data[2]
                

                if departure_station not in self.stations:
                    # als departure niet in self.stations is, dan departure station toevoegen
                    # als departure wel in self.stations, dan arrival_station en distance toevoegen aan trajctory
                    # class onder departure station
                    
                    self.stations[departure_station] = Connection(arrival_station, distance)
                else:
                    connection = Connection(arrival_station, distance)
                    self.stations[departure_station].update_connection(arrival_station, distance)
                
            # BUG deze asserts moeten verander worden en anders!
            #assert self.stations['Alkmaar'].arrival_station == 'Hoorn'
            #assert self.stations['Alkmaar'].arrival_station == 'Den Helder'
            #assert self.stations['Alkmaar'].distance == '36'
            #print(self.stations['Alkmaar'].arrival_station)    

    def print_station_overview(self) -> None:
        """
        For logic purposes if you want to see the overview of all connections

        post: print an overview of all stations, connections and distances
        """

        for station_name, station_instance in self.stations.items():
            print(f'{station_name}: {str(station_instance)}')

    def random_station(self):
        """
        find a random station for the purpose of a starting point

        post: returns a random station
        """
        random_station = random.choice(list(self.stations.keys()))
        #TEST STATEMENT print(f'start station = {random_station}')
        return random_station

    def random_connection(self, departure_station):
        """
        find a random connection for the purpose of making a trajectory

        pre: enter a departure station
        post: returns a station connected with the departure station 
        """
        neighbours = list(self.stations[departure_station].get_connection())
        #TEST STATEMENT print(f'Connecties zijn: {neighbours}')

        #TEST STATEMENT print(f'aantal buren: {len(neighbours)}')

        if len(neighbours) > 1:
            random_index = random.randint(1, len(neighbours))
            #TEST STATEMENT print(random_index)
            random_neighbour = neighbours[random_index - 1]
            #TEST STATEMENT print(random_neighbour)
        else:
            random_neighbour = neighbours[0]
        return random_neighbour
    
    def generate_trajectory(self):
        """
        generate a trajectory based on hopping through stations
        that are connected based on randomness

        post: returns a list of connected stations
        """
        # Initialize an empty list for a trajectory
        trajectory = []

        # Choose a random starting station
        _station = self.random_station()
        #TEST STATEMENT print(_station)
        trajectory.append(_station)

        for i in range(5):
            i = i + 1
            new_station = self.random_connection(_station)
            trajectory.append(new_station)
            _station = new_station
            
        return trajectory
