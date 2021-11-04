from random import randint, random
from figureTypes import *
import random

class Specimen:
    def __init__(self, genes :int, rangeOfRands) -> None:
        self.chrsom = [random.randint(*rangeOfRands) for x in range(genes)]
        self.rangeOfRands = rangeOfRands
        self.fitness = 0
    
    def countFitness(self) -> None:
        pass

    def setchrsom(self, chrsom) -> None:
        self.chrsom = chrsom

    def randGenes(self, num) -> int:
        return random.choices(range(self.chrsom), k = num)

    def swap(self):
        (i1, i2) = self.randGenes(2)
        self.chrsom[i1], self.chrsom[i2] = self.chrsom[i2], self.chrsom[i1]

    def replacement(self):
        self.chrsom[self.randGenes(1)] = random.randint(*self.rangeOfRands)
    
    def inversion(self):
        (min_idx, max_idx) = sorted(self.randGenes(2))
        self.chrsom = \
            self.chrsom[:min_idx] + \
            list(reversed(self.chrsom[min_idx:max_idx])) + \
            self.chrsom[max_idx:]

class GeneticAlgorithm:
    def __init__(self, generationSize: int, mutProb: int, elitarism) -> None:
        self.generation = [Specimen() for x in range(generationSize)]
        self.mutProb = mutProb
        self.elitarism = elitarism

    @classmethod
    def getChildren(cls, parent1: Specimen, parent2 :Specimen) -> list(Specimen):
        n = random.choice(parent1.randGenes(1))
        child1, child2 = Specimen(), Specimen()
        child1.setchrsom(parent1.chrsom[0:n] + parent2.chrsom[n:])
        child2.setchrsom(parent1.chrsom[0:n] + parent2.chrsom[n:])
        return [child1, child2]

    def buildNewGeneration(self) -> None:
        self.generation.sort(key = lambda x : x.fitness, reverse= True)
        new = [*self.generation[:int(len(self.generation) * self.elitarism)]]
        fitnessArray = [x.fitness for x in self.generation]
        while len(new) < len(self.generation):
            parents = random.choices(self.generation, weights=fitnessArray, k=2)
            children = self.getChildren(*parents)
            for child in children:
                child.mutate(self.mutProb)
            new.extend(children)
        self.generation = new

    def repeat(self, n: int) -> None:
        for x in range(n):
            self.buildNewGeneration()