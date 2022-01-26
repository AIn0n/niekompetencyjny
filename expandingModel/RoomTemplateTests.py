import unittest
from random import randint, choice

from expandingModel.JsonIO import JsonIO
from expandingModel.RoomTemplate import *


class TestTemplatesRandom(unittest.TestCase):
    def setUp(self) -> None:
        self.size = randint(3, 20)
        self.rooms = RoomTemplate.generateRooms(self.size)
        print("\nGenerated rooms:")
        for room in self.rooms:
            print(room)

    def testRoomCount(self):
        self.assertEqual(self.size, len(self.rooms))


class TestTemplatesJson(unittest.TestCase):
    def setUp(self) -> None:
        file = "input_data/example.json"
        self.field, self.templates = JsonIO.read(file)

    def testValidate(self):
        for template in self.templates:
            self.assertTrue(template.validate(self.field))

    def testValidateTooNarrow(self):
        altered = choice(self.templates)
        # Make a random minWidth negative
        altered.minWidth *= -1
        # ...including zeros
        altered.minWidth -= 1

        invalidCount = 0
        for template in self.templates:
            if not template.validate(self.field):
                invalidCount += 1
        self.assertEqual(invalidCount, 1)

    def testValidateTooShort(self):
        altered = choice(self.templates)
        # Make a random minWidth negative
        altered.minHeight *= -1
        # ...including zeros
        altered.minHeight -= 1

        invalidCount = 0
        for template in self.templates:
            if not template.validate(self.field):
                invalidCount += 1
        self.assertEqual(invalidCount, 1)

    def testValidateTooWide(self):
        altered = choice(self.templates)
        # Make a random minWidth exceed the field's width
        altered.minWidth = self.field.getWidth() + 1

        invalidCount = 0
        for template in self.templates:
            if not template.validate(self.field):
                invalidCount += 1
        self.assertEqual(invalidCount, 1)

    def testValidateTooHigh(self):
        altered = choice(self.templates)
        # Make a random minHeight exceed the field's width
        altered.minHeight = self.field.getHeight() + 1

        invalidCount = 0
        for template in self.templates:
            if not template.validate(self.field):
                invalidCount += 1
        self.assertEqual(1, invalidCount)

    def testName(self):
        altered = choice(self.templates)
        # Make a random name blank
        altered.name = ""

        invalidCount = 0
        for template in self.templates:
            if not template.validate(self.field):
                invalidCount += 1
        self.assertEqual(1, invalidCount)


if __name__ == "__main__":
    unittest.main()
