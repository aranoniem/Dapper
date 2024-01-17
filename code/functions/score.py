from track import Tracks

class Score(object):
    """Calculate railnetwork quality score"""

    def __init__(self, level):
        """Initialiser"""
        # Load data about tracks
        self.tracks = Load(level).tracks
        self.station = Load(level).objects

        # Initialise set, to prevent duplicates
        self.ridden_tracks = set()
        self.time = 0

    def individual_tracks(self, trajectories):
        """
        Keep record of individual ridden tracks, without duplicates

        pre: trajectories in the form of a list of lists (eg. [[a, b], [c, d]])
        post: return a set of tuples with the tracks sorted alphabetically
        """
        # Iterate over list of trajectories
        for trajectory in trajectories:

            # Iterate over stations within a trajectory
            for i in range (len(trajectory) - 1):

                # Put station and connecting station together
                journey = (trajectory[i], trajectory[i+1])

                # Create a tuple and sort stations aphabetically
                journey = tuple(sorted(journey))

                # Add tuple to set
                self.ridden_tracks.add(journey)


    def calculate_score(self, trajectories) -> float:
        """
        Calculates score of the quality of the railnetwork

        pre: p is between 0 and 1, T and min are integers
        post: returns score as a float
        """
        # Put indivual tracks into set
        individual_tracks(trajectories)

        # Calculate p-value
        p = self.calc_p(trajectories)

        # Calculate T-value
        T = self.calc_T(trajectories)

        # Calculate time of all trajectories
        Min = self.calc_min(trajectories)

        # Formula for railnetwork quality
        K = p * 10000 - (T*100 + Min)
        return K

    def calc_p(self) -> float:
        """
        Calculates fraction of ridden tracks
        
        post: returns float between 0 and 1
        """
        total_tracks = len(self.tracks)
        number_ridden_tracks = len(self.ridden_tracks)
        return float(number_ridden_tracks / total_tracks)

    def calc_T(self, trajectories) -> int:
        """"
        Calculates total amount of trajectories
        
        post: returns integer
        """
        return len(trajectories)

    def calc_min(self, trajectories) -> int:
        """
        Calculates the total amount of minutes in all trajectories

        post: returns integer
        """
        self.time = 0

         # Iterate over list of trajectories
        for trajectory in trajectories:

            # Iterate over stations within a trajectory
            for i in range (len(trajectory) - 1):
                departure_station = trajectory[i]
                arrival_station = trajectory[i+1]
                minutes = departure_station.get_distance(arrival_station)
                self.time += minutes


