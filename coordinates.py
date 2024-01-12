import csv
import matplotlib.pyplot as plt

# Read station coordinates from StationsHolland.csv
stations = {}
with open('StationsHolland.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header line

    for row in csv_reader:
        station, latitude, longitude = row
        stations[station] = {'latitude': float(latitude), 'longitude': float(longitude)}

# Read edges from ConnectiesHolland.csv
connections = {}
times = {}

with open('ConnectiesHolland.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header line

    for row in csv_reader:
        if len(row) < 3:
            continue  # Skip incomplete lines

        departure_station, arrival_station, time = row

        # Add the connection to the dictionary
        if departure_station not in connections:
            connections[departure_station] = []
            times[departure_station] = []
            
        connections[departure_station].append(arrival_station)
        times[departure_station].append(time)

# Find minimum and maximum coordinates
min_lat = min(station['latitude'] for station in stations.values())
max_lat = max(station['latitude'] for station in stations.values())
min_lon = min(station['longitude'] for station in stations.values())
max_lon = max(station['longitude'] for station in stations.values())

# Create a coordinate grid
plt.figure(figsize=(10, 10))
plt.scatter([station['longitude'] for station in stations.values()], [station['latitude'] for station in stations.values()], marker='o', color='red')

# print names for each station
for station, coords in stations.items():
    plt.text(coords['longitude'], coords['latitude'], station, ha='right', va='bottom', fontsize=8)

# Set axis based on mix and max longitude and latitude
plt.xlim(min_lon - 0.1, max_lon + 0.1)
plt.ylim(min_lat - 0.1, max_lat + 0.1)

# Same aspect ratio to prevent the image from looking distorted
plt.gca().set_aspect('equal', adjustable='box')

# Draw lines between connected stations and their corresponding travel times
for departure_station, connected_stations in connections.items():
    dep_coords = stations[departure_station]
    for i, arrival_station in enumerate(connected_stations):
        arr_coords = stations[arrival_station]
        plt.plot([dep_coords['longitude'], arr_coords['longitude']], [dep_coords['latitude'], arr_coords['latitude']], linestyle='-', color='blue')
        
        # line to indicate from where the train departs
        plt.plot([dep_coords['longitude'], dep_coords['longitude'] + (arr_coords['longitude'] - dep_coords['longitude'])/2.0],
        [dep_coords['latitude'], dep_coords['latitude'] + (arr_coords['latitude'] - dep_coords['latitude'])/2.0], linestyle='-', color='red')

        
        # print the length of the route in minutes of each route
        time = times[departure_station][i]
        text_x = (dep_coords['longitude'] + arr_coords['longitude']) / 2
        text_y = (dep_coords['latitude'] + arr_coords['latitude']) / 2
        plt.text(text_x, text_y + 0.002, time, ha='center', va='center', fontsize=8, color='black')

# Add labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Coordinate Grid of Stations in Holland with Connections and Times')

# Show the plot
plt.grid(True)
plt.show()
