import random
import math


class Genes:
    def __init__(self, size):
        self.index = 0
        self.directions = [None for i in range(size)]
        self.initialize()

    def initialize(self):
        for i in range(len(self.directions)):
            y = random.randint(0, 3)
            if y == 4:
                self.directions[i] = [0, 0]
            else:
                x = y * math.pi * 0.5
                self.directions[i] = [int(math.cos(x)), int(math.sin(x))]

    def clone(self, GL):
        gene = Genes(GL)
        for i in range(len(self.directions)):
            gene.directions[i] = self.directions[i]
        for i in range(len(self.directions), GL):
            y = random.randint(0, 3)
            if y == 4:
                gene.directions[i] = [0, 0]
            else:
                x = y * math.pi * 0.5
                gene.directions[i] = [int(math.cos(x)), int(math.sin(x))]
        return gene

    def mutate(self):
        mutation_probability = 0.01
        length_direction = len(self.directions)
        for idx in range(length_direction):
            if idx >= length_direction-20:
                mutation_probability *= 1.25
            c = random.random()
            if c <= mutation_probability:
                y = random.randint(0, 3)
                if y == 4:
                    self.directions[idx] = [0, 0]
                else:
                    x = y * math.pi * 0.5
                    self.directions[idx] = [int(math.cos(x)), int(math.sin(x))]
