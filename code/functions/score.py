# TODO berekenen score
# Een lijst met lijsten

from track import Tracks

class Score():

    def __init__(self, level, trajectories):
        self.trajectories = trajectories
        self.calculate_score()

    def calculate_score(self, p, T, min) -> float:
        """
        Calculates score of the quality of the railnetwork

        pre: p is between 0 and 1, T and min are integers
        post: returns score as a float
        """
        K = p * 10000 - (T*100 + Min)
        return K

    def calc_p(self) -> float:
        """
        Calculates fraction of ridden tracks
        
        post: returns float between 0 and 1
        """
        pass

    def calc_T(self) -> int:
        """"
        Calculates total amount of trajectories
        
        post: returns integer
        """
        pass

    def calc_min(self) -> int:
        """
        Calculates the total amount of minutes in all trajectories

        post: returns integer
        """
        pass
