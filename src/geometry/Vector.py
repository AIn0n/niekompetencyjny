from .Point import Point


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
        # A Vec object can only be vertical or horizontal, therefore one of
        # these is always 0
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
        if self == other:
            return True
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
