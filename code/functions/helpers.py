def get_user_input():
    algorithm_choice = input("What algorithm do you want to run? (totally_random, semi_random, greedy_search, breadth_first, depth_first, hillclimber, local_search, or simulated_annealing): ").lower()

    if algorithm_choice not in ['totally_random', 'semi_random', 'greedy_search', 'breadth_first', 'depth_first', 'hillclimber', 'local_search', 'simulated_annealing']:
        print("Invalid algorithm choice. Please choose a valid algorithm.")
        return None

    level_name = input("Enter the level name: (Nationaal or Holland)")

    trajectories = int(input("What is the maximum amount of trajectories? "))
    timeframe = int(input("What is the timeframe for one trajectory? "))
    iterations = int(input("How many times would you like to run the algorithm?"))

    if algorithm_choice in ['hillclimber', 'local_search', 'simulated_annealing']:
        max_iterations = float(input("How many iterations are allowed when no better solution is found? "))
    
    iterations = int(input("How many times would you like to run the algorithm"))

    if algorithm_choice == "hillclimber":
        max_iterations = int(input("How many iterations are allowed when no better solution is found? "))
        return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations
    else:
        max_iterations = None
        return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations

def finetune_railnetwork(railnetwork):
    trajectory_count = len(railnetwork)
    for i in range(trajectory_count):
        railnetwork[i] = '[' + ', '.join(railnetwork[i]) + ']'
        print(railnetwork[i])

    return railnetwork
