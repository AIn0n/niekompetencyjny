from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x :int
    y :int

class Rectangle:
    def __init__(self, a :Point, b :Point, c :Point, d :Point) -> None:
#   c-----d
#   |     |
#   a-----b
        self.a = a
        self.b = b
        self.c = c
        self.d = d