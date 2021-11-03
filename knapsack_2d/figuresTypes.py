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
        self.a = a
        self.calcCoords()

    def calcCoords(self):
        #   d-----c
        #   |     |
        #   a-----b
        self.b = Point(self.a.x + self.width, self.a.y)
        self.c = Point(self.a.x + self.width, self.a.y + self.height)
        self.d = Point(self.a.x, self.a.y + self.height)

    def __str__(self):
        return f"A - {self.a}, B - {self.b}, C - {self.c}, D = {self.d}"

    def moveX(self, offset: int) -> None:
        self.a = dataclasses.replace(self.a, x=self.a.x + offset)
        self.calcCoords()

    def moveY(self, offset: int) -> None:
        self.a = dataclasses.replace(self.a, y=self.a.y + offset)
        self.calcCoords()


# For testing purposes
if __name__ == '__main__':
    # Testing rect construction
    pnt = Point(1, 3)
    rect = Rectangle(pnt, 5, 10)
    print(rect)

    # Testing rect movement
    rect.moveX(-5)
    rect.moveY(100)
    print(rect)
