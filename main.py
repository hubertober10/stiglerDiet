# Description: This file is the main file of the project. It runs the genetic algorithm with different mutation probabilities and writes the results to a CSV file.
from selection import ranking_selection
from crossover import onePoint_Crossover
from mutation import scramble_mutation
from utility_functions import initialize_population, evolution, write_results_to_csv


# This part of the project runs the genetic algorithm with different mutation probabilities and writes the results to a CSV file
mutation_probabilities = [0.05, 0.1, 0.2]
reproduction_probabilities = [0.95, 0.9, 0.8]
fitness_constraint = [True, False]

for mutation in mutation_probabilities:
    for reproduction_probability in reproduction_probabilities:
        for fitness in fitness_constraint:
            for trial in range(30):
                initial_population =  initialize_population(100, 5)
                median_fitness_generations, best_individual = evolution(initial_population, 100, reproduction_probability, mutation, ranking_selection, onePoint_Crossover, scramble_mutation, True, 'min', 5, fitness)
                write_results_to_csv(f"{mutation}_{reproduction_probability}_{fitness}/{trial}_{mutation}_{reproduction_probability}_{fitness}.csv", median_fitness_generations, best_individual)