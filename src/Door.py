from geometry.Point import Point


class Door:
    def __init__(self, r1: str, r2: str, p=Point.zero()) -> None:
        self.pair = frozenset([r1, r2])
        self.point = p

    def copyAndSetPoint(self, p: Point):
        tmp = list(self.pair)
        tmp = Door(tmp[0], tmp[1])
        tmp.point = p
        return tmp

    def __hash__(self) -> int:
        return hash(self.pair)

    def __eq__(self, __o: object) -> bool:
        return self.pair == __o.pair

    def __str__(self) -> str:
        tmp = list(self.pair)
        return f"rooms = {tmp[0]}, {tmp[1]}: point = {self.point}"

    def __repr__(self) -> str:
        return str(self)
