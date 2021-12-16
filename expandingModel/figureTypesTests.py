import unittest
from random import randint
from figureTypes import *
import math
from unittest.case import skip

class TestRectClass(unittest.TestCase):

    def testConctructorVariables(self):
        w, h = randint(1, 127) * 2, randint(1, 127) * 2
        p = Point(0, 0)
        r = Rect(p, w, h)
        self.assertTrue(r.p == p)
        self.assertTrue(r.width_l == w//2)
        self.assertTrue(r.width_r == w//2)
        self.assertTrue(r.height_u == h//2)
        self.assertTrue(r.height_d == h//2)
        self.assertTrue(r.field == w*h)
        self.assertTrue(r.a == Point(p.x - w/2, p.y - h/2))
        self.assertTrue(r.b == Point(p.x + w/2, p.y - h/2))
        self.assertTrue(r.c == Point(p.x + w/2, p.y + h/2))
        self.assertTrue(r.d == Point(p.x - w/2, p.y + h/2))

    def testCollidesWithInnerRect(self):
        w1, h1 = randint(16, 127) * 2, randint(16, 127) * 2
        w2, h2 = randint(1, 127) * 2, randint(1, 127) * 2
        p = Point(0, 0)
        outer, inner = Rect(p, w1, h1), Rect(p, w2, h2)
        self.assertTrue(outer.collides(inner))
        self.assertTrue(inner.collides(outer))

    def testCollidesWithNonColliding(self):
        w1, h1 = randint(1, 16) * 2, randint(1, 16) * 2
        w2, h2 = randint(1, 16) * 2, randint(1, 16) * 2
        p1, p2 = Point(0, 0), Point(randint(31, 64), randint(31, 64))
        r1, r2 = Rect(p1, w1, h1), Rect(p2, w2, h2)
        self.assertFalse(r1.collides(r2))
        self.assertFalse(r2.collides(r1))

    def testCollidesWithTouchingWalls(self):
        r1, r2 = Rect(Point(0, 0), 6, 2), Rect(Point(5, 0), 4, 2)
        self.assertFalse(r1.collides(r2))
        self.assertFalse(r2.collides(r1))

    def testCollidesWithColliding(self):
        w, h = randint(17, 25), randint(17, 25)
        w, h = w + w % 2, h + h % 2
        r1 = Rect(Point(0, 0), 16, 16)
        r2 = Rect(Point(16, 16), w, h)
        self.assertTrue(r1.collides(r2))
        self.assertTrue(r2.collides(r1))

    def testContainRectWithContaining(self):
        zero_p = Point(0, 0)
        inner = Rect(zero_p, randint(1, 8) * 2, randint(1, 8) * 2)
        outer = Rect(zero_p, randint(16, 32) * 2, randint(16, 32) * 2)
        self.assertTrue(outer.containsRectangle(inner))
        self.assertFalse(inner.containsRectangle(outer))

    def testContainRectWithNonContaining(self):
        r1, r2 = Rect(Point(0, 0), 8, 6), Rect(Point(4, 0), 8, 6)
        self.assertFalse(r1.containsRectangle(r2) or r2.containsRectangle(r1))

    def testCloneOffset(self):
        r = Rect(Point(0, 0), 8, 8)
        new = r.cloneOffset(Point(5, 5))
        self.assertEqual(new.p, Point(5, 5))
        self.assertEqual(new.field, r.field)
        self.assertEqual(new.height_d, r.height_d)
        self.assertEqual(new.width_l, r.width_l)

    def testGetHorizontalVectors(self):
        r = Rect(Point(0, 0),randint(1, 16) * 2, randint(1, 16) * 2)
        self.assertEqual(r.getHorVecs(), [Vec(r.a, r.b), Vec(r.d, r.c)])
    
    def testGetVerticalVectors(self):
        r = Rect(Point(0, 0),randint(1, 16) * 2, randint(1, 16) * 2)
        self.assertEqual(r.getVerVecs(), [Vec(r.a, r.d), Vec(r.b, r.c)])

    def testExpandRightSameX(self):
        area = Rect(Point(0, 0), 100, 100)
        r1, r2 = Rect(Point(0,0), 2, 8), Rect(Point(10,0), 2, 8)
        r1.expandRight([r2], area)
        self.assertEqual(r1.b.x, 9)
        self.assertEqual(r1.c.x, 9)
        self.assertEqual(r1.width_r, 9)
        self.assertEqual(r1.field, 10 * 8)

    def testExpandRightLilAbove(self):
        area = Rect(Point(0, 0), 100, 100)
        r1, r2 = Rect(Point(0,0), 2, 8), Rect(Point(10,8), 2, 8)
        r1.expandRight([r2], area)
        self.assertEqual(r1.b.x, area.width_r)
        self.assertEqual(r1.c.x, area.width_r)
        self.assertEqual(r1.width_r, area.width_r)
        self.assertEqual(r1.field, (area.width_r + r1.width_l) * 8)

    def testGetHeightWidthSquare(self):
        length = randint(1, 50) * 2
        square = Rect(Point(0, 0), length, length)
        self.assertEqual(square.getWidth(), length)
        self.assertEqual(square.getHeight(), length)

    def testGetHeightWidthRectangle(self):
        width = randint(1, 50) * 2
        height = randint(1, 50) * 2
        rectangle = Rect(Point(0, 0), width, height)
        self.assertEqual(rectangle.getWidth(), width)
        self.assertEqual(rectangle.getHeight(), height)

    def testGetHeightWidthExpandLeftRight(self):
        area = Rect(Point(0, 0), randint(50, 100) * 2, randint(50, 100) * 2)
        width = randint(1, 50) * 2
        height = randint(1, 50) * 2
        rectangle = Rect(Point(0, 0), width, height)
        print(f"{area}, width = {area.getWidth()}, width_r = {area.width_r}")
        print(f"{rectangle}, width = {rectangle.getWidth()}")
        rectangle.expandLeft([], area)
        rectangle.expandRight([], area)
        print(f"{rectangle}, width = {rectangle.getWidth()}")
        self.assertEqual(rectangle.getWidth(), area.getWidth())

    def testGetHeightWidthExpandUpDown(self):
        area = Rect(Point(0, 0), randint(50, 100) * 2, randint(50, 100) * 2)
        offsetX = randint(0, 50)
        offsetY = randint(0, 50)
        width = randint(1, 20) * 2
        height = randint(1, 20) * 2
        rectangle = Rect(Point(offsetX, offsetY), width, height)
        rectangle.expandUp([], area)
        rectangle.expandDown([], area)
        self.assertEqual(rectangle.getHeight(), area.getHeight())


class TestPointClass(unittest.TestCase):

    def test_str(self):
        x, y = randint(0, 255), randint(0, 255)
        p = Point(x=x, y=y)
        self.assertEqual(f'({x}, {y})', str(p))

if __name__ == '__main__':
    unittest.main()