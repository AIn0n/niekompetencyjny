from abstracts.Chromosome import Chromosome
from random import getrandbits

class BinaryChromosome(Chromosome):
    def randGene(self):
        return getrandbits(1)