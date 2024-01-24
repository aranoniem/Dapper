import csv
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from code.algorithms.greedy import GreedySearch
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

    def plot_locations(self, locations, connections, made_connections):
        connection_offsets = {}
    
        plt.scatter([loc.longitude for loc in locations.values()], [loc.latitude for loc in locations.values()], marker='o', color='red')
    
        for loc in locations.values():
            plt.text(loc.longitude, loc.latitude, loc.name, ha='right', va='bottom', fontsize=8)
        
        # loop through each trajectory 
        for(route, color) in enumerate(self.trajectories):
            # loop for all the connections in a route
            for i in range(len(route) - 1):
                departure_station = route[i]
                arrival_location = route[i + 1]
                dep_coords = locations[departure_station]
                arr_coords = locations[arrival_location]
                
                # check if a connection has already made in reverse or normal order so the arrows can be offset to eachother.
                connection = (departure_station, arrival_location)
                reversed_connection = (arrival_location, departure_station)
    
                # Choose the appropriate connection for offset tracking
                offset_connection = connection if connection in connection_offsets else reversed_connection
    
                if offset_connection not in connection_offsets:
                    connection_offsets[offset_connection] = 0
    
                # determine the ratio to make the line offset for x and y based on if the line is more vertically aligned or horizontally
                ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)
                
                # determine the offset for x and y based on if the line is more horizontally algined or vertically
                horizontal_offset = 0.008 * connection_offsets[offset_connection] if ratio <= 1 else 0
                vertical_offset = 0.008 * connection_offsets[offset_connection] if ratio > 1 else 0
                
                # increment the offset count to offset the next arrow with the same connection by the right amount
                connection_offsets[offset_connection] += 1  
    
                # Calculate and print the distance for the current connection only once
                distance = dep_coords.get_distance(arrival_location)
                
                # draw a black line if the connection is not used(doesnt work yet) else draw a coloured line with an x or y offset determined by what route it is
                if connection in made_connections or reversed_connection in made_connections:
                    line = FancyArrowPatch((dep_coords.longitude, dep_coords.latitude),
                        (arr_coords.longitude, arr_coords.latitude),
                        color='black', arrowstyle='-|>', mutation_scale=10)
                else:
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset),
                        (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset),
                        color=color, arrowstyle='-|>', mutation_scale=15)
    
                plt.gca().add_patch(line)
    
                text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                text_y = (dep_coords.latitude + arr_coords.latitude) / 2
    
                # Ensure a minimum non-zero distance for the text
                min_text_distance = 0.002
                text_y = max(text_y, dep_coords.latitude + min_text_distance)
    
                # Retrieve the correct travel time for the current route
                matching_times = [time for dest, time in connections.get(departure_station, []) if dest == arrival_location]
    
                # Check if there's at least one non-zero travel time for the connection
                non_zero_times = [float(time) for time in matching_times if float(time) > 0]
    
                if non_zero_times:
                    current_route_time = non_zero_times[0]
                    # Print the time if available
                    plt.text(text_x, text_y, f"{current_route_time:.2f} mins", ha='center', va='center', fontsize=8, color='black')
    
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
        locations = self.read_locations('data/StationsHolland.csv')
        connections = self.read_connections('data/ConnectiesHolland.csv')

        num_colors = 7  # Number of different colors for trajectories
        greedy_search = GreedySearch.solve('Holland', 7, 120, num_colors) 

        self.trajectories = greedy_search.trajectories

        plt.figure(figsize=(10, 10))
        self.plot_locations(locations, connections, [(("Delft", "Den Haag Centraal"), 13)])
        self.set_plot_limits(locations)

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Coordinate Grid of Locations in Holland with Connections and Times')

        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    railroad_map = Railroadmap('example', 0.0, 0.0)
    railroad_map.main()