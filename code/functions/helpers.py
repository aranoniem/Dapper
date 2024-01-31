from typing import Any

def get_user_input() -> Any:
    """
    Get input from user needed to run algorithms and create a railnetwork

    post: returns algorithmname, filename, number max amount of trajectories,
    integer timeframe, integer iterations, integer max_iterations
    """
    algorithm_choice: str = get_algorithm()
    level_name: str = get_level()
    trajectories: int = get_max_trajectories()
    timeframe: int = get_timeframe()
    iterations: int = get_iterations()
    if algorithm_choice in ['hillclimber', 'local_search']:
        max_iterations: Any = get_max_iterations()
    else:
        max_iterations = None

    return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations

def get_algorithm() -> str:
    """
    Get algorithm from user

    post: returns algorithm of choice
    """
    # Prompt user for input
    algorithm_choice: Any = input("What algorithm do you want to run? (totally_random, semi_random, greedy_search, breadth_first, depth_first, hillclimber or local_search): ").lower()

    # Check if algorithm is among correct ones, prompt user again if not
    while algorithm_choice not in ['totally_random', 'semi_random', 'greedy_search', 'breadth_first', 'depth_first', 'hillclimber', 'local_search']:
        print("Invalid algorithm choice. Please choose a valid algorithm.")
        algorithm_choice = input("What algorithm do you want to run? (totally_random, semi_random, greedy_search, breadth_first, depth_first, hillclimber or local_search): ").lower()
    return algorithm_choice

def get_level() -> str:
    """
    Get level from user

    post: returns filename as a string
    """
    # Prompt user for input
    level_name: Any = input("Enter the level name (Nationaal or Holland): ").lower()

    # Check if level is among correct ones, prompt user again if not
    while level_name.lower() not in ['nationaal', 'holland']:
        print("Invalid level name. Please enter either 'Nationaal' or 'Holland'.")
        level_name = input("Enter the level name (Nationaal or Holland): ").lower()
    return level_name.capitalize()

def get_max_trajectories() -> int:
    """
    Get number of max trajectories from user

    post: returns integer
    """
    # Prompt user for input
    trajectories: Any = input("What is the maximum amount of trajectories? ")

    # Check if number of trajectories is valid, prompt user again if not
    while not (trajectories.isdigit() and 0 < int(trajectories) <= 100):
        print("Invalid input. Please enter a valid integer between 1 and 100.")
        trajectories = input("What is the maximum amount of trajectories? ")
    return int(trajectories)

def get_timeframe() -> int:
    """
    Get maximum amount of time a trajectory may take

    post: returns integer
    """
    # Prompt user for input
    timeframe: Any = input("What is the timeframe for one trajectory? ")

    # Check if timeframe is valid, prompt user again if not
    while not (timeframe.isdigit() and 5 <= int(timeframe) <= 1000):
        print("Invalid timeframe. Please enter a timeframe between 5 and 1000")
        timeframe = input("What is the timeframe for one trajectory? ")
    return int(timeframe)

def get_iterations() -> int:
    """
    Get amount of iterations the program needs to run

    post: return integer
    """
    # Prompt user for input
    iterations: Any = input("How many times would you like to run the algorithm? ")

    # Check if iterations is valid, prompt user again if not
    while not (iterations.isdigit() and 0 < int(iterations)):
        print("Invalid. Please enter a positive input for your iterations")
        iterations = input("How many times would you like to run the algorithm? ")
    return int(iterations)

def get_max_iterations() -> Any:
    """
    Get max iterations for usage of hillclimber or local search

    post: returns integer
    """
    # Prompt user for input
    max_iterations: Any = input("How many iterations are allowed when no better solution is found? ")

    # Check if max_iterations are valid, prompt user again if not
    while not (max_iterations.isdigit() and 0 < int(max_iterations)):
        print("Invalid. Please enter a positive input for your iterations")
        max_iterations = input("How many iterations are allowed when no better solution is found? ")
    return int(max_iterations)

def finetune_railnetwork(railnetwork) -> list:
    """
    Change formatting of list of railnetwork into a neater output

    pre: list of lists
    post: list of lists
    """
    trajectory_count: int = len(railnetwork)
    for i in range(trajectory_count):
        railnetwork[i] = '[' + ', '.join(railnetwork[i]) + ']'

    return railnetwork
