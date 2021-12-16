from typing import Tuple
from figureTypes import *
from LocationChromosome import LocationChromosome
from BinaryChromosome import BinaryChromosome
import copy
from random import getrandbits, randint, choice, choices, uniform

class Specimen:
    def __init__(self, *kwargs) -> None:
        self.chrsoms = [*kwargs]
        self.fitness = 0

    def getChild(self, o):
        c1, c2 = copy.copy(self), copy.copy(o)
        for i in range(len(self.chrsoms)):
            p = choice(range(len(self.chrsoms[i].genes)))
            c1.chrsoms[i].genes[:p] = o.chrsoms[i].genes[:p]
            c2.chrsoms[i].genes[p:] = self.chrsoms[i].genes[p:]
        return c1, c2

class FitnessClass:
    def __init__(self, area: Rect, rooms: tuple) -> None:
        self.area = area
        self.rooms = rooms
        self.rX = (self.area.a.x, self.area.b.x)
        self.rY = (self.area.a.y, self.area.d.y)

    def getRndSpecimen(self):
        return Specimen(
            LocationChromosome(len(self.rooms), self.rY, self.rX), 
            BinaryChromosome(len(self.rooms)))
        
    def countFitness(self, s: Specimen) -> None:
        rooms, total_field = [], 0
        for idx, pos in enumerate(s.chrsoms[0].genes):
            new = Rect(Point(0, 0), 
             self.rooms[idx].height_u + self.rooms[idx].height_d,
             self.rooms[idx].width_l + self.rooms[idx].width_r) \
              if s.chrsoms[1].genes[idx] else self.rooms[idx]
                
            new = new.cloneOffset(pos)
            if not self.area.containsRectangle(new) or\
               any(map(lambda room : room.collides(new), rooms)):
                s.fitness = 0
                return
            rooms.append(new)
            total_field += new.field
        s.fitness = total_field

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
        childs = p1.getChild(p2)
        for child in childs:
            self.fitnessClass.countFitness(child)
        return childs

    def buildNewGeneration(self) -> None:
        #not valuable parents case
        if len(tuple(filter(lambda x : x.fitness > 0, self.generation))) < 2:
            for specimen in self.generation:
                for chromosome in specimen.chrsoms:
                    chromosome.mutate(1.0)
                self.fitnessClass.countFitness(specimen)
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