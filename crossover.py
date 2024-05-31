import random

# Ths function is performing the One Point Crossover
def onePoint_Crossover(parent1, parent2):
    """
    One Point Crossover: exchange of syntactic characteristics of two individuals - generating an offspring that
                         is the combination of the parents.

    Parameters:
        parent1: individual one for reproduction
        parent2: indivudal two for reproduction

    Output: Two individuals - Offsprings
    """
    
    # Choice of a random point for crossover
    # 1 and len(parent) -1 to ensure that the crossover point is not the first or last element of the individual and that the offspring is not the same as the parents
    cross_point = random.randint(1, len(parent1) - 1)

    # Reproduction stage with two parents
    # The first offspring is a combination of the first part of parent1 and the second part of parent2
    first_offspring = parent1[:cross_point] + parent2[cross_point:]

    # The second offspring is a combination of the first part of parent2 and the second part of parent1
    second_offspring = parent2[:cross_point] + parent1[cross_point:]

    return first_offspring, second_offspring