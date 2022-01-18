import random
import unittest
from random import randint

from expandingModel.RoomTemplate import *


class TestLocationChromosome(unittest.TestCase):
    def setUp(self) -> None:
        self.size = randint(3, 20)
        self.rooms = RoomTemplate.generateRooms(self.size)
        print("\nGenerated rooms:")
        for room in self.rooms:
            print(room)

    def testRoomCount(self):
        self.assertEqual(self.size, len(self.rooms))


if __name__ == "__main__":
    unittest.main()
