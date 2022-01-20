import PathFinding
from Path import Path
from RoomTemplate import RoomTemplate
from Door import Door
from figures.figures import Rect, Point


class Room:
    def __init__(self, template: RoomTemplate, rect: Rect):
        self.template = template
        self.rect = rect
        self.doors = set()
        self.name = self.template.name
        # todo: Implement data validation

    def addDoor(self, door: Door):
        # todo: Add a method that checks if a point lies on a Rect's border
        self.doors.add(door)
        # Adds the door to the room it's supposed to lead to
        if not door.leadsTo.doors.__contains__(door):
            door.leadsTo.addDoor(Door(door.coords, self))

    def __str__(self):
        return self.name


templates = RoomTemplate.generateRooms(4)
roomA = Room(templates[0], Rect(Point(5, 5), 10, 10))
roomB = Room(templates[1], Rect(Point(15, 5), 10, 10))
roomC = Room(templates[2], Rect(Point(10, -5), 10, 10))
roomD = Room(templates[3], Rect(Point(25, 5), 10, 10))

roomA.name = "A"
roomB.name = "B"
roomC.name = "C"
roomD.name = "D"

roomA.addDoor(Door(Point(10, 9), roomB))
roomA.addDoor(Door(Point(6, 0), roomC))
roomC.addDoor(Door(Point(12, 0), roomB))
roomB.addDoor(Door(Point(20, 5), roomD))


path = PathFinding.propagatePath(Point(10, -5), roomC, roomD, Path(0, set()))
print("Found path's flag:", path.flag)
print("Found path:", path)
