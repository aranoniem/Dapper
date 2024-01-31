# Import algorithms
from .depth_first import Depth_first


class Breadth_first(Depth_first):
    """
    A Depth First algorithm that builds a queue of connections for each
    assignment, to a maximum of time.

    Almost all the functions are identical to DepthFirst, which is
    why we use that as a parent class
    """
    def get_next_trajectory(self):
        return self.stack.pop(0)
