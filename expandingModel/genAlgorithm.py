from figureTypes import *
from LocationChromosome import LocationChromosome
from BinaryChromosome import BinaryChromosome
import copy
from random import choice, choices

class Specimen:
    def __init__(self, size, rX, rY) -> None:
        self.chrsoms = {
            'location' : LocationChromosome(size, rY, rX),
            'rotation' : BinaryChromosome(size),
            'expansion': BinaryChromosome(size * 4)}
        self.fitness = 0

    def getChild(self, o, mut):
        c1, c2 = copy.copy(self), copy.copy(o)
        for k in self.chrsoms.keys():
            p = choice(range(len(self.chrsoms[k].genes)))
            c1.chrsoms[k].genes[:p] = o.chrsoms[k].genes[:p]
            c1.chrsoms[k].mutate(mut)
            c2.chrsoms[k].genes[p:] = self.chrsoms[k].genes[p:]
            c2.chrsoms[k].mutate(mut)
        return c1, c2

class FitnessClass:
    def __init__(self, area: Rect, rooms: tuple) -> None:
        self.area = area
        self.rooms = rooms
        self.rcts = [Rect(Point(0,0), x.minWidth, x.minHeight) for x in rooms]
        self.rX = (self.area.a.x, self.area.b.x)
        self.rY = (self.area.a.y, self.area.d.y)

    def getRndSpecimen(self):
        return Specimen(len(self.rcts), self.rX, self.rY)
        
    def countFitness(self, s: Specimen) -> None:
        rcts = []
        for i in range(len(s.chrsoms['location'].genes)):
            #rotation section
            new = Rect(Point(0, 0), self.rcts[i].getHeight(), self.rcts[i].getWidth()) \
                if s.chrsoms['rotation'].genes[i] else self.rcts[i]
            #location section
            new = new.cloneOffset(s.chrsoms['location'].genes[i])
            if not self.area.containsRectangle(new) or\
               any(map(lambda r : r.collides(new), rcts)):
                s.fitness = 0
                return None

            rcts.append(new)
        #expansion section
        total_field = 0
        for n in range(len(self.rcts)):
            r = rcts.pop(0)
            for i, func in enumerate([r.expandLeft, r.expandRight, r.expandUp, r.expandDown]):
                if s.chrsoms['expansion'].genes[n*4 + i]:
                    func(rcts, self.area)
            total_field += r.field
            rcts.append(r)
        #neighbours section
        for i in range(len(self.rooms)):
            for n in range(len(self.rooms)):
                if self.rooms[n].name in self.rooms[i].neighbours and \
                   not rcts[n].neighbours(rcts[i]):
                    s.fitness = 0
                    return None

        s.fitness = total_field

class GeneticAlgorithm:
    def __init__(
    self, 
    generationSize: int, 
    mutProb:        float, 
    elitarism:      float, 
    fitnessClass:   FitnessClass) -> None:
        self.generation = [fitnessClass.getRndSpecimen() for x in range(generationSize)]
        self.mutProb = mutProb
        self.elitarism = elitarism
        self.fitnessClass = fitnessClass

    def getChildren(self, p1: Specimen, p2 :Specimen) -> list:
        childs = p1.getChild(p2, self.mutProb)
        return childs

    def buildNewGeneration(self) -> None:
        #elitarism
        self.generation.sort(key = lambda x : x.fitness, reverse= True)
        new = [*self.generation[:int(len(self.generation) * self.elitarism)]]
        if len(tuple(filter(lambda x : x.fitness > 0, self.generation))) < 2:
            while len(new) < len(self.generation):
                new.append(self.fitnessClass.getRndSpecimen())
        else:
            fitnessArr = [x.fitness for x in self.generation]
            while len(new) < len(self.generation):
                parents = choices(self.generation, weights=fitnessArr, k=2)
                new.extend(self.getChildren(*parents))

        #HOTFIX
        for elem in new:
            self.fitnessClass.countFitness(elem)
        self.generation = new

    def repeat(self, n: int) -> None:
        for x in range(n):
            self.buildNewGeneration()