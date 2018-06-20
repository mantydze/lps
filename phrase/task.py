import string
import random
import itertools
import numpy as np

DNA = "!., " + string.ascii_letters# + string.digits + string.punctuation
print(DNA)
PARENT_SIZE = 2 # Number of parents used to breed new child
MUTATION_RATE = 0.01
N_GENERATIONS = 100

def calc_fitness(population, target):
    """ Calculate fitness scores of given population
        population - list of strings
        target - string value we are looking for

        return [('str_value', fitness_score), ...]
    """
    fitness = []
    for p in population:
        f = sum(x == y for x, y in zip(p, target))
        fitness.append((p, f))

    return fitness

def gen_parent(l):
    """ Generate random string.
        l - length
    """
    return

def initial_population(target_size, pop_size=300):
    """ Generates initial population ['abc', 'xyz', ...]
        target_size - length of string
    """
    population = []
    for _ in range(pop_size):
        population.append(''.join(random.choices(DNA, k=target_size)))

    return population

def breed(parents, target_size):
    """ Breed given parents and return next generation of children
        parents - [
            (('ABC', 1), ('ABD', 2), ...),
            ... ]
    """

    next_generation = []
    # Create one child from each family
    for family in parents:
        child = ""
        # Create new child letter by letter
        for i in range(target_size):
            allele = ""
            if random.random() < MUTATION_RATE:
                allele = random.choice(DNA)
            else:
                alleles = [parent[0][i] for parent in family]
                allele = random.choice(alleles)

            child += allele

        next_generation.append(child)

    return next_generation

def evolve(population, target, verbose=True):

    for i in range(N_GENERATIONS+1):
        # fitness: [('abc', 1), ('xyz', 0), ...]
        fitness = calc_fitness(population, target)
        # Individual with best fitness value from current population
        best = sorted(fitness, key=lambda x:x[1], reverse=True)[0]

        if verbose:
            print("Generation %d :: %s" % (i, best))
        if best[0] == target:
            return True, population

        # All possible combinations of parents
        parents = itertools.combinations(fitness, PARENT_SIZE)
        # Sort combination of parents by sum of their fitness scores
        parents = sorted(parents, key=lambda x:sum([i[1] for i in x]), reverse=True)
        # Take only best parent combinations
        parents = parents[:len(population)]
        # Breed next population from best parents
        population = breed(parents, len(target))

    return False, population

if __name__ == '__main__':

    TARGET = "Monika yra pasiutus ir niekada nemiega!!!!"

    population = initial_population(len(TARGET))
    found, population = evolve(population, TARGET)

    print(found)