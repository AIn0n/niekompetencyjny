import json

from src.RoomTemplate import RoomTemplate


class RoomHandler:
    def __init__(self, rooms, area) -> None:
        self.rooms = rooms
        self.area = area
        self.allowList = dict()
        self.doors = []

    @staticmethod
    def readFromJson(path: str) -> None:
        assert len(path)
        res = RoomHandler([], None)
        with open(path, "r") as f:
            data = json.load(f)
            for r in data:
                room = RoomTemplate(
                    r["name"], r["minSize"][0], r["minSize"][1], r["expandable"]
                )
                for n in r["neighbours"]:
                    room.addNeighbourString(n)
                if r["name"] == "area":
                    res.area = room
                else:
                    res.rooms.append(room)

    def getRotatedAndLocatedRooms(
        self, rotations: list, locations: list
    ) -> list:
        assert len(self.rooms) == len(rotations) == len(locations)
        result = []
        for room, rotation, location in zip(self.rooms, rotations, locations):
            result.append(room.getRectRef(rotation).cloneOffset(location))
        return result

    def outOfArea(self, rects: list) -> bool:
        assert len(rects) > 0
        return any(map(lambda x: not self.area.containsRectangle(x), rects))

    @staticmethod
    def areCollisions(rects: list) -> bool:
        assert len(rects) > 1
        for i in range(len(rects)):
            for j in range(len(rects)):
                if i != j and rects[i].collides(rects[j]):
                    return True
        return False
