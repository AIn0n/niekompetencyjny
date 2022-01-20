from figures.figures import Point


class Door:
    def __init__(self, coords: Point, leadsTo):
        self.coords = coords
        self.leadsTo = leadsTo

    def __eq__(self, other):
        return self.coords == other.coords

    def __ne__(self, other):
        return self.coords != other.coords

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return str(self.coords) + " -> " + str(self.leadsTo)
