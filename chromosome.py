from random import randint
from metadata import metadata
from crossover import uniform
from crossover import onepoint

class chromosome():
    
    def __init__(self, md):
        self.metadata = md

    def initializeRandomly(self):
        self.c = []
        i = 0
        while(i < self.metadata.course_count):
            i+=1
            self.c.append(randint(self.metadata.min_slot, self.metadata.max_slot))

        self.fitness = calculateFitness

    def initalizeCrossover(self, c):
        self.c = c
        self.fitness = fitnessFunction(self.c)

    def mutate(self):
        index = randint(0, self.meta_data.coures_count-1)
        self.c[index] = randint(self.metadata.min_slot, self.metadata.max_slot)

    def calcFitness(self):
        pass
