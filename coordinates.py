import csv
import matplotlib.pyplot as plt

class Railroadmap:
    def __init__(self, name, latitude, longitude):
        """
        Initializes the name, latitude, and longitude for each separate instance.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connections = []  # List to store connected locations
        self.times = []  # List to store corresponding travel times

    def read_locations(self, file_path):
        """
        Reads out the file with station coordinates; saves and returns the coordinates mapped to their station.
        """
        locations = {}
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                name, latitude, longitude = row
                locations[name] = Railroadmap(name, float(latitude), float(longitude))

        return locations

    def read_connections(self, file_path):
        """
        Reads out the file with railroad connections and saves the departure and arrival stations mapped in a dictionary.
        """
        connections = {}

        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                if len(row) < 3:
                    continue  # Skip incomplete lines

                departure_station, arrival_station, time = row

                if departure_station not in connections:
                    connections[departure_station] = []

                connections[departure_station].append((arrival_station, time))

        return connections

    def plot_locations(self, locations, connections):
        """
        Uses locations and connections that are passed to the method to create a graph structure with matplotlib.
        """
        plt.scatter([loc.longitude for loc in locations.values()], [loc.latitude for loc in locations.values()], marker='o', color='red')

        for loc in locations.values():
            plt.text(loc.longitude, loc.latitude, loc.name, ha='right', va='bottom', fontsize=8)

        for departure_station, connection_list in connections.items():
            dep_coords = locations[departure_station]

            for connection in connection_list:
                arrival_location, time = connection
                arr_coords = locations[arrival_location]

                # create a blue line from the current departure station to the current departure station at the corresponding coordinates
                plt.plot([dep_coords.longitude, arr_coords.longitude], [dep_coords.latitude, arr_coords.latitude], linestyle='-', color='blue')

                # creates a red line that is half the length of the previous blue line to indicate in what direction the connection is
                plt.plot([dep_coords.longitude, dep_coords.longitude + (arr_coords.longitude - dep_coords.longitude) / 2.0],
                         [dep_coords.latitude, dep_coords.latitude + (arr_coords.latitude - dep_coords.latitude) / 2.0],
                         linestyle='-', color='red')

                text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                text_y = (dep_coords.latitude + arr_coords.latitude) / 2
                plt.text(text_x, text_y + 0.002, time, ha='center', va='center', fontsize=8, color='black')

    def set_plot_limits(self, locations):
        """
        Sets the plot limits based on the minimum and maximum latitude and longitude.
        """
        min_lat = min(loc.latitude for loc in locations.values())
        max_lat = max(loc.latitude for loc in locations.values())
        min_lon = min(loc.longitude for loc in locations.values())
        max_lon = max(loc.longitude for loc in locations.values())

        plt.xlim(min_lon - 0.1, max_lon + 0.1)
        plt.ylim(min_lat - 0.1, max_lat + 0.1)
        plt.gca().set_aspect('equal', adjustable='box')

    def main(self):
        """
        Reads all the stations and their coordinates; also reads the connections between stations to make a graph of the connections in between stations similar to a map.
        """
        locations = self.read_locations('data/StationsHolland.csv')
        connections = self.read_connections('data/ConnectiesHolland.csv')

        plt.figure(figsize=(10, 10))
        self.plot_locations(locations, connections)
        self.set_plot_limits(locations)

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Coordinate Grid of Locations in Holland with Connections and Times')

        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    railroad_map = Railroadmap('example', 0.0, 0.0)
    railroad_map.main()