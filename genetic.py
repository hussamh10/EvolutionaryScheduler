import crossover as c
from metadata import metadata
from random import randint

md = metadata() #initializa meta data
population_count = 100 # even

def init():
    population = []
    total_fitness = 0

    while i < population_count:
        c = chromosome(md)
        c.initializeRandomly()
        total_fitness += c.fitness

        population.append(c)
        i+=1

    return population, total_fitness

def reproduce(population, crossover):
    new_population = []
    total_fitness = 0
    
    while i < population_count/2:
        x, y = selection(population)

        a = chromosome(md)
        a.initalizeCrossover(x)

        b = chromosome(md)
        b.initalizeCrossover(y)

        total_fitness += a.fitness
        total_fitness += b.fitness

        new_population.append(a)
        new_population.append(b)

    return population, total_fitness


def selection(population, total_fitness):
    #value = randint(0, population_count)

