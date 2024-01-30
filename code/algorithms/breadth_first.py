# Import algorithms
from .depth_first import Depth_first #. gebruik je omdat het uit dezelfde folder komt. moet ivm main.py vanuit de root.

class Breadth_first(Depth_first):
    
    def get_next_trajectory(self):
        return self.stack.pop(0)
