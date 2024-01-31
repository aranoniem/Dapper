from typing import Any
from random import choice

def get_random_station(data):
    """
    Find a random station from all stations

    pre: data that a random station is picked from
    post: returns one station
    """
    return choice(list(data))