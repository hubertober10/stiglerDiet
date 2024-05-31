import random

# This function is performing the ranking selection
def ranking_selection(current_population, fitness_generation, problem):
    """
    Ranking Selection: Individuals are sorted based on their fitness.
    Only takes into account a position on the raking and not the value itself.

    Parameters:
        current_population: population
        fitness_generation: list with the fitness of each individual
        problem: 'max' for maximization problem, 'min' for minimization problem

    Output: One individual
    """

    # Zip the current population and their fitness values into a list of tuples
    list_tuple_individuals_fitness = list(zip(current_population, fitness_generation))

    # Sort the list of tuples based on the fitness value
    # If it's a maximization problem, sort in ascending order
    # If it's a minimization problem, sort in descending order
    list_tuple_individuals_fitness.sort(key=lambda x: x[1], reverse=(problem == 'min'))

    # Calculate the selection probability for each individual using a linear function
    # The probability is proportional to the individual's rank in the sorted list
    selection_prob = [(individual, (index + 1) / len(list_tuple_individuals_fitness)) 
                      for index, (individual, _) in enumerate(list_tuple_individuals_fitness)]

    # Select a random individual and check if it's selected based on its selection probability
    # If not, repeat the process until an individual is selected
    while True:
        new_indv, prob = random.choice(selection_prob)
        if prob > random.uniform(0, 1):
            return new_indv