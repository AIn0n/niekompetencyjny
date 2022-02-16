class RoomHandler:
    def __init__(self, rooms, area) -> None:
        self.rooms = rooms
        self.area = area
        self.allowList = dict()
        self.doors = []

    def getRotatedAndLocatedRooms(self, rotations: list, locations: list) -> list:
        assert(len(self.rooms) == len(rotations) == len(locations))
        result = []
        for room, rotation, location in zip(self.rooms, rotations, locations):
            result.append(room.getRectRef(rotation).cloneOffset(location))
        return result

    def outOfArea(self, rects: list) -> bool:
        assert(len(rects) > 0)
        return any(map(lambda x: not self.area.containsRectangle(x), rects))

    @staticmethod
    def areCollisions(rects: list) -> bool:
        for i in range(len(rects)):
            for j in range(len(rects)):
                pass
