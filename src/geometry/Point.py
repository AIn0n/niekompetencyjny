from dataclasses import dataclass
import math


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
