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

    def isVertical(self) -> bool:
        return self.start.x == self.end.x

    def isHorizontal(self) -> bool:
        return self.start.y == self.end.y

    def isAligned(self, other) -> bool:
        if self.isVertical() and other.isHorizontal and other.start.x <= self.start.x <= other.end.x:
            return True
        elif self.isHorizontal() and other.isVertical and other.start.y <= self.start.y <= other.end.y:
            return True
        return False


class Rect:

    def __init__(self, p: Point, width: int, height: int) -> None:
        if height % 2 or width % 2 or not height or not width:
            raise ValueError('every dim should be divisible by two')
        self.width_l = width // 2
        self.width_r = width // 2
        self.height_u = height // 2
        self.height_d = height // 2
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

    def isAlignedHorizontally(self, rect):
        return self.horUp.isAligned(rect.verRight) or self.horDown.isAligned(rect.verRight)

    def isAlignedVertically(self, rect):
        return self.verLeft.isAligned(rect.horDown) or self.verRight.isAligned(rect.horDown)

    def isToRightOf(self, rect):
        return rect.b.x <= self.a.x

    def isToLeftOf(self, rect):
        return self.b.x <= rect.a.x

    def isAbove(self, rect):
        return self.d.y <= rect.a.y

    def isBelow(self, rect):
        return rect.d.y <= self.a.y

    # Would the rectangle come into conflict with the given vector if it were to be expanded downwards?
    def isAlignedDown(self, rect):
        return self.isAlignedVertically(rect) and self.isAbove(rect)

    # Would the rectangle come into conflict with the given vector if it were to be expanded upwards?
    def isAlignedUp(self, rect):
        return self.isAlignedVertically(rect) and self.isBelow(rect)

    # Would the rectangle come into conflict with the given vector if it were to be expanded to the left?
    def isAlignedLeft(self, rect):
        return self.isAlignedHorizontally(rect) and self.isToRightOf(rect)

    # Would the rectangle come into conflict with the given vector if it were to be expanded downwards?
    def isAlignedRight(self, rect):
        return self.isAlignedHorizontally(rect) and self.isToLeftOf(rect)

    # todo: Introduce limits at the borders

    def expandLeft(self, rects, area) -> None:
        if len(rects) == 0: return
        try:
            new_x = max(r.b.x for r in rects if self.isAlignedLeft(r))
        except ValueError:              # If nothing is to the left
            new_x = area.a.x
        self.a = Point(new_x, self.a.y)
        self.d = Point(new_x, self.d.y)
        self.width_l = abs(self.p.x) + abs(new_x)
        self.calcCoords()
        self.calcField()
        self.calcVecs()

    def expandRight(self, rects, area) -> None:
        if len(rects) == 0: return
        try:
            new_x = min(r.a.x for r in rects if self.isAlignedRight(r))
        except ValueError:              # If nothing is to the right
            new_x = area.b.x
        self.b = Point(new_x, self.b.y)
        self.c = Point(new_x, self.c.y)
        self.width_r = abs(new_x) - abs(self.p.x)
        self.calcCoords()
        self.calcField()
        self.calcVecs()

    def expandUp(self, rects, area) -> None:
        if len(rects) == 0: return
        try:
            new_y = min(r.a.y for r in rects if self.isAlignedUp(r))
        except ValueError:              # If nothing is to the left
            new_y = area.d.y
        self.c = Point(self.c.y, new_y)
        self.d = Point(self.d.y, new_y)
        self.height_u = abs(new_y) - abs(self.p.y)
        self.calcCoords()
        self.calcField()
        self.calcVecs()

    def expandDown(self, rects, area) -> None:
        if len(rects) == 0: return
        try:
            new_y = max(r.d.y for r in rects if self.isAlignedDown(r))
        except ValueError:              # If nothing is to the left
            new_y = area.a.y
        self.a = Point(self.a.y, new_y)
        self.b = Point(self.d.y, new_y)
        self.height_d = abs(self.p.y) + abs(new_y)
        self.calcCoords()
        self.calcField()
        self.calcVecs()


if __name__ == '__main__':
    rB = Rect(Point(50, 50), 100, 100)
    r = Rect(Point(5, 5), 4, 4)
    r2 = Rect(Point(0, 0), 2, 8)
    r3 = Rect(Point(10, 0), 2, 8)
    r4 = Rect(Point(3, 8), 8, 2)
    print(
        f"BORDER = {rB}, {r.isAlignedUp(rB)}\n"
        f"r = {r}, \n"
        f"r2 = {r2}, {r.isAlignedUp(r2)}, \n"
        f"r3 = {r3}, {r.isAlignedUp(r3)}, \n"
        f"r4 = {r4}, {r.isAlignedUp(r4)}")
    r.expandUp([r2, r3, r4], rB)
    print(f"Expanded r: {r}")
