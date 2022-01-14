import random
from random import randint

from figureTypes import Point, Rect

class RoomTemplate:
    def __init__(self, name: str, minWidth: int, minHeight: int, expandable: bool) -> None:
        self.name = name
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.expandable = expandable
        # Replace with a dict?
        self.neighbours = set()

    def addNeighbour(self, neighbour) -> None:
        # todo: Implement neighbour validation
        self.neighbours.add(neighbour.name)
        neighbour.neighbours.add(self.name)

    def addNeighbour(self, neighbour: str) -> None:
        self.neighbours.add(neighbour)

    def getRectRef(self, reverse = False) -> Rect:
        return Rect(Point.zero(), self.minWidth, self.minHeight) if not reverse\
            else Rect(Point.zero(), self.minHeight, self.minWidth)

    def __eq__(self, __o: object) -> bool:
        if(type(__o)==type(self)):
            return  self.name       == __o.name         and\
                    self.minHeight  == __o.minHeight    and\
                    self.minWidth   == __o.minWidth     and\
                    self.expandable == __o.expandable   and\
                    self.neighbours == __o.neighbours
        return False

    def __str__(self):
        return f"{self.name}, at least {self.minWidth}x{self.minHeight}, expandable = {self.expandable}," \
               f" neighbours: {self.neighbours}"

    ######### RANDOM ROOM GENERATION #########
    @staticmethod
    def generateName():
        return ''.join(random.choice([chr(i) for i in range(ord('a'), ord('z'))]) for _ in range(randint(6, 12)))

    @staticmethod
    def generateRoomNoConnections():
        return RoomTemplate(RoomTemplate.generateName(), randint(2, 20), randint(2, 20), random.choice([True, False]))

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
                randomRoom = random.choice(otherRooms)
                otherRooms.remove(randomRoom)
                room.addNeighbour(randomRoom)
        return rooms
