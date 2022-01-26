from random import randint, choice

from figures.figures import Point, Rect


class RoomTemplate:
    def __init__(
        self, name: str, minWidth: int, minHeight: int, expandable: bool
    ) -> None:
        self.name = name
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.expandable = expandable
        self.exit = False
        # Replace with a dict?
        self.neighbours = set()

    # EXTERNALLY ACTIVATED, REMEMBER TO USE
    def validate(self, field: Rect):
        return (
            len(self.name) > 0
            and 0 < self.minWidth <= field.getWidth()
            and 0 < self.minHeight <= field.getHeight()
        )

    def addNeighbour(self, neighbour) -> None:
        # todo: Implement neighbour validation
        self.neighbours.add(neighbour.name)
        neighbour.neighbours.add(self.name)

    def addNeighbourString(self, neighbour: str) -> None:
        self.neighbours.add(neighbour)

    def getRectRef(self, reverse=False) -> Rect:
        return (
            Rect(Point.zero(), self.minWidth, self.minHeight)
            if not reverse
            else Rect(Point.zero(), self.minHeight, self.minWidth)
        )

    def __eq__(self, __o: object) -> bool:
        if type(__o) == type(self):
            return self.name == __o.name
        return False

    def __str__(self):
        return (
            f"{self.name}, at least {self.minWidth}x{self.minHeight}, expandable = {self.expandable},"
            f" neighbours: {self.neighbours}"
        )

    def __hash__(self):
        return hash(str(self))

    ######### RANDOM ROOM GENERATION, FOR TESTING PURPOSES #########
    @staticmethod
    def generateName():
        return "".join(
            choice([chr(i) for i in range(ord("a"), ord("z"))])
            for _ in range(randint(6, 12))
        )

    @staticmethod
    def generateRoomNoConnections():
        return RoomTemplate(
            RoomTemplate.generateName(),
            randint(2, 20),
            randint(2, 20),
            choice([True, False]),
        )

    @staticmethod
    def generateRooms(count):
        rooms = list()
        for i in range(count):
            # Implement something to counter duplicates
            rooms.append(RoomTemplate.generateRoomNoConnections())

        for room in rooms:
            # Pool of unique non-self rooms
            otherRooms = rooms.copy()
            otherRooms.remove(room)

            for i in range(randint(0, 2)):
                # Selecting a random valid neighbour
                randomRoom = choice(otherRooms)
                otherRooms.remove(randomRoom)
                room.addNeighbour(randomRoom)
        return rooms
