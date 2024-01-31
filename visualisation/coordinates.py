from __future__ import annotations
from typing import Dict, List, Tuple

import csv
import random
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
import geopandas as gpd
import contextily as cx

sys.path.append('../code')
from classes.station import Station


class Railroadmap:
    def __init__(self, level: str) -> None:
        """
        Initialize a Railroadmap object with the specified level.

        Post: returns None
        """

        self.level: str = level
        self.latitude: float = 0.0
        self.longitude: float = 0.0
        # stores the offset for latitude or longitude for one extra connection.
        self.offset_coefficient: float = 0.008 if level == "Holland" else 0.018

    def read_locations(self) -> Dict[str, Station]:
        """
        Read station locations from a CSV file and return a dictionary of
        Station objects.

        Post: returns Dict[str, Station]: Dictionary of station names and
        corresponding Station objects.
        """
        locations: Dict[str, Station] = {}
        with open(f'data/Stations{self.level}.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            # retrieve the station object from the current row
            for row in csv_reader:
                name, latitude, longitude = row
                locations[name] = Station(0, name, float(latitude),
                                          float(longitude))

        return locations

    def read_connections(self) -> Dict[str, List[Tuple[str, float]]]:
        """
        Read connections from a CSV file and return a dictionary
        of departure stations and their connections.

        Post: returns Dict[str, List[Tuple[str, float]]]: Dictionary
        of departure stations and their connections.
        """
        connections: Dict[str, List[Tuple[str, float]]] = {}

        with open(f'data/Connecties{self.level}.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header line

            for row in csv_reader:
                if len(row) < 3:
                    continue  # Skip incomplete lines

                departure_station, arrival_station, time = row
                time = float(time)

                if departure_station not in connections:
                    connections[departure_station] = []

                connections[departure_station].append((arrival_station, time))

        return connections

    def generate_random_color(self) -> List[float]:
        """
        generates a 3 element list with random red green blue values

        Post: returns a 3 elemnt list of random value floats
        """
        return [random.random(), random.random(), random.random()]

    def plot_locations(self, locations: Dict[str, Station],
                       connections: Dict[str, List[Tuple[str, float]]],
                       NL_shape: gpd.GeoDataFrame) -> None:
        """
        Plot the locations, connections, and trajectories on a map.

        Post: returns None
        """
        connection_offsets: Dict[Tuple[str, str], int] = {}
        used_reversed_connections: set[Tuple[str, str]] = set()

        # Create a new plot
        fig, ax = plt.subplots(figsize=(10, 10))

        # Plot the geographical shape with a low alpha to act as a background
        NL_shape.plot(ax=ax, alpha=0.3, edgecolor="black", facecolor="white")

        # Plot stations as red dots
        plt.scatter([loc.longitude for loc in locations.values()],
                    [loc.latitude for loc in locations.values()],
                    marker='o', color='red')

        # Offset lists to prevent station names from overlapping
        name_offsets_latitude: List[float] = []
        name_offsets_longitude: List[float] = []

        # Define offsets based on the level
        if self.level == "Holland":
            name_offsets_latitude = [0, 0, 0.1125, 0.225, 0.1, 0.25, 0, 0,
                                     0, 0, 0, 0, 0.075, 0, 0, 0, 0, 0.2,
                                     0.15, -0.015, 0, 0]
            name_offsets_longitude = [0, 0, -0.035, -0.02, 0.018, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.035,
                                      0, 0, 0]
        elif self.level == "Nationaal":
            name_offsets_latitude = [0, 0, 0.35, 0.3, 0.2, -0.35, -0.3,
                                     -0.29, 0, 0, 0.45, 0, -0.03, 0, 0,
                                     -0.1, 0, 0, 0, 0, 0, 0, 0, 0.2, 0,
                                     0.075, 0.12, 0, 0, -0.05, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0.5, -0.15, -0.15, 0, 0.2, 0, 0,
                                     0, 0.225, 0, 0, 0, 0, 0, 0, 0]

            name_offsets_longitude = [0, 0, 0, 0, 0.05, 0.01, 0.07, 0.02, 0,
                                      0, -0.06, 0, 0.025,0, 0, 0.02, 0.07,
                                      0, 0.04, 0, 0, 0, 0, 0.04, 0, -0.035,
                                      -0.075, 0, 0, -0.0035, -0.05, 0, 0, 0,
                                      0, 0, 0, 0, 0.05, 0, 0, 0, 0, 0, 0,
                                      -0.05, -0.01, 0.04, -0.075, -0.085, 0,
                                      0, 0, -0.1, 0, 0, 0, 0.25, 0, 0, 0]

        # Print all the station names with hardcoded offsets applied
        current_index = 0
        for loc in locations.values():
            plt.text(loc.longitude + name_offsets_latitude[current_index],
                     loc.latitude + name_offsets_longitude[current_index],
                     loc.name, ha='right', va='bottom', fontsize=8)
            current_index += 1

        for dep_station, destinations in connections.items():
            for dest, time in destinations:
                connection = (dep_station, dest)
                reversed_connection = (dest, dep_station)

                # if the reversed connection was previously used
                if reversed_connection in used_reversed_connections:
                    used_reversed_connections.add(reversed_connection)

                # check if the connection is already registered
                if connection not in connections and reversed_connection not in connections:
                    dep_coords = locations[dep_station]
                    arr_coords = locations[dest]

                    offset_connection = connection if connection not in connection_offsets else reversed_connection

                    if offset_connection not in connection_offsets:
                        connection_offsets[offset_connection] = 0

                    # determine if the connection is more 
                    # horizontal or vertical
                    ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)

                    # adjust the offset accordingly
                    horizontal_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio <= 1 else 0
                    vertical_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio > 1 else 0

                    if reversed_connection in used_reversed_connections:
                        connection_offsets[reversed_connection] = max(connection_offsets[reversed_connection], connection_offsets[connection])

                    connection_offsets[offset_connection] += 1

                    # Draw a line with an arrow between departure
                    # and arrival coordinates
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset),
                                        (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset), color=(0.5, 0.5, 0.5), arrowstyle='-|>', mutation_scale=10)
                    plt.gca().add_patch(line)

                    # Extract matching times for the connection
                    matching_times = [time for dest, time in
                                      connections.get(dep_station, []) if dest == dest]
                    non_zero_times = [time for time in matching_times if time > 0]

                    # print the time for the corresponding connection
                    if non_zero_times:
                        current_route_time = non_zero_times[0]
                        text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                        text_y = (dep_coords.latitude + arr_coords.latitude) / 2
                        min_text_distance = 0.002
                        text_y = max(text_y, dep_coords.latitude + min_text_distance)
                        plt.text(text_x, text_y, int(current_route_time),
                                 ha='center', va='center', fontsize=8, color='black')

        # create lists to store the labels and their corresponding colors
        unique_color_labels = []
        unique_color_lines_list = []

        # Plot trajectories with unique colors and add labels
        for i, route in enumerate(self.trajectories):
            color = self.generate_random_color()

            unique_color_labels.append(f'Route {i + 1}')

            # create a custom label for the corresponding line
            unique_color_line = Line2D([0], [0], marker='o', color=color,
                                label=unique_color_labels[i], markersize=5)
            unique_color_lines_list.append(unique_color_line)

            # for all connections in the route
            for j in range(len(route) - 1):
                departure_station = route[j]
                arrival_location = route[j + 1]
                dep_coords = locations[departure_station]
                arr_coords = locations[arrival_location]

                connection = (departure_station, arrival_location)
                reversed_connection = (arrival_location, departure_station)

                # check if the connections was previously used
                offset_connection = connection if connection in connection_offsets else reversed_connection

                if offset_connection not in connection_offsets:
                    connection_offsets[offset_connection] = 0

                # determine if the connection is more
                # horizontal or vertical
                ratio = (arr_coords.longitude - dep_coords.longitude) / (arr_coords.latitude - dep_coords.latitude)

                # adjust the offset accordingly
                horizontal_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio <= 1 else 0
                vertical_offset = self.offset_coefficient * connection_offsets[offset_connection] if ratio > 1 else 0

                # new connection counted so update the offset list
                connection_offsets[offset_connection] += 1

                if not (connection in connections or reversed_connection in connections):
                    # Draw a line with an arrow between departure
                    # and arrival coordinates for trajectories
                    line = FancyArrowPatch((dep_coords.longitude + horizontal_offset, dep_coords.latitude + vertical_offset), (arr_coords.longitude + horizontal_offset, arr_coords.latitude + vertical_offset),
                                        color=color, arrowstyle='-|>', mutation_scale=15)

                    plt.gca().add_patch(line)

                    # Extract matching times for the trajectory
                    matching_times = [time for dest, time in connections.get(departure_station, []) if dest == arrival_location]
                    non_zero_times = [time for time in matching_times if time > 0]

                    # print the time for the corresponding connection
                    if non_zero_times:
                        current_route_time = non_zero_times[0]
                        text_x = (dep_coords.longitude + arr_coords.longitude) / 2
                        text_y = (dep_coords.latitude + arr_coords.latitude) / 2
                        min_text_distance = 0.002
                        text_y = max(text_y, 
                                 dep_coords.latitude + min_text_distance)
                        plt.text(text_x, text_y, int(current_route_time), 
                                 ha='center', va='center', fontsize=8, color='black')

        # Display a legend for unique trajectory routes
        plt.legend(handles=unique_color_lines_list, loc='lower right')

        # Add a basemap for additional context
        cx.add_basemap(ax, crs=NL_shape.crs,
                       source=cx.providers.OpenStreetMap.Mapnik)

    def set_plot_limits(self, locations: Dict[str, Station]) -> None:
        """
        Set plot limits for the current map based on the minimum and maximum latitude and longitude of locations.

        Post: returns None
        """

        # find the minimum and maximum longitude and latitude values
        min_lat = min(loc.latitude for loc in locations.values())
        max_lat = max(loc.latitude for loc in locations.values())
        min_lon = min(loc.longitude for loc in locations.values())
        max_lon = max(loc.longitude for loc in locations.values())

        # set the plot limits
        plt.xlim(min_lon - 0.1, max_lon + 0.1)
        plt.ylim(min_lat - 0.1, max_lat + 0.1)
        plt.gca().set_aspect('equal', adjustable='box')

    def main(self, trajectories: List[List[str]]) -> None:
        """
        Main function to visualize the railroad map with trajectories.

        Post: returns None
        """
        # read the locations and connections for plotting
        locations = self.read_locations()
        connections = self.read_connections()

        # set the shapefile path
        shapefile_path = 'visualisation/shapefile_for_visualisation/ne_50m_admin_0_countries.shp'

        # read the shapefile for plotting it later
        NL_shape = gpd.read_file(shapefile_path)

        # retrieve the trajectories list of lists
        self.trajectories = trajectories

        # plot the stations connections and trajectories
        self.plot_locations(locations, connections, NL_shape)
        self.set_plot_limits(locations)

        # set the plot labels
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.title(f'Coordinate grid of locations in {self.level} with connections and travel times')

        plt.grid(True)
