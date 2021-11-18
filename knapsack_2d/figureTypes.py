import dataclasses
from dataclasses import dataclass
import random


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def isValid(self) -> bool:
        return self.x != -1 and self.y != -1

    @classmethod
    def rand(self, rangeX, rangeY):
        return Point(random.randint(*rangeX), random.randint(*rangeY))


# Can only hold perpendicular lines
class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.width = b.x - a.x if b.x - a.x != 0 else b.y - a.y

    def isVertical(self) -> bool:
        return self.a.x == self.b.x

    def isHorizontal(self) -> bool:
        return self.a.y == self.b.y

    def containsPoint(self, point: Point) -> bool:
        if self.isVertical():
            return point.x == self.a.x and self.a.y <= point.y <= self.b.y
        if self.isHorizontal():
            return point.y == self.a.y and self.a.x <= point.x <= self.b.x

    def containsLine(self, other):
        return self.containsPoint(other.a) and self.containsPoint(other.b)

    def splitAtPoint(self, point: Point):
        if not self.containsPoint(point):
            raise ValueError
        return [Line(self.a, point), Line(point, self.b)]

    def splitAtLine(self, line):
        if not self.containsLine(line):
            raise ValueError
        if self.a == line.a:
            return self.splitAtPoint(line.b)
        if self.b == line.b:
            return self.splitAtPoint(line.a)

        split = self.splitAtPoint(line.a)
        # Splits the remaining segment, will fall into one of the above if clauses
        return (split.append(split.pop.splitAtLine(line)))

    def __str__(self) -> str:
        return f"A - {self.a}, B - {self.b}"


class Rect:
    def __init__(self, a: Point, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.field = width * height
        self.a = a
        self.calcCoords()

    def calcCoords(self) -> None:
        #   d-----c
        #   |     |
        #   a-----b
        self.b = Point(self.a.x + self.width, self.a.y)
        self.c = Point(self.a.x + self.width, self.a.y + self.height)
        self.d = Point(self.a.x, self.a.y + self.height)

    def collides(self, other):
        return (self.a.x < other.c.x) and (self.c.x > other.a.x) and (self.a.y < other.c.y) and (self.c.y > other.a.y)

    def containsRectangle(self, other):
        return (other.a.x >= self.a.x) and (other.a.y >= self.a.y) and (other.c.x <= self.c.x) and (
                other.c.y <= self.c.y)

    def __str__(self) -> str:
        return f"A - {self.a}, B - {self.b}, C - {self.c}, D = {self.d}"

    def move(self, offset: Point) -> None:
        self.a = dataclasses.replace(self.a, x=self.a.x + offset.x, y=self.a.x + offset.y)
        self.calcCoords()

    def cloneOffset(self, offset: Point):
        newCoords = Point(self.a.x + offset.x, self.a.y + offset.y)
        return Rect(newCoords, self.width, self.height)


# For testing purposes
if __name__ == '__main__':
    l1 = Line(Point(4, 5), Point(8, 5))
    l2 = Line(Point(6, 5), Point(8, 5))

    result = l1.splitAtLine(l2)
    for i in range(len(result)):
        print(result[i])
