import math
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    # todo: Test this method
    def distance(self, other):
        return math.sqrt(
            pow(abs(self.x - other.x), 2) + pow(abs(self.y - other.y), 2)
        )

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    @staticmethod
    def zero():
        return Point(0, 0)

    @staticmethod
    def getDoorPlacement(l: list, v: float):
        return l[int(len(l) * v)]


class Vec:
    start: Point
    end: Point

    def __init__(self, p1: Point, p2: Point):
        # Ensures the leftmost or uppermost point is start
        if p1.x < p2.x or p1.y < p2.y:
            self.start = p1
            self.end = p2
        else:
            self.start = p1
            self.end = p2

    def __str__(self):
        return f"[{self.start}, {self.end}]"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def getLength(self):
        # A Vec object can only be vertical or horizontal, therefore one of these is always 0
        return abs(self.start.x - self.end.x) or abs(self.start.y - self.end.y)

    def isVertical(self):
        return self.start.x == self.end.x

    def isHorizontal(self):
        return self.start.y == self.end.y

    def containsPoint(self, point) -> bool:
        if self.isHorizontal():
            return (
                point.y == self.start.y
                and self.start.x <= point.x <= self.end.x
            )
        if self.isVertical():
            return (
                point.x == self.start.x
                and self.start.y <= point.y <= self.end.y
            )

    def sameOrientation(self, other):
        return (self.isVertical() and other.isVertical()) or (
            self.isHorizontal() and other.isHorizontal
        )

    def collidesSameOrient(self, other) -> bool:
        if self.sameOrientation(other):
            return (
                (
                    self.containsPoint(other.start)
                    or self.containsPoint(other.end)
                    or other.containsPoint(self.start)
                    or other.containsPoint(self.end)
                )
                and self.start != other.end
                and self.end != other.start
            )
        return False

    def commonPart(self, other):
        assert self.collidesSameOrient(other)
        if self.isVertical():
            return Vec(
                Point(self.start.x, max(self.start.y, other.start.y)),
                Point(self.end.x, min(self.end.y, other.end.y)),
            )
        if self.isHorizontal():
            return Vec(
                Point(max(self.start.x, other.start.x), self.start.y),
                Point(min(self.end.x, other.end.x), self.end.y),
            )

    def toPointsNoBorders(self):
        points = list()
        if self.isVertical():
            for y in range(self.start.y + 1, self.end.y - 1):
                points.append(Point(self.start.x, y))
        if self.isHorizontal():
            for x in range(self.start.x + 1, self.end.x - 1):
                points.append(Point(x, self.start.y))
        return points

    def getDoorPoint(self, value):
        point = self.getLength() * value
        point = round(point)
        if self.isHorizontal():
            door_X = self.start.x + point
            if door_X == self.start.x:
                door_X += 1
            if door_X == self.end.x:
                door_X -= 1
            door_Y = self.start.y
        else:
            door_Y = self.start.y + point
            if door_Y == self.start.y:
                door_Y += 1
            if door_Y == self.end.y:
                door_Y -= 1
            door_X = self.start.x
        return Point(door_X, door_Y)


