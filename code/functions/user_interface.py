def get_user_input():
    algorithm_choice = input("What algorithm do you want to run? (Totally_random, Semi_random, GreedySearch, Breadthfirst, Depthfirst, Hillclimber, Local_search, or Simulated_annealing): ").lower()

    if algorithm_choice not in ['totally_random', 'semi_random', 'greedySearch', 'breadthfirst', 'depthfirst', 'hillclimber', 'local_search', 'simulated_annealing']:
        print("Invalid algorithm choice. Please choose a valid algorithm.")
        return None

    level_name = input("Enter the level name: ")

    trajectories = int(input("What is the maximum amount of trajectories? "))
    timeframe = int(input("What is the timeframe for one trajectory? "))
    iterations = int(input("How many times would you like to run the algorithm"))

    if algorithm_choice in ['Hillclimber', 'Local_search', 'Simulated_annealing']:
        max_iterations = int(input("How many iterations are allowed when no better solution is found? "))
        return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations
    else:
        max_iterations = None
        return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations