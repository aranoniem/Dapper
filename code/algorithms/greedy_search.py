from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score
from code.functions.elements import get_random_station

class Greedy_search:
    def __init__(self, level):
        """
        Retrieves file name and loads in the connections between stations.
        Initializes a trajectories list to keep track of found trajectories,
        initializes a total time counter for the score calculation,
        and sets the number of colors for trajectories.
        """
        self.level = level
        self.connections = Load(level).objects
        self.total_time_for_trajectories = 0
        self.trajectories = []

    def solve(self, max_trajectories, timeframe):
        """
        Generates (max_trajectories) number of routes and adds the routes to the list of routes.

        pre: amount of trajectories, amount of time for one trajectory
        post: qualityscore (K) and all trajectories (lists in a list)
        """

        for i in range(max_trajectories):
            route = self.generate_trajectory(timeframe)
            self.trajectories.append(route)
            self.update_trajectories(route)

        score = Score(self.level, self.trajectories, self.total_time_for_trajectories)
        print(float(score.K))
        return (float(score.K), self.trajectories)

    def generate_trajectory(self, timeframe):
        """
        Picks a random station to start from and then makes a route shorter or equal to timeframe;
        that does not use the same connection twice.
        """
        current_station = get_random_station(self.connections)
        route = [current_station]
        total_time = 0
        visited_stations = set()

        while total_time <= timeframe:
            next_station = self.choose_next_station(current_station, visited_stations)

            # If a dead end is reached
            if next_station is None:
                break

            connection_distance = self.connections[current_station].get_distance(next_station)

            if total_time + connection_distance <= timeframe:
                route.append(next_station)
                total_time += connection_distance
                visited_stations.add(current_station)
                current_station = next_station
            else:
                break

        return route

    def choose_next_station(self, current_station, visited_stations):
        """
        Adds a new station to the route if it's the closest neighbor and the station was not visited previously.
        """
        connections_list = self.connections[current_station].get_connections()
        unvisited_neighbors = [neighbor for neighbor in connections_list if neighbor not in visited_stations]

        # If a dead end is reached
        if not unvisited_neighbors:
            return None

        return min(unvisited_neighbors, key=lambda x: self.connections[current_station].get_distance(x))

    def update_trajectories(self, route):
        """
        Update the list of trajectories by appending the new route and color.
        """
        self.total_time_for_trajectories += sum(self.calculate_total_time(route))

        print(f"Found route {len(self.trajectories)}: {route}")

    def calculate_total_time(self, route):
        """
        Retrieves the sum of the distances between stations.
        """
        return [self.connections[route[i]].get_distance(route[i + 1]) for i in range(len(route) - 1)]
