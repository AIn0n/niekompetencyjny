from chromosomes.Chromosome import Chromosome
from random import uniform


class FloatChromosome(Chromosome):
    def randGene(self):
        return uniform(0, 1)
