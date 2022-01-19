from pickle import TRUE
import unittest

from JsonIO import JsonIO
from RoomTemplate import RoomTemplate
from figureTypes import Point, Rect


class JsonIOTests(unittest.TestCase):
    def testJsonRead(self):
        file = "expandingModel/input_data/example.json"
        area, rooms = JsonIO.read(file)
        expected = [
            RoomTemplate("hall", 2, 2, True),
            RoomTemplate("kitchen", 10, 5, True),
            RoomTemplate("elevator", 4, 8, False),
        ]

        expected[0].addNeighbour("kitchen")
        expected[0].addNeighbour("elevator")
        expected[1].addNeighbour("hall")
        expected[2].addNeighbour("hall")
        for elem in rooms:
            self.assertTrue(elem in expected)
            if elem.name == "hall":
                self.assertTrue(elem.exit)
            else:
                self.assertFalse(elem.exit)
        self.assertEqual(area, Rect(Point.zero(), 20, 20))
        self.assertEqual(len(rooms), len(expected))


if __name__ == "__main__":
    unittest.main()
