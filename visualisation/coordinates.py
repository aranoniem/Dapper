import csv
import random
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
import geopandas as gpd
import contextily as cx
import os
import sys

sys.path.append('../code')
from algorithms.greedy import GreedySearch
from classes.station import Station

class Railroadmap:
    def __init__(self, level):
        self.level = level
        self.latitude = 0.0
        self.longitude = 0.0
        # stores the offset for x or y for one extra connection.
        # the reason for the offset being different for "Holland" than for "Nationaal" is because "Holland" has a lower density 
        # in connections so with a low offset its still visible
        self.offset_coefficient = 0.008 if level == "Holland" else 0.016

    def read_locations(self):
        """
        read out all the connections from the csv file and store it in a dictionary that has the values mapped by place name
        """
        locations = {}
        with open(f'data/Stations{self.level}.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                name, latitude, longitude = row
                locations[name] = Station(0, name, float(latitude), float(longitude))

        return locations

    def read_connections(self):
        """
        read out all the connection s between stations from the csv file and store the connections in a dictionary mapped by the departure station
        """
        connections = {}

        with open(f'data/Connecties{self.level}.csv', 'r') as csv_file:
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
        
    
    def plot_locations(self, locations, connections, NL_shape):
        connection_offsets = {}
        used_reversed_connections = set()
        
        # set the size of the subplot
        fig, ax = plt.subplots(figsize=(10,10))
        
        # draw the plot of the Netherlands behind the plot of the railnetwork
        NL_shape.plot(ax=ax, alpha=0.3, edgecolor="black", facecolor="white")

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
                
                # If the connection is not part of a route
                if connection not in connections and reversed_connection not in connections:
                    dep_coords = locations[dep_station]
                    arr_coords = locations[dest]

                    # Determine what type of connection "connection" is
                    offset_connection = connection if connection not in connection_offsets else reversed_connection

                    if offset_connection not in connection_offsets:
                        connection_offsets[offset_connection] = 0
                    
                    ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)
                    horizontal_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio <= 1 else 0
                    vertical_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio > 1 else 0

                    # Adjust offsets if reversed connection is used
                    if reversed_connection in used_reversed_connections:
                        connection_offsets[reversed_connection] = max(connection_offsets[reversed_connection], connection_offsets[connection])

                    connection_offsets[offset_connection] += 1

                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset),
                           (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset), color=(0.5, 0.5, 0.5), arrowstyle='-|>', mutation_scale=10)
                    plt.gca().add_patch(line)

                    # Print time for the connection
                    matching_times = [time for dest, time in connections.get(dep_station, []) if dest == dest]
                    non_zero_times = [float(time) for time in matching_times if float(time) > 0]

                    if non_zero_times:
                        current_route_time = non_zero_times[0]
                        text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                        text_y = (dep_coords.latitude + arr_coords.latitude) / 2
                        min_text_distance = 0.002
                        text_y = max(text_y, dep_coords.latitude + min_text_distance)
                        plt.text(text_x, text_y, f"{current_route_time:.2f} mins", ha='center', va='center', fontsize=8, color='black')
        
        # create lists for the labels which store the route number, and for a list that stores the coloured lines that belong to the corresponding route labels
        unique_color_labels = []
        unique_color_lines_list = []  

        # Loop through each trajectory
        for i, route in enumerate(self.trajectories):
            color = self.generate_random_color()

            # Using Line2D library for drawing a line in the color corresponding to the route
            unique_color_labels.append(f'Route {i + 1}')

            # Using Line2D library for drawing a line in the color corresponding to the route
            unique_color_line = Line2D([0], [0], marker='o', color=color, label=unique_color_labels[i], markersize=5)
            unique_color_lines_list.append(unique_color_line)  

            # Loop for all the connections in a route
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
                horizontal_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio <= 1 else 0
                vertical_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio > 1 else 0
                    
                connection_offsets[offset_connection] += 1
                distance = dep_coords.get_distance(arrival_location)

                if not (connection in connections or reversed_connection in connections):
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset), (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset),
                    color=color, arrowstyle='-|>', mutation_scale=15)

                    plt.gca().add_patch(line)

                    # Print time for the connection
                    matching_times = [time for dest, time in connections.get(departure_station, []) if dest == arrival_location]
                    non_zero_times = [float(time) for time in matching_times if float(time) > 0]

                    if non_zero_times:
                        current_route_time = non_zero_times[0]
                        text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                        text_y = (dep_coords.latitude + arr_coords.latitude) / 2
                        min_text_distance = 0.002
                        text_y = max(text_y, dep_coords.latitude + min_text_distance)
                        plt.text(text_x, text_y, f"{current_route_time:.2f} mins", ha='center', va='center', fontsize=8, color='black')

        # Update the legend after the loop with the list of handles
        plt.legend(handles=unique_color_lines_list, loc='lower right')

        # Set the background map 
        cx.add_basemap(ax, crs=NL_shape.crs, source=cx.providers.OpenStreetMap.Mapnik)

    def set_plot_limits(self, locations):
        """
        find and set the edge values of the plot by determining the minimum and maximum latitude and longitude values
        """
        min_lat = min(loc.latitude for loc in locations.values())
        max_lat = max(loc.latitude for loc in locations.values())
        min_lon = min(loc.longitude for loc in locations.values())
        max_lon = max(loc.longitude for loc in locations.values())

        plt.xlim(min_lon - 0.1, max_lon + 0.1)
        plt.ylim(min_lat - 0.1, max_lat + 0.1)
        plt.gca().set_aspect('equal', adjustable='box')

    def main(self, trajectories):
        locations = self.read_locations()
        connections = self.read_connections()

        # stores the path to the shapefile which is used for retrieving the map of the Netherlands
        # shapefile origin: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/
        # sources: https://stackoverflow.com/questions/65110568/how-to-add-a-real-map-as-the-background-to-a-plot, https://contextily.readthedocs.io/en/latest/intro_guide.html
        # https://stackoverflow.com/questions/61436956/set-shape-restore-shx-config-option-to-yes-to-restore-or-create-it
        shapefile_path = 'visualisation/shapefile_for_visualisation/ne_50m_admin_0_countries.shp'

        # Read the shapefile in for plotting it later
        NL_shape = gpd.read_file(shapefile_path)

        self.trajectories = trajectories

        self.plot_locations(locations, connections, NL_shape)
        self.set_plot_limits(locations)

        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.title(f'Coordinate Grid of Locations in {self.level} with Connections and Times')

        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    level = "Nationaal"

    # Replace with your own method to generate trajectories
    trajectories = GreedySearch.solve(level, 7, 120).trajectories

    railroad_map = Railroadmap(level)
    railroad_map.main(trajectories)
