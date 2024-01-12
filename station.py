import csv
from connection import Connection

class Station():

    def __init__(self, level):
        """
        Initialises connections for the appropriate 'railnetwork' version.

        post: sets up variables to store information about connections
        TODO: EIND: check beschrijving
        """
        #initialize an empty connection dictionary
        self.stations = {}

        #load connections between stations
        self.load_connections(f'data/Connecties{level}.csv')

    def load_connections(self, filename):
        """
        Parses information into memory

        pre: filename of railway data is specified
        post: stations and distances are all loaded into memory and connected
        """
        with open(filename, 'r') as csv_file:
            # Skip the header line
            csv_file.readline()


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
    
    def get_description(self):
        pass
    

    def print_station_overview(self):
        for station_name, station_instance in self.stations.items():
            print(f'{station_name}: {str(station_instance)}')
