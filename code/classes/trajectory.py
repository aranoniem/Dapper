import random

class Trajectory:
    def random_station(self):
        """
        find a random station for the purpose of a starting point

        post: returns a random station
        """
        random_station = random.choice(list(self.stations.keys()))
        #TEST STATEMENT print(f'start station = {random_station}')
        return random_station

    def random_connection(self, departure_station):
        """
        find a random connection for the purpose of making a trajectory

        pre: enter a departure station
        post: returns a station connected with the departure station 
        """
        neighbours = list(self.stations[departure_station].get_connection())
        #TEST STATEMENT print(f'Connecties zijn: {neighbours}')

        #TEST STATEMENT print(f'aantal buren: {len(neighbours)}')

        if len(neighbours) > 1:
            random_index = random.randint(1, len(neighbours))
            #TEST STATEMENT print(random_index)
            random_neighbour = neighbours[random_index - 1]
            #TEST STATEMENT print(random_neighbour)
        else:
            random_neighbour = neighbours[0]
        return random_neighbour
    
    def generate_trajectory(self):
        """
        generate a trajectory based on hopping through stations
        that are connected based on randomness

        post: returns a list of connected stations
        """
        # Initialize an empty list for a trajectory
        trajectory = []

        # Choose a random starting station
        _station = self.random_station()
        #TEST STATEMENT print(_station)
        trajectory.append(_station)

        for i in range(5):
            i = i + 1
            new_station = self.random_connection(_station)
            trajectory.append(new_station)
            _station = new_station
            
        return trajectory
