from chromosomes.Chromosome import Chromosome
from figures import Point
from random import randint


class LocationChromosome(Chromosome):
    def __init__(self, size, rY, rX):
        self.rX, self.rY = rX, rY
        super().__init__(size)

    def randGene(self):
        return Point(randint(*self.rX), randint(*self.rY))
