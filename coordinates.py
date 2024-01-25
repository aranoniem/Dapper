import csv
import sys
import os
import random
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D

sys.path.append('code')
from code.algorithms.greedy import GreedySearch
from code.classes.station import Station

class Railroadmap:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connections = []  # List to store connected locations
        self.trajectories = []  # List to store trajectories
        self.color_list = []

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
    
    def generate_random_color(self):
        """
        Generates a random RGB color.
        """
        return [random.random(), random.random(), random.random()]
    
    def plot_locations(self, locations, connections):
        connection_offsets = {}
        used_reversed_connections = set()
    
        plt.scatter([loc.longitude for loc in locations.values()], [loc.latitude for loc in locations.values()], marker='o', color='red')
    
        for loc in locations.values():
            plt.text(loc.longitude, loc.latitude, loc.name, ha='right', va='bottom', fontsize=8)
    
        # Draw lines for connections that are not part of any route
        for dep_station, destinations in connections.items():
            for dest, time in destinations:
                connection = (dep_station, dest)
                reversed_connection = (dest, dep_station)
    
                # Check if the reversed connection is used
                if reversed_connection in used_reversed_connections:
                    used_reversed_connections.add(reversed_connection)
    
                if connection not in self.connections and reversed_connection not in self.connections:
                    dep_coords = locations[dep_station]
                    arr_coords = locations[dest]
    
                    # Adjust offsets if reversed connection is used
                    offset_connection = connection if connection not in connection_offsets else reversed_connection
    
                    if offset_connection not in connection_offsets:
                        connection_offsets[offset_connection] = 0
    
                    ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)
                    horizontal_offset = 0.008 * connection_offsets[offset_connection] if ratio <= 1 else 0
                    vertical_offset = 0.008 * connection_offsets[offset_connection] if ratio > 1 else 0
    
                    # Adjust offsets if reversed connection is used
                    if reversed_connection in used_reversed_connections:
                        connection_offsets[reversed_connection] = max(connection_offsets[reversed_connection], connection_offsets[connection])
    
                    connection_offsets[offset_connection] += 1
    
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset),
                                            (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset),
                                            color=(0.5, 0.5, 0.5), arrowstyle='-|>', mutation_scale=10)
                    plt.gca().add_patch(line)
    
        # loop through each trajectory
        for i, route in enumerate(self.trajectories):
            color = self.generate_random_color()
    
            # loop for all the connections in a route
            for j in range(len(route) - 1):
                departure_station = route[j]
                arrival_location = route[j + 1]
                dep_coords = locations[departure_station]
                arr_coords = locations[arrival_location]
    
                connection = (departure_station, arrival_location)
                reversed_connection = (arrival_location, departure_station)
    
                offset_connection = connection if connection in connection_offsets else reversed_connection
    
                if offset_connection not in connection_offsets:
                    connection_offsets[offset_connection] = 0
    
                ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)
                horizontal_offset = 0.008 * connection_offsets[offset_connection] if ratio <= 1 else 0
                vertical_offset = 0.00 * connection_offsets[offset_connection] if ratio > 1 else 0
    
                connection_offsets[offset_connection] += 1
    
                distance = dep_coords.get_distance(arrival_location)
    
                if not (connection in connections or reversed_connection in connections):
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset),
                                            (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset),
                                            color=color, arrowstyle='-|>', mutation_scale=15)
    
                    plt.gca().add_patch(line)
    
                text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                text_y = (dep_coords.latitude + arr_coords.latitude) / 2
    
                min_text_distance = 0.002
                text_y = max(text_y, dep_coords.latitude + min_text_distance)
    
                matching_times = [time for dest, time in connections.get(departure_station, []) if dest == arrival_location]
    
                non_zero_times = [float(time) for time in matching_times if float(time) > 0]
    
                if non_zero_times:
                    current_route_time = non_zero_times[0]
                    plt.text(text_x, text_y, f"{current_route_time:.2f} mins", ha='center', va='center', fontsize=8,
                            color='black')
    
        # Combine legend labels for routes and unique colors with corresponding colors
        unique_color_labels = [f'Route {i + 1}' for i in range(len(self.trajectories))]
    
        # using Line2D library for drawing a line in the color corresponding to the route
        unique_color_patches = [Line2D([0], [0], marker='o', color=color, label=label, markersize=5) for color, label in zip([self.generate_random_color() for route in self.trajectories], unique_color_labels)]
        plt.legend(handles=unique_color_patches, loc='lower right')
    
        plt.show()
        
    def set_plot_limits(self, locations):
        min_lat = min(loc.latitude for loc in locations.values())
        max_lat = max(loc.latitude for loc in locations.values())
        min_lon = min(loc.longitude for loc in locations.values())
        max_lon = max(loc.longitude for loc in locations.values())

        plt.xlim(min_lon - 0.1, max_lon + 0.1)
        plt.ylim(min_lat - 0.1, max_lat + 0.1)
        plt.gca().set_aspect('equal', adjustable='box')

    def main(self):
        locations = self.read_locations('data/StationsNationaal.csv')
        connections = self.read_connections('data/ConnectiesNationaal.csv')
    
        num_colors = 20  # Number of different colors for trajectories
        greedy_search = GreedySearch.solve('Nationaal', 20, 120)
    
        trajectories = greedy_search.trajectories
    
        self.trajectories = trajectories
    
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
