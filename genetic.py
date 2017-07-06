from crossover import onepoint
from random import randint


class metaData():
    pass
    #course count
    #min_slot
    #max_slot


class chromosome():
    
    def __init__(self, metadata):
        self.metadata = metadata

    def initializeRandomly(self):
        self.c = []
        i = 0
        while(i < self.metadata.course_count):
            i+=1
            self.c.append(randint(self.metadata.min_slot, self.metadata.max_slot))

        self.fitness = calculateFitness

    def initalizeCrossover(self, a, b, cross_type):
        self.c = cross_type(a, b)
        self.fitness = fitness()

    def mutate(self):
        index = randint(0, self.meta_data.coures_count-1)
        self.c[index] = randint(self.metadata.min_slot, self.metadata.max_slot)

    def calcFitness(self):
        return 0
        pass
