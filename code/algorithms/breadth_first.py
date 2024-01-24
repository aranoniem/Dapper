# Import algorithms
from .depth_first import DepthFirst #. gebruik je omdat het uit dezelfde folder komt. moet ivm main.py vanuit de root.

class BreadthFirst(DepthFirst):
    
    def get_next_station(self):
        return self.stack.pop(0)
