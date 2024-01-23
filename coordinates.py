import csv
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from code.algorithms.greedy import GreedySearch
from code.classes.load import Load
from code.classes.station import Station

class Railroadmap:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connections = []  # List to store connected locations
        self.trajectories = []  # List to store trajectories

    def read_locations(self, file_path):
        locations = {}
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                name, latitude, longitude = row
                locations[name] = Station(0, name, float(latitude), float(longitude))

        return locations

    def read_connections(self, file_path):
        connections = {}

        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                if len(row) < 3:
                    continue  # Skip incomplete lines

                departure_station, arrival_station, time = row
                time = float(time)  # Convert time to float if it's not already

                if departure_station not in connections:
                    connections[departure_station] = []

                connections[departure_station].append((arrival_station, time))

        return connections

    def plot_locations(self, locations, connections, selected_route, made_connections):
        plt.scatter([loc.longitude for loc in locations.values()], [loc.latitude for loc in locations.values()], marker='o', color='red')
    
        for loc in locations.values():
            plt.text(loc.longitude, loc.latitude, loc.name, ha='right', va='bottom', fontsize=8)
    
        route_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
        route_offset = 0.15
    
        for i, (route, color) in enumerate(self.trajectories):
            if i == selected_route:
                for j in range(len(route) - 1):
                    departure_station = route[j]
                    arrival_location = route[j + 1]
    
                    # Ensure departure_station is a string
                    if isinstance(departure_station, list):
                        departure_station = departure_station[0]
    
                    # Ensure arrival_location is a string
                    if isinstance(arrival_location, list):
                        arrival_location = arrival_location[0]
    
                    dep_coords = locations[departure_station]
                    arr_coords = locations[arrival_location]
    
                    # Introduce an offset based on the route index
                    offset = i * route_offset
    
                    if (departure_station, arrival_location) in made_connections:
                        line = FancyArrowPatch((dep_coords.longitude + offset, dep_coords.latitude),
                            (arr_coords.longitude + offset, arr_coords.latitude),
                            color='black', arrowstyle='-|>', mutation_scale=15)
                    else:
                        line = FancyArrowPatch((dep_coords.longitude + offset, dep_coords.latitude),
                            (arr_coords.longitude + offset, arr_coords.latitude),
                            color=color, arrowstyle='-|>', mutation_scale=15)
    
                    plt.gca().add_patch(line)
    
                    text_x = (dep_coords.longitude + arr_coords.longitude) / 2 + offset
                    text_y = (dep_coords.latitude + arr_coords.latitude) / 2
    
                    # Retrieve the correct travel time for the current route using get_distance
                    current_route_time = connections[departure_station].get_distance(arrival_location)
    
                    plt.text(text_x, text_y + 0.002, f"{current_route_time:.2f} mins", ha='center', va='center', fontsize=8, color='black')

    def set_plot_limits(self, locations):
        min_lat = min(loc.latitude for loc in locations.values())
        max_lat = max(loc.latitude for loc in locations.values())
        min_lon = min(loc.longitude for loc in locations.values())
        max_lon = max(loc.longitude for loc in locations.values())

        plt.xlim(min_lon - 0.1, max_lon + 0.1)
        plt.ylim(min_lat - 0.1, max_lat + 0.1)
        plt.gca().set_aspect('equal', adjustable='box')

    def main(self, level):
        # Use Load class to load stations, connections, and tracks
        loader = Load(level)
        
        # Access the loaded stations and connections
        locations = loader.objects
        connections = loader.load_connections(f'data/Connecties{level}.csv')  # Corrected assignment
        
        # Modify this part to use GreedySearch
        num_colors = 7  
        greedy_search = GreedySearch.solve(level, 7, 120, num_colors)  # Adjust 'your_level' accordingly
        self.trajectories = greedy_search.trajectories
        
        plt.figure(figsize=(10, 10))
        selected_route = 0  # Change this to the index of the route you want to display
        
        # Access made connections from the Load instance
        made_connections = loader.load_connections(f'data/Connecties{level}.csv')  
        
        self.plot_locations(locations, connections, selected_route, made_connections)
        self.set_plot_limits(locations)
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Coordinate Grid of Locations in Holland with Connections and Times')
        
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    railroad_map = Railroadmap('example', 0.0, 0.0)
    railroad_map.main("Holland")
