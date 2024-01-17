from code.classes.load import Load
from code.functions.connections import used_connections
from code.functions.score import Score

def greedy_search(level, max_time, start_station_index, timeframe):
    # Load connections using the provided function
    connections = all_connections(level)

    total_time_for_trajectories = 0
    for i in range(timeframe):
        # Initialize variables
        current_station = random.choice(list(connections.keys()))
        route = [current_station]
        total_time = 0
        visited_stations = set()

        while total_time <= max_time:
            # Find the possible connections to the current station
            connections_list = connections[current_station]

            # Filter out already visited stations
            unvisited_neighbors = [neighbor for neighbor in connections_list if neighbor not in visited_stations]

            # If a dead end is reached
            if not unvisited_neighbors:
                break

            # Choose the next station based on the shortest distance
            next_station = min(unvisited_neighbors, key=lambda x: get_distance(current_station, x))

            # Get the distance for checking if the next station is a valid station
            connection_distance = get_distance(current_station, next_station)

            if total_time + connection_distance <= max_time:
                # Update variables for the next iteration
                route.append(next_station)
                total_time += connection_distance
                visited_stations.add(current_station)  # Mark the current station as visited
                current_station = next_station
            else:
                break  # Break the loop if adding the next station exceeds the time limit
        
        total_time_for_trajectories += total_time        
    return calculate_score(routes, total_time)

# Example usage:
level = 1
result_route, total_time = greedy_search(level, max_time=120, timeframe=5)
print("Greedy Route with Time Constraint (<= 2 hours):", result_route)
print("Total time:", total_time)
