# Description: This file contains utility functions for the genetic algorithm implementation.
# Import the necessary libraries
import random
import statistics
import csv
from itertools import chain
from data import nutrients, data

# This function initializes a population of individuals with a specified number of ingredients
def initialize_population(population_size, individual_size):
    """
    Initialize Population for Genetic Algorithm.
    
    Parameters:
        population_size: Number of total individuals desired
        individual_size: Number of ingredients per individual

    Output: List of n (population_size) individuals, each a list of m (individual_size) ingredients
    """
    population = []
    # Ensure that every ingredient is present at least once -> Attempt to ensure variety
    while len(set(chain.from_iterable(population))) != len(data):
        population = []
        # Populate
        while len(population) != population_size:
            # Generate individuals
            # Randomly generate the individuals - list of ingredients of a size individual_size
            individual = random.sample(range(len(data)), individual_size)
            population.append(individual)

    return population


# This function calculates the fitness of an individual in a population based on certain constraints and penalties
def fitness(individual, population, data, nutrients_constraints, penalty_weight):
    """
    Fitness Function for Genetic Algorithm.

    Parameters:
        individual: The individual to evaluate
        population: The current population
        data: The data containing the ingredients and their properties
        nutrients_constraints: Whether nutrient constraints are considered
        penalty_weight: The weight of the penalty for violating constraints

    Output: The fitness score of the individual
    """
    counts = {}  # A dictionary to keep track of ingredient counts
    fitness = 0  # The fitness score of the individual
    penalty = 0  # The penalty score for violating constraints

    if nutrients_constraints:
        # If there are nutrient constraints, calculate the sum of prices and nutrient values for the individual
        sum_price = sum(data[dish][2] for dish in individual)
        sum_nutrients = [sum(data[dish][i] for dish in individual) for i in range(3, 12)]
        fitness = sum_price  # The fitness score is initially set to the sum of prices
        for diet_nutrients, min_requirement in zip(sum_nutrients, nutrients):
            # Iterate over the diet nutrient values and the minimum requirements
            if diet_nutrients - min_requirement[1] < 0:
                # If the diet nutrient value is less than the minimum requirement, add a penalty
                fitness += 1
        for entity in population:
            # Iterate over each entity in the population
            for ingredient in list(set(entity)):
                # Iterate over each unique ingredient in the entity and update the ingredient counts
                if ingredient in counts:
                    counts[ingredient] += 1
                else:
                    counts[ingredient] = 1
        for ingredient in individual:
            # Iterate over each ingredient in the individual
            if counts[ingredient] != 1:
                # If an ingredient appears more than once, add a penalty
                penalty += counts[ingredient]
        if max(counts) != min(counts):
            # If there is a variation in ingredient counts, calculate the penalty based on the counts
            penalty = ((penalty - min(counts)) / (max(counts) - min(counts))) * penalty_weight
        else:
            penalty = 0.5  # If all ingredient counts are the same, set a default penalty
        fitness += penalty  # Add the penalty to the fitness score

    else:
        # If there are no nutrient constraints, calculate the sum of prices for the individual
        fitness = 0
        for ingredient in individual:
            # Iterate over each ingredient in the individual and update the fitness score
            fitness += data[ingredient][2]
        for entity in population:
            # Iterate over each entity in the population
            for ingredient in list(set(entity)):
                # Iterate over each unique ingredient in the entity and update the ingredient counts
                if ingredient in counts:
                    counts[ingredient] += 1
                else:
                    counts[ingredient] = 1
        for ingredient in individual:
            # Iterate over each ingredient in the individual
            if counts[ingredient] != 1:
                # If an ingredient appears more than once, add a penalty
                penalty += counts[ingredient]
        if max(counts) != min(counts):
            # If there is a variation in ingredient counts, calculate the penalty based on the counts
            penalty = ((penalty - min(counts)) / (max(counts) - min(counts))) * penalty_weight
        else:
            penalty = 0.5  # If all ingredient counts are the same, set a default penalty
        fitness += penalty  # Add the penalty to the fitness score
    return fitness

# This function selects the elite individual from a population based on the fitness values
def get_elite(population, fitness_values, problem):
    """
    Get Elite Individual from Population.
    
    Parameters:
        population: The current population
        fitness_values: The fitness values of the individuals
        problem: 'max' for maximization problem, 'min' for minimization problem
    
    Output: The elite value and the elite individual
    """
    if problem == 'max':
        elite_value = max(fitness_values)
        elite_indvidual = population[fitness_values.index(max(fitness_values))]
    elif problem == 'min':
        elite_value = min(fitness_values)
        elite_indvidual = population[fitness_values.index(min(fitness_values))]
    return elite_value, elite_indvidual

# This function selects two parents from a population using a selection function
def select_parents(current_population, fitness_generation, select_function, problem):
    """
    Select Parents for Reproduction.

    Parameters: 
        current_population: The current population
        fitness_generation: The fitness values of the individuals
        select_function: The selection function to use
        problem: 'max' for maximization problem, 'min' for minimization problem
    
    Output: Two parent individuals

    """
    parent1 = select_function(current_population, fitness_generation, problem)
    parent2 = select_function(current_population, fitness_generation, problem)
    return parent1, parent2

