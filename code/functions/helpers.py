def get_user_input():

    algorithm_choice = input("What algorithm do you want to run? (totally_random, semi_random, greedy_search, breadth_first, depth_first, hillclimber, local_search, or simulated_annealing): ").lower()

    while algorithm_choice not in ['totally_random', 'semi_random', 'greedy_search', 'breadth_first', 'depth_first', 'hillclimber', 'local_search', 'simulated_annealing']:
        
        if algorithm_choice not in ['totally_random', 'semi_random', 'greedy_search', 'breadth_first', 'depth_first', 'hillclimber', 'local_search', 'simulated_annealing']:
            print("Invalid algorithm choice. Please choose a valid algorithm.")

        algorithm_choice = input("What algorithm do you want to run? (totally_random, semi_random, greedy_search, breadth_first, depth_first, hillclimber, local_search, or simulated_annealing): ").lower()

    level_name = input("Enter the level name (Nationaal or Holland): ")

    while level_name.lower() not in ['nationaal', 'holland']:
        if level_name.lower() not in ['nationaal', 'holland']:
            print("Invalid level name. Please enter either 'Nationaal' or 'Holland'.")

        level_name = input("Enter the level name (Nationaal or Holland): ").lower()

    trajectories = int(input("What is the maximum amount of trajectories? "))

    while trajectories <= 0 and trajectories >= 100:

        if trajectories <= 0 and trajectories >= 100:
             print("Invalid amount. Please enter an amount between 0 and 100")

        trajectories = int(input("What is the maximum amount of trajectories? "))

    timeframe = int(input("What is the timeframe for one trajectory? "))

    while timeframe <= 0 and timeframe >= 1000:

        if timeframe <= 0 and timeframe >= 1000:
             print("Invalid timeframe. Please enter a timeframe between 0 and 1000")

        timeframe = int(input("What is the timeframe for one trajectory? "))

    iterations = int(input("How many times would you like to run the algorithm? "))

    while iterations <= 0:

        if iterations <= 0:
             print("Invalid. Please enter a positive input for your iterations")

        iterations = int(input("How many times would you like to run the algorithm? "))

    if algorithm_choice in ['hillclimber', 'local_search', 'simulated_annealing']:

        max_iterations = int(input("How many iterations are allowed when no better solution is found? "))

        while max_iterations <= 0:

            if iterations <= 0:
                print("Invalid. Please enter a positive input for your iterations")

            max_iterations = int(input("How many iterations are allowed when no better solution is found? "))

    else:
        max_iterations = None

    return algorithm_choice, level_name, trajectories, timeframe, iterations, max_iterations

def finetune_railnetwork(railnetwork):
    trajectory_count = len(railnetwork)
    for i in range(trajectory_count):
        railnetwork[i] = '[' + ', '.join(railnetwork[i]) + ']'
        print(railnetwork[i])

    return railnetwork
