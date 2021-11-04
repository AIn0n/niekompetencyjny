import dataclasses
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"


class Rectangle:
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
        return (other.a.x <= self.a.x) and (other.a.y <= self.a.y) and (self.c.x <= self.c.x) and (self.c.y <= other.c.y)

    def __str__(self):
        return f"A - {self.a}, B - {self.b}, C - {self.c}, D = {self.d}"

    def moveX(self, offset: int) -> None:
        self.a = dataclasses.replace(self.a, x=self.a.x + offset)
        self.calcCoords()

    def moveY(self, offset: int) -> None:
        self.a = dataclasses.replace(self.a, y=self.a.y + offset)
        self.calcCoords()

    def cloneOffset(self, offset: Point):
        newCoords = Point(self.a.x + offset.x, self.a.y + offset.y)
        return Rectangle(newCoords, self.width, self.height)

# For testing purposes
if __name__ == '__main__':
    # Testing rect construction
    pnt = Point(0, 0)
    rect = Rectangle(pnt, 5, 10)
    print(rect)

    # Testing rect movement
    #rect.moveX(0)
    #rect.moveY(0)
    #print(rect)

    rect2 = Rectangle(pnt, 5, 10)
    rect2.moveX(600)
    print(rect2)
    print(rect.collides(rect2))

    rectMoved = rect.cloneOffset(Point(10, 10))
    print(rectMoved)
