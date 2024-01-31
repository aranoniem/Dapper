
from classes.load import Load

class Score(object):
    """Calculate railnetwork quality score"""

    def __init__(self, level: str, trajectories: list, time: int) -> None:
        """Initialiser"""
        # Load data about tracks
        self.tracks = Load(level).tracks
        self.station = Load(level).objects

        # Initialise set, to prevent duplicates
        self.ridden_tracks: set[str] = set()
        self.calculate_score(trajectories, time)

    def individual_tracks(self, trajectories: list) -> set:
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

        return self.ridden_tracks


    def calculate_score(self, trajectories: list, Min: int) -> float:
        """
        Calculates score of the quality of the railnetwork

        pre: p is between 0 and 1, T and min are integers
        post: returns score as a float
        """
        # Put indivual tracks into set
        self.individual_tracks(trajectories)

        # Calculate p-value
        p = self.calc_p()
        print(f"p:", p)
        # TEST: print(self.ridden_tracks)
        #print("\n")
        #print(f"{self.tracks} , x")
        #print(p)

        # the total amount of minutes in all trajectories
        T = self.calc_T(trajectories)
        print(f"T:", T)
        print(f"Min:", Min)
        # Formula for railnetwork quality
        self.K = p * 10000 - (T*100 + Min)
        print(f"K:", self.K)
        return self.K

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
    
    def __str__(self):
        return f"{self.K}"
        


