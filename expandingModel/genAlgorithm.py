from typing import Tuple
from figureTypes import *
from random import getrandbits, randint, choice, choices, uniform

class Specimen:
    def __init__(self, genes :int, rangeX, rangeY) -> None:
        self.rangeX, self.rangeY = rangeX, rangeY
        self.chrsom = [[self.getRndPoint(), self.getRndFuncNr()] for x in range(genes)]
        self.fitness = 0

    def randomizeChrsom(self) -> None:
        for n in range(len(self.chrsom)):
            self.chrsom[n] = [self.getRndPoint(), self.getRndFuncNr()]

    def getRndFuncNr(self) -> int:
        return [getrandbits(1) for n in range(4)]

    def getRndPoint(self):
        return Point(randint(*self.rangeX), randint(*self.rangeY))

    def randGenes(self, num) -> int:
        return choices(range(len(self.chrsom)), k = num)

    def newChild(self, chrsom, prob):
        child = Specimen(0, self.rangeX, self.rangeY)
        child.chrsom = chrsom
        child.mutate(prob)
        return child

    def swap(self) -> None:
        (i1, i2) = self.randGenes(2)
        self.chrsom[i1], self.chrsom[i2] = self.chrsom[i2], self.chrsom[i1]

    def replacement(self) -> None:
        self.chrsom[self.randGenes(1)[0]] = [self.getRndPoint(), self.getRndFuncNr()]

    def inversion(self) -> None:
        (min_idx, max_idx) = sorted(self.randGenes(2))
        self.chrsom = \
            self.chrsom[:min_idx] + \
            self.chrsom[min_idx:max_idx][::-1] + \
            self.chrsom[max_idx:]

    def mutate(self, prob) -> None:
        if uniform(0, 1) < prob:
            choice([self.swap, self.replacement, self.inversion])()

class FitnessClass:
    def __init__(self, area: Rect, rooms: tuple) -> None:
        self.area = area
        self.rooms = rooms

    def getRndSpecimen(self):
        rX = (self.area.a.x, self.area.b.x)
        rY = (self.area.a.y, self.area.d.y)
        return Specimen(len(self.rooms), rX, rY)

    def countFitness(self, specimen: Specimen) -> None:
        totalArea, rooms = 0, []
        for idx, gene in enumerate(specimen.chrsom):
            new = self.rooms[idx].cloneOffset(gene[0])
            if not self.area.containsRectangle(new) or\
               any(map(lambda room : room.collides(new), rooms)):
                specimen.fitness = 0
                return
            rooms.append(new)
        for _ in range(len(self.rooms)):
            r = rooms.pop(0)
            for i, func in enumerate([r.expandLeft, r.expandRight, r.expandUp, r.expandDown]):
                if gene[1][i]: func(rooms, self.area)
            totalArea += r.field
            rooms.append(r)

        specimen.fitness = totalArea

class GeneticAlgorithm:
    def __init__(
    self, 
    generationSize: int, 
    mutProb: float, 
    elitarism: float, 
    fitnessClass: FitnessClass) -> None:
        self.generation = [fitnessClass.getRndSpecimen() for x in range(generationSize)]
        self.mutProb = mutProb
        self.elitarism = elitarism
        self.fitnessClass = fitnessClass

    def getChildren(self, p1: Specimen, p2 :Specimen) -> list:
        n, childs = *p1.randGenes(1), []
        for chrsom in [p1.chrsom[0:n] + p2.chrsom[n:], p2.chrsom[0:n] + p1.chrsom[n:]]:
            childs.append(p1.newChild(chrsom, self.mutProb))
            self.fitnessClass.countFitness(childs[-1])
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

        fitnessArr = [x.fitness for x in self.generation]
        while len(new) < len(self.generation):
            parents = choices(self.generation, weights=fitnessArr, k=2)
            new.extend(self.getChildren(*parents))
        self.generation = new

    def repeat(self, n: int) -> None:
        for x in range(n):
            self.buildNewGeneration()