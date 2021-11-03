from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x :int
    y :int

class Rectangle:
    def __init__(self, a :Point, width :int, height :int) -> None:
        self.width = width
        self.height = height

        #   d-----c
        #   |     |
        #   a-----b
        self.a = a
        self.b = Point(a.x + width, a.y)
        self.c = Point(a.x + width, a.y + height)
        self.d = Point(a.x, a.y + height)



if __name__ == '__main__':
    pnt = Point(1, 3)