# This function generates offspring from two parents using a crossover function
def generate_offspring(parent1, parent2, crossover_function, reproduction_probability, mutate_function, mutation_probability):
    """
    Generate Offspring from Parents.

    Parameters:
        parent1: The first parent individual
        parent2: The second parent individual
        crossover_function: The crossover function to use
        reproduction_probability: The probability of reproduction
        mutate_function: The mutation function to use
        mutation_probability: The probability of mutation

    Output: Two offspring individuals
    """

    if random.uniform(0, 1) < reproduction_probability:
        offspring1, offspring2 = crossover_function(parent1, parent2)
    else:
        offspring1, offspring2 = parent1, parent2

    if random.uniform(0, 1) < mutation_probability:
        offspring1 = mutate_function(offspring1)

    if random.uniform(0, 1) < mutation_probability:
        offspring2 = mutate_function(offspring2)

    return offspring1, offspring2

# This function replaces the worst individual in the population with the elite individual
def replace_worst_with_elite(population, fitness_values, elite_value, elite_individual, current_population, data, fitness_constraint, penalty_weight, problem):
    """
    Replace the Worst Individual with the Elite Individual.

    Parameters:
        population: The current population
        fitness_values: The fitness values of the individuals
        elite_value: The fitness value of the elite individual
        elite_individual: The elite individual
        current_population: The current population
        data: The data containing the ingredients and their properties
        fitness_constraint: Whether nutrient constraints are considered
        penalty_weight: The weight of the penalty for violating constraints
        problem: 'max' for maximization problem, 'min' for minimization problem
        
    Updated population and fitness values
    """
    if problem == 'max':
        worst_value = min(fitness_values)
        if elite_value > worst_value:
            population.pop(fitness_values.index(worst_value))
            fitness_values.pop(fitness_values.index(worst_value))
            population.append(elite_individual)
            fitness_values.append(fitness(elite_individual, current_population, data, fitness_constraint, penalty_weight))
    elif problem == 'min':
        worst_value = max(fitness_values)
        if elite_value < worst_value:
            population.pop(fitness_values.index(worst_value))
            fitness_values.pop(fitness_values.index(worst_value))
            population.append(elite_individual)
            fitness_values.append(fitness(elite_individual, current_population, data, fitness_constraint, penalty_weight))

# This function evolves a population over a number of generations
def evolution(inital_population, generations, reproduction_probability, mutation_probability, select_function, crossover_function, mutate_function, elitism, problem, penalty_weight, fitness_constraint):
    """
    Evolution of Population over Generations.

    Parameters:
        inital_population: The initial population
        generations: The number of generations to evolve
        reproduction_probability: The probability of reproduction
        mutation_probability: The probability of mutation
        select_function: The selection function to use
        crossover_function: The crossover function to use
        mutate_function: The mutation function to use
        elitism: Whether to use elitism
        problem: 'max' for maximization problem, 'min' for minimization problem
        penalty_weight: The weight of the penalty for violating constraints
        fitness_constraint: Whether nutrient constraints are considered

    Output: The median fitness values over generations and the best individual
    """
    current_population = []
    median_fitness_generations = []

    for generation in range(generations):
        new_population = []

        # Calculate fitness for the initial population
        if generation == 0:
            current_population = inital_population
            fitness_generation = [fitness(individual, current_population, data, fitness_constraint, penalty_weight) for individual in current_population]
            median_fitness_generations.append(statistics.median(fitness_generation))

        # Generate new population
        while len(new_population) < len(inital_population):
            # Elitism: keep the best individual for the next generation
            if elitism:
                elite, elite_indv = get_elite(current_population, fitness_generation, problem)

            # Select two parents and generate offspring
            parent1, parent2 = select_parents(current_population, fitness_generation, select_function, problem)
            offspring1, offspring2 = generate_offspring(parent1, parent2, crossover_function, reproduction_probability, mutate_function, mutation_probability)

            # Add offspring to the new population
            new_population.extend([offspring1, offspring2][:len(inital_population) - len(new_population)])

        # Calculate fitness for the new population
        fitness_generation = [fitness(individual, new_population, data, fitness_constraint, penalty_weight) for individual in new_population]
        median_fitness_generations.append(statistics.median(fitness_generation))

        # Elitism: replace the worst individual with the elite if necessary
        if elitism:
            replace_worst_with_elite(new_population, fitness_generation, elite, elite_indv, current_population, data, fitness_constraint, penalty_weight, problem)

        current_population = new_population

    return median_fitness_generations, new_population[fitness_generation.index(min(fitness_generation))]

# This function writes the results of the genetic algorithm to a CSV file
def write_results_to_csv(filename, median_fitness, best_individual):
    """
    Write Results to CSV File.
    
    Parameters:
        filename: The name of the CSV file
        median_fitness: The median fitness values over generations
        best_individual: The best individual
    
    Outputs CSV file with the results to directory
    """

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generation', 'Median Fitness'])
        for generation, fitness in enumerate(median_fitness):
            writer.writerow([generation, fitness])
        writer.writerow(['Best Individual'])
        writer.writerow(best_individual)