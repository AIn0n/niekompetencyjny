from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass(frozen=True, order=True)
class Vec:
    start: Point
    end: Point


class Rect:

    def __init__(self, p: Point, width: int, height: int) -> None:
        if height % 2 or width % 2 or not height or not width:
            raise ValueError('every dim should be divisible by two')
        self.width_l = width / 2
        self.width_r = width / 2
        self.height_u = height / 2
        self.height_d = height / 2
        self.p = p
        self.calcCoords()
        self.calcField()
        self.calcVecs()

    def calcCoords(self) -> None:
        ''' d-------c
            |       |
            a-------b   '''
        self.a = Point(self.p.x - self.width_l, self.p.y - self.height_d)
        self.b = Point(self.p.x + self.width_r, self.p.y - self.height_d)
        self.c = Point(self.p.x + self.width_r, self.p.y + self.height_u)
        self.d = Point(self.p.x - self.width_l, self.p.y + self.height_u)

    def calcVecs(self) -> None:
        ''' end
            ^
            |
            start-->end   '''
        self.horUp = Vec(self.d, self.c)
        self.horDown = Vec(self.a, self.b)
        self.verLeft = Vec(self.a, self.d)
        self.verRight = Vec(self.b, self.c)

    def calcField(self) -> None:
        self.field = (self.width_l + self.width_r) * (self.height_u + self.height_d)

    def collides(self, other) -> bool:
        return (self.a.x < other.c.x) and (self.c.x > other.a.x) and \
               (self.a.y < other.c.y) and (self.c.y > other.a.y)

    def containsRectangle(self, other) -> bool:
        return (other.a.x >= self.a.x) and (other.a.y >= self.a.y) and \
               (other.c.x <= self.c.x) and (other.c.y <= self.c.y)

    def __str__(self) -> str:
        return f'A - {self.a}, B - {self.b}, C - {self.c}, D = {self.d}'

    def cloneOffset(self, offset: Point):
        p = Point(self.p.x + offset.x, self.p.y + offset.y)
        return Rect(p, self.width_l + self.width_r, self.height_u + self.height_d)

    def getVerVecs(self) -> Iterable:
        return [self.verLeft, self.verRight]

    def getHorVecs(self) -> Iterable:
        return [self.horDown, self.horUp]

    def expandLeft(self, vecs) -> None:
        if len(vecs) == 0: return
        new_x = max(v.start.x for v in filter(vecs, )
        self.a = Point(new_x, self.a.y)
        self.d = Point(new_x, self.d.y)
        self.width_l = abs(self.p.x) + abs(new_x)
        self.calcCoords()
        self.calcField()
        self.calcVecs()