class Rect:
    def __init__(self, p: Point, width: int, height: int) -> None:
        if height % 2 or width % 2 or not height or not width:
            raise ValueError("every dim should be divisible by two")
        self.width_l = width // 2
        self.width_r = width // 2
        self.height_u = height // 2
        self.height_d = height // 2
        self.p = p
        self.calcEverything()

    def __eq__(self, __o: object) -> bool:
        return (
            self.getHeight() == __o.getHeight()
            and self.getWidth() == __o.getWidth()
            and self.p == __o.p
        )

    def calcCoords(self) -> None:
        """
        d-------c
        |       |
        a-------b
        """
        self.a = Point(self.p.x - self.width_l, self.p.y - self.height_d)
        self.b = Point(self.p.x + self.width_r, self.p.y - self.height_d)
        self.c = Point(self.p.x + self.width_r, self.p.y + self.height_u)
        self.d = Point(self.p.x - self.width_l, self.p.y + self.height_u)

    def calcVecs(self) -> None:
        """
        end
        ^
        |
        start-->end
        """
        self.horUp = Vec(self.d, self.c)
        self.horDown = Vec(self.a, self.b)
        self.verLeft = Vec(self.a, self.d)
        self.verRight = Vec(self.b, self.c)

    def calcField(self) -> None:
        self.field = (self.width_l + self.width_r) * (
            self.height_u + self.height_d
        )

    def getHeight(self) -> int:
        return self.verLeft.getLength()

    def getWidth(self) -> int:
        return self.horUp.getLength()

    def collides(self, other) -> bool:
        return (
            (self.a.x < other.c.x)
            and (self.c.x > other.a.x)
            and (self.a.y < other.c.y)
            and (self.c.y > other.a.y)
        )

    def containsRectangle(self, other) -> bool:
        return (
            (other.a.x >= self.a.x)
            and (other.a.y >= self.a.y)
            and (other.c.x <= self.c.x)
            and (other.c.y <= self.c.y)
        )

    def __str__(self) -> str:
        return f"A - {self.a}, B - {self.b}, C - {self.c}, D = {self.d}"

    def cloneOffset(self, offset: Point):
        p = Point(self.p.x + offset.x, self.p.y + offset.y)
        return Rect(
            p, self.width_l + self.width_r, self.height_u + self.height_d
        )

    def getVerVecs(self) -> Iterable:
        return [self.verLeft, self.verRight]

    def getHorVecs(self) -> Iterable:
        return [self.horDown, self.horUp]

    def isToRightOf(self, rect):
        return rect.b.x <= self.a.x

    def isToLeftOf(self, rect):
        return self.b.x <= rect.a.x

    def isBelow(self, rect):
        return self.d.y <= rect.a.y

    def isAbove(self, rect):
        return rect.d.y <= self.a.y

    # An alternative, potentially better solution would be checking if only one of isAbove, below, lefOf, rightOf
    # applies and the appropriate vector is at the same x/y
    def neighbours(self, other) -> bool:
        result = []
        for s in self.getHorVecs():
            for o in other.getHorVecs():
                if s.collidesSameOrient(o):
                    result.append(s)
        for s in self.getVerVecs():
            for o in other.getVerVecs():
                if s.collidesSameOrient(o):
                    result.append(s)
        return result

    # Would the rectangle come into conflict with the given vector if it were to be expanded downwards?
    def isAlignedDown(self, rect):
        return self.isAbove(rect) and (
            (self.a.x < rect.a.x < self.b.x or self.a.x < rect.b.x < self.b.x)
            or (rect.a.x <= self.b.x <= rect.b.x)
        )

    # Would the rectangle come into conflict with the given vector if it were to be expanded upwards?
    def isAlignedUp(self, rect):
        return self.isBelow(rect) and (
            (self.a.x < rect.a.x < self.b.x or self.a.x < rect.b.x < self.b.x)
            or (rect.a.x <= self.b.x <= rect.b.x)
        )

    # Would the rectangle come into conflict with the given vector if it were to be expanded to the left?
    def isAlignedLeft(self, rect):
        return self.isToRightOf(rect) and (
            (self.b.y < rect.a.y < self.c.y or self.b.y < rect.d.y < self.c.y)
            or (rect.a.y <= self.b.y and rect.d.y >= self.c.y)
        )

    # Would the rectangle come into conflict with the given vector if it were to be expanded downwards?
    def isAlignedRight(self, rect):
        return self.isToLeftOf(rect) and (
            (self.b.y < rect.a.y < self.c.y or self.b.y < rect.d.y < self.c.y)
            or (rect.a.y <= self.b.y and rect.d.y >= self.c.y)
        )

    def calcEverything(self):
        self.calcCoords()
        self.calcField()
        self.calcVecs()

    def expandLeft(self, rects, area) -> None:
        new_x = max(
            [r.b.x for r in rects if self.isAlignedLeft(r)] + [area.a.x]
        )
        self.a = Point(new_x, self.a.y)
        self.d = Point(new_x, self.d.y)
        self.width_l = abs(self.p.x - new_x)
        self.calcEverything()

    def expandRight(self, rects, area) -> None:
        new_x = min(
            [r.a.x for r in rects if self.isAlignedRight(r)] + [area.b.x]
        )
        self.b = Point(new_x, self.b.y)
        self.c = Point(new_x, self.c.y)
        self.width_r = abs(new_x - self.p.x)
        self.calcEverything()

    def expandUp(self, rects, area) -> None:
        new_y = min([r.a.y for r in rects if self.isAlignedUp(r)] + [area.d.y])
        self.c = Point(self.c.x, new_y)
        self.d = Point(self.d.x, new_y)
        self.height_u = abs(new_y - self.p.y)
        self.calcEverything()

    def expandDown(self, rects, area) -> None:
        new_y = max(
            [r.d.y for r in rects if self.isAlignedDown(r)] + [area.a.y]
        )
        self.a = Point(self.a.x, new_y)
        self.b = Point(self.b.x, new_y)
        self.height_d = abs(self.p.y - new_y)
        self.calcEverything()
