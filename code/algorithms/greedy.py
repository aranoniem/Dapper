import random
from code.classes.load import Load
from code.classes.station import Station
from code.classes.score import Score

class GreedySearch:
    def __init__(self, level, timeframe, max_time, num_colors):
        """
        Retrieves file name, the maximum allowed time per route, and the amount of routes to be made (timeframe),
        also loads in the connections between stations. Initializes a trajectories list to keep track of found trajectories,
        initializes a total time counter for the score calculation, and sets the number of colors for trajectories.
        """
        self.level = level
        self.max_time = max_time
        self.timeframe = timeframe
        self.connections = Load(level).objects
        self.total_time_for_trajectories = 0
        self.trajectories = []

    @classmethod
    def solve(cls, level, timeframe, max_time, num_colors):
        """
        Makes it so the GreedySearch function can be called with GreedySearch.solve(<arguments>) for ease of use.
        """
        instance = cls(level, timeframe, max_time, num_colors)
        instance._solve()
        return instance

    def _solve(self):
        """
        Generates (timeframe) routes and adds the routes to the list of routes.
        """
        for i in range(self.timeframe):
            route = self._generate_route()
            self._update_trajectories(route, i)

        self._calculate_and_print_score()

    def _generate_route(self):
        """
        Picks a random station to start from and then makes a route shorter or equal to 120 min;
        that does not use the same connection twice.
        """
        current_station = self._choose_random_station()
        route = [current_station]
        total_time = 0
        visited_stations = set()

        while total_time <= self.max_time:
            next_station = self._choose_next_station(current_station, visited_stations)

            # If a dead end is reached
            if next_station is None:
                break

            connection_distance = self.connections[current_station].get_distance(next_station)

            if total_time + connection_distance <= self.max_time:
                route.append(next_station)
                total_time += connection_distance
                visited_stations.add(current_station)
                current_station = next_station
            else:
                break

        return route

    def _choose_random_station(self):
        return random.choice(list(self.connections.keys()))

    def _choose_next_station(self, current_station, visited_stations):
        """
        Adds a new station to the route if it's the closest neighbor and the station was not visited previously.
        """
        connections_list = self.connections[current_station].get_connections()
        unvisited_neighbors = [neighbor for neighbor in connections_list if neighbor not in visited_stations]

        # If a dead end is reached
        if not unvisited_neighbors:
            return None

        return min(unvisited_neighbors, key=lambda x: self.connections[current_station].get_distance(x))

    def _update_trajectories(self, route, current_route):
        """
        Update the list of trajectories by appending the new route and color.
        """
        self.total_time_for_trajectories += sum(self._calculate_total_time(route))

        colors = [
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ]

        self.trajectories.append((route, colors[current_route]))
        print(f"Found route {len(self.trajectories)}: {route}")

    def _calculate_total_time(self, route):
        """
        Retrieves the sum of the distances between stations.
        """
        return [self.connections[route[i]].get_distance(route[i + 1]) for i in range(len(route) - 1)]

    def _calculate_and_print_score(self):
        score = Score(self.level, [trajectory[0] for trajectory in self.trajectories], self.total_time_for_trajectories)
        print(score)
