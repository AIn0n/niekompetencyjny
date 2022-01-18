import random
import unittest
from random import randint

from expandingModel.Room import *


class TestLocationChromosome(unittest.TestCase):
    def setUp(self) -> None:
        self.size = randint(3, 20)
        self.rooms = Room.generateRooms(self.size)
        print("\nGenerated rooms:")
        for room in self.rooms:
            print(room)

    def testRoomCount(self):
        self.assertEquals(self.size, len(self.rooms))


if __name__ == "__main__":
    unittest.main()
