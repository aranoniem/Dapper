#import libraries
import pandas as pd


def all_connections(level):
    """
    Establish simple dictionary of connections

    pre: part of filename of the data
    post: returns a dictionary with departure stations (station1) as keys
    and arrival stations as values (station2)
    """
    pass

def get_distance():
    # uit het station halen
    pass

def used_connections(trajectory):
    """
    Keeps track of 'ridden' connections

    pre: trajectory to check and add to list
    post: bool
    """
    trajectories = []

    if trajectory in trajectories:
        return True
    trajectories.append(trajectory)
    return True

