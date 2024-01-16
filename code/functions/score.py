# TODO berekenen score
# Een lijst met lijsten

class Score():

    def __init__(self, map, routes):
        self.routes = routes #X!
        self.calculate_score()

    def calculate_score(self, p, T, min) -> float:
        K = p * 10000 - (T*100 + Min)
        return K
