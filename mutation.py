import random

# This function is performing the scramble mutation
def scramble_mutation(offspring):
    """
    Scramble Mutation: For a random individual select two random positions and shuffle the genes between them.

    Parameters:
        offspring: The individual to be mutated

    Output: Mutated individual
    """
    # Select two random points for the range to be shuffled
    cross_point = sorted(random.sample(range(len(offspring)), 2))

    # If the points are consecutive, choose new points
    while cross_point[1] - cross_point[0] == 1:
        cross_point = sorted(random.sample(range(len(offspring)), 2))

    # Get the subset to be shuffled
    shuffle_sublist = offspring[cross_point[0]:cross_point[1]]

    # Shuffle the subset
    random.shuffle(shuffle_sublist)

    # Replace the original subset with the shuffled subset
    offspring[cross_point[0]:cross_point[1]] = shuffle_sublist

    return offspring