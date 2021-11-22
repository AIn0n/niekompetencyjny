import unittest
from random import randint
from figureTypes import *
import math
from unittest.case import skip

class TestRectClass(unittest.TestCase):

    def testConstructorVariables(self):
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

    def testExpandLeft(self):
        x1, x2 = randint(2, 8)*2, randint(9, 16)*2
        r = Rect(Point(0, 0), 2, 6)
        r1 = Rect(Point(-x1-1, -1), 2, 6)
        r2 = Rect(Point(-x2-1, -1), 2, 6)
        r.expandLeft([r1, r2])
        self.assertEqual(r.width_l, x1)
        self.assertEqual(r.field, (x1 + 1) * 6)
        self.assertEqual(r.a.x, -x1)
        self.assertEqual(r.d.x, -x1)
        

class TestPointClass(unittest.TestCase):

    def test_str(self):
        x, y = randint(0, 255), randint(0,255)
        p = Point(x=x, y=y)
        self.assertEqual(f'({x}, {y})', str(p))

class TestVecClass(unittest.TestCase):
    @skip
    def testGetLen(self):
        start, end = [Point(randint(0, 16), randint(0, 16)) for n in [0, 1]]
        vec = Vec(start, end)
        self.assertEqual(vec.getDistance(), 
            math.sqrt(abs(start.x - end.x) ** 2 + abs(start.y - end.y)))
