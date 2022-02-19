import unittest
from src.geometry.Point import Point
from src.geometry.Rectangle import Rect
from src.RoomHandler import RoomHandler
from src.RoomTemplate import RoomTemplate


class TestRoomHandler(unittest.TestCase):
    def testGetLocatedRooms(self):
        rooms = [
            RoomTemplate("hall", 2, 2, True),
            RoomTemplate("kitchen", 6, 4, True),
        ]
        roomHandler = RoomHandler(rooms, None)
        rotations = [False, False]
        locations = [Point(2, 4), Point(3, 18)]
        result = roomHandler.getRotatedAndLocatedRooms(rotations, locations)
        self.assertEqual(result[0].p.x, locations[0].x)
        self.assertEqual(result[0].p.y, locations[0].y)
        self.assertEqual(result[1].p.x, locations[1].x)
        self.assertEqual(result[1].p.y, locations[1].y)

    def testOutOfArea(self):
        rooms = [
            RoomTemplate("hall", 2, 2, True),
            RoomTemplate("kitchen", 6, 4, True),
        ]
        rects = [x.getRectRef() for x in rooms]
        area = Rect(Point.zero(), 20, 20)
        roomHandler = RoomHandler(rooms, area)
        self.assertFalse(roomHandler.outOfArea(rects))

    def testOutOfAreaShouldReturnTrue(self):
        rooms = [
            RoomTemplate("hall", 2, 2, True),
            RoomTemplate("kitchen", 12, 4, True),
        ]
        rects = [x.getRectRef() for x in rooms]
        area = Rect(Point.zero(), 10, 10)
        roomHandler = RoomHandler(rooms, area)
        self.assertTrue(roomHandler.outOfArea(rects))

    def testAreCollisionsShouldReturnFalse(self):
        rects = [Rect(Point.zero(), 2, 2), Rect(Point(2, 0), 2, 4)]
        self.assertFalse(RoomHandler.areCollisions(rects))

    def testAreCollisionsShouldReturnTure(self):
        rects = [Rect(Point.zero(), 2, 2), Rect(Point(1, 0), 2, 4)]
        self.assertTrue(RoomHandler.areCollisions(rects))

    def testReadFromJson(self):
        roomHandler = RoomHandler.readFromJson("input_data/new_example.json")
        self.assertEqual(len(roomHandler.rooms), 3)
        self.assertEqual(len(roomHandler.doors), 3)
        self.assertEqual(
            roomHandler.allowList["expandable"], [True, True, False]
        )
        self.assertEqual(roomHandler.allowList["location"], [True, True, True])
        self.assertEqual(roomHandler.allowList["rotation"], [True, True, True])


if __name__ == "__main__":
    unittest.main()
