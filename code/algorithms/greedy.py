from code.classes.load import Load
from code.functions.connections import used_connections

def greedy_search(level, max_time=120, start_station_index):
    # Load connections using the provided function
    connections = all_connections(level)

    # Check if start_station_index is out of bounds
    if start_station_index < 0 or start_station_index >= len(connections):
        print("Invalid start_station_index. Must be between 0 and", len(connections) - 1)
        return None, 0

    # Initialize variables
    current_station = list(connections.keys())[start_station_index]
    route = [current_station]
    total_time = 0

    while total_time <= max_time:
        # Find the possible connections to the current station
        connections_list = connections[current_station]

        # Filter out already visited stations
        unvisited_neighbors = [neighbor for neighbor in connections_list if not used_connections(neighbor)]

        # If a dead end is reached
        if not unvisited_neighbors:
            break

        # Choose the next station based on the shortest distance
        next_station = min(unvisited_neighbors, key=lambda x: get_distance(current_station, x))

        # Get the distance for checking for if the next station is a valid station
        connection_distance = get_distance(current_station, next_station)

        if total_time + connection_distance <= max_time:
            # Update variables for the next iteration
            route.append(next_station)
            total_time += connection_distance
            current_station = next_station
        else:
            break  # Break the loop if adding the next station exceeds the time limit

    return route, total_time

# Example usage:
level = 1
result_route, total_time = greedy_search(level, max_time=120, start_station_index=5)
if result_route is not None:
    print("Greedy Route with Time Constraint (<= 2 hours):", result_route)
    print("Total time:", total_time)

# Example usage:
level = 1
result_route, total_time = greedy_search(level, max_time=120)
print("Greedy Route with Time Constraint (<= 2 hours):", result_route)
print("Total time:", total_time)