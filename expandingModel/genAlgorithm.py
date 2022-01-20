from chromosomes.FloatChromosome import FloatChromosome
from figures.figures import *
from chromosomes.LocationChromosome import LocationChromosome
from chromosomes.BinaryChromosome import BinaryChromosome
from random import choice, choices
import copy, itertools


class Specimen:
    def __init__(self, size: int, rX: tuple, rY: tuple) -> None:
        self.chrsoms = {
            "location": LocationChromosome(size, rY, rX),
            "rotation": BinaryChromosome(size),
            "expansion": BinaryChromosome(size * 4),
            "doors": FloatChromosome(size),
        }
        self.fitness = 0

    def getChild(self, chrsom: dict, rX: tuple, rY: tuple):
        result = Specimen(len(self.chrsoms["location"]), rX, rY)
        result.chrsoms = chrsom
        return result


class FitnessClass:
    def __init__(self, area: Rect, rooms: tuple) -> None:
        self.area = area
        self.rooms = rooms
        self.rX = (self.area.a.x, self.area.b.x)
        self.rY = (self.area.a.y, self.area.d.y)

    def getRndSpecimen(self):
        return Specimen(len(self.rooms), self.rX, self.rY)

    def getChildren(self, p1: Specimen, p2: Specimen, mut: float) -> list:
        chrsoms1, chrsoms2 = {}, {}
        for k in p1.chrsoms.keys():
            p = choice(range(len(p1.chrsoms[k])))
            chrsoms1[k] = copy.copy(p1.chrsoms[k])
            chrsoms2[k] = copy.copy(p2.chrsoms[k])
            chrsoms1[k].genes = p1.chrsoms[k][:p] + p2.chrsoms[k][p:]
            chrsoms2[k].genes = p2.chrsoms[k][:p] + p1.chrsoms[k][p:]
            chrsoms1[k].mutate(mut)
            chrsoms2[k].mutate(mut)

        return (
            p1.getChild(chrsoms1, self.rX, self.rY),
            p1.getChild(chrsoms2, self.rX, self.rY),
        )

    def validNeighborsAndGetDoors(
        self, rectangles: list, doorsParams: FloatChromosome
    ) -> bool:
        result = []
        for i in range(len(self.rooms)):
            tmp = []
            for n in range(len(self.rooms)):
                if self.rooms[n].name in self.rooms[i].neighbours or (
                    self.rooms[n].exit
                    and not rectangles[n].neighbours(self.area)
                ):
                    commVecs = rectangles[n].neighbours(rectangles[i])
                    if len(commVecs) < 1:
                        return False
                    allVecs = list(
                        itertools.chain.from_iterable(
                            [x.toPointsNoBorders() for x in commVecs]
                        )
                    )
                    if len(allVecs) < 1:
                        return False
                    tmp.append(Point.getDoorPlacement(allVecs, doorsParams[n]))
            result.append(tmp)
        return result

    def countFitness(self, s: Specimen) -> None:
        rcts = []
        for i in range(len(self.rooms)):
            # rotation and location
            rect = (
                self.rooms[i]
                .getRectRef(s.chrsoms["rotation"][i])
                .cloneOffset(s.chrsoms["location"][i])
            )
            if not self.area.containsRectangle(rect) or any(
                map(lambda r: r.collides(rect), rcts)
            ):
                s.fitness = 0
                return None
            rcts.append(rect)
        # expansion section
        expandRects(rcts, self.area, s.chrsoms["expansion"])

        # doors section
        doors = self.validNeighborsAndGetDoors(rcts, s.chrsoms["doors"])
        if doors == False:
            s.fitness = 0
            return None
        sumOfDist = sumAllDoorDist(doors)
        s.fitness = sum(x.field for x in rcts) * 1.0 / sumOfDist


def expandRects(rects: list, area: Rect, expansion) -> None:
    for n in range(len(rects)):
        r = rects.pop(0)
        funcs = [r.expandLeft, r.expandRight, r.expandUp, r.expandDown]
        for i, func in enumerate(funcs):
            if expansion[n * 4 + i]:
                func(rects, area)
        rects.append(r)


def sumAllDoorDist(doors: list):
    result = 0
    for room in doors:
        if len(room) > 1:
            for i in range(len(room)):
                for j in range(i + 1, len(room)):
                    result += room[i].distance(room[j])
    return result


class GeneticAlgorithm:
    def __init__(
        self,
        generationSize: int,
        mutProb: float,
        elitarism: float,
        fitnessClass: FitnessClass,
    ) -> None:
        self.generation = [
            fitnessClass.getRndSpecimen() for x in range(generationSize)
        ]
        self.mutProb, self.elitarism, self.fitnessClass = (
            mutProb,
            elitarism,
            fitnessClass,
        )

    def buildNewGeneration(self) -> None:
        for elem in self.generation:
            self.fitnessClass.countFitness(elem)
        # elitarism
        self.generation.sort(key=lambda x: x.fitness, reverse=True)
        new = [
            x
            for x in self.generation[
                : int(len(self.generation) * self.elitarism)
            ]
            if x.fitness > 0
        ]
        if len(new) < 2:
            while len(new) < len(self.generation):
                new.append(self.fitnessClass.getRndSpecimen())
        else:
            fitnessArr = [x.fitness for x in self.generation]
            while len(new) < len(self.generation):
                new.extend(
                    self.fitnessClass.getChildren(
                        *choices(self.generation, weights=fitnessArr, k=2),
                        self.mutProb
                    )
                )
        self.generation = new

    def repeat(self, n: int) -> None:
        for _ in range(n):
            self.buildNewGeneration()
