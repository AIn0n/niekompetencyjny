import random
from random import randint


class Room:
    def __init__(
        self, name: str, minWidth: int, minHeight: int, expandable: bool
    ) -> None:
        self.name = name
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.expandable = expandable
        self.neighbours = set()

    def addNeighbour(self, neighbour):
        # Implement neighbour validation
        self.neighbours.add(neighbour.name)
        neighbour.neighbours.add(self.name)

    def __str__(self):
        return (
            f"{self.name}, at least {self.minWidth}x{self.minHeight}, expandable = {self.expandable},"
            f" neighbours: {self.neighbours}"
        )

    ######### RANDOM ROOM GENERATION #########
    @staticmethod
    def generateName():
        return "".join(
            random.choice([chr(i) for i in range(ord("a"), ord("z"))])
            for _ in range(randint(6, 12))
        )

    @staticmethod
    def generateRoomNoConnections():
        return Room(
            Room.generateName(),
            randint(2, 20),
            randint(2, 20),
            random.choice([True, False]),
        )

    @staticmethod
    def generateRooms(count):
        rooms = list()
        for i in range(count):
            # Implement something to counter duplicates
            rooms.append(Room.generateRoomNoConnections())

        for room in rooms:
            # Pool of unique non-self rooms
            otherRooms = rooms.copy()
            otherRooms.remove(room)

            for i in range(randint(0, 2)):
                # Selecting a random valid neighbour
                randomRoom = random.choice(otherRooms)
                otherRooms.remove(randomRoom)
                room.addNeighbour(randomRoom)
        return rooms
