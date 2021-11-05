from random import randint, random
from figureTypes import *
import random

class Specimen:
    def __init__(self, genes :int, rangeOfRands) -> None:
        self.chrsom = [Point.rand(rangeOfRands, rangeOfRands) for x in range(genes)]
        self.rangeOfRands = rangeOfRands
        self.fitness = 0

    def randomizeChrsom(self) -> None:
        for n in range(len(self.chrsom)):
            self.chrsom[n] = Point.rand(self.rangeOfRands, self.rangeOfRands)

    def randGenes(self, num) -> int:
        return random.choices(range(len(self.chrsom)), k = num)

    def swap(self) -> None:
        (i1, i2) = self.randGenes(2)
        self.chrsom[i1], self.chrsom[i2] = self.chrsom[i2], self.chrsom[i1]

    def replacement(self) -> None:
        self.chrsom[self.randGenes(1)[0]] = Point.rand(self.rangeOfRands, self.rangeOfRands)
    
    def inversion(self) -> None:
        (min_idx, max_idx) = sorted(self.randGenes(2))
        self.chrsom = \
            self.chrsom[:min_idx] + \
            list(reversed(self.chrsom[min_idx:max_idx])) + \
            self.chrsom[max_idx:]

    def mutate(self, prob) -> None:
        if random.uniform(0, 1) < prob:
            random.choice([self.swap, self.replacement, self.inversion])()

class FitnessClass:
    def __init__(self, area: Rect, rooms: tuple) -> None:
        self.area = area
        self.rooms = rooms

    def countFitness(self, specimen: Specimen) -> None:
        totalArea = 0
        movedRooms = []
        for idx, gene in enumerate(specimen.chrsom):
            if gene.isValid():
                movedRect = self.rooms[idx].cloneOffset(gene)
                if not self.area.containsRectangle(movedRect):
                    specimen.fitness = 0
                    return
                for room in movedRooms:
                    if movedRect.collides(room):
                        specimen.fitness = 0
                        return
                totalArea += movedRect.field
        if totalArea != 0: print("wow")
        specimen.fitness = totalArea

class GeneticAlgorithm:
    def __init__(
    self, 
    generationSize: int, 
    mutProb: float, 
    elitarism: float, 
    fitnessClass: FitnessClass)->None:
        self.generation = [Specimen(len(fitnessClass.rooms), [0, 20]) for x in range(generationSize)]
        self.mutProb = mutProb
        self.elitarism = elitarism
        self.fitnessClass = fitnessClass

    def getChildren(self, p1: Specimen, p2 :Specimen) -> list:
        n = p1.randGenes(1)[0]
        params = len(self.fitnessClass.rooms), p1.rangeOfRands
        childs = [Specimen(*params), Specimen(*params)]
        childs[0].chrsom = p1.chrsom[0:n] + p2.chrsom[n:]
        childs[1].chrsom = p1.chrsom[0:n] + p2.chrsom[n:]
        self.fitnessClass.countFitness(childs[0])
        self.fitnessClass.countFitness(childs[1])
        return childs

    def buildNewGeneration(self) -> None:
        #not valuable parents case
        if len(tuple(filter(lambda x : x.fitness > 0, self.generation))) < 2:
            for elem in self.generation:
                elem.mutate(1.0)
                self.fitnessClass.countFitness(elem)
            return

        #elitarism
        self.generation.sort(key = lambda x : x.fitness, reverse= True)
        new = [*self.generation[:int(len(self.generation) * self.elitarism)]]

        fitnessArray = [x.fitness for x in self.generation]
        if len(tuple(filter(lambda x : x > 0, fitnessArray))) < 2:
            for specimen in self.generation:
                specimen.mutate(1.0)
        
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
            #for s in self.generation:
                #print(s.chrsom)
            #print()

if __name__ == '__main__':
    squares = tuple([
        Rect(Point(0, 0), 5, 4), 
        Rect(Point(0, 0), 5, 6), 
        Rect(Point(0, 0), 3, 2)])
    fitCls = FitnessClass(Rect(Point(0, 0), 20, 20),squares)
    genAlg = GeneticAlgorithm(100, 0.1, 0.2, fitCls)
    genAlg.repeat(5000)