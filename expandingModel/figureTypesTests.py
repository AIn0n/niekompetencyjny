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
        self.assertTrue(r.width_l == w // 2)
        self.assertTrue(r.width_r == w // 2)
        self.assertTrue(r.height_u == h // 2)
        self.assertTrue(r.height_d == h // 2)
        self.assertTrue(r.field == w * h)
        self.assertTrue(r.a == Point(p.x - w / 2, p.y - h / 2))
        self.assertTrue(r.b == Point(p.x + w / 2, p.y - h / 2))
        self.assertTrue(r.c == Point(p.x + w / 2, p.y + h / 2))
        self.assertTrue(r.d == Point(p.x - w / 2, p.y + h / 2))

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
        r = Rect(Point(0, 0), randint(1, 16) * 2, randint(1, 16) * 2)
        (vec1, vec2) = r.getHorVecs()
        self.assertEqual(r.getHorVecs(), [Vec(r.a, r.b), Vec(r.d, r.c)])

    def testGetVerticalVectors(self):
        r = Rect(Point(0, 0), randint(1, 16) * 2, randint(1, 16) * 2)
        self.assertEqual(r.getVerVecs(), [Vec(r.a, r.d), Vec(r.b, r.c)])

    def testExpandRightSameX(self):
        area = Rect(Point(0, 0), 100, 100)
        r1, r2 = Rect(Point(0, 0), 2, 8), Rect(Point(10, 0), 2, 8)
        r1.expandRight([r2], area)
        self.assertEqual(r1.b.x, 9)
        self.assertEqual(r1.c.x, 9)
        self.assertEqual(r1.width_r, 9)
        self.assertEqual(r1.field, 10 * 8)

    def testExpandRightLilAbove(self):
        area = Rect(Point(0, 0), 100, 100)
        r1, r2 = Rect(Point(0, 0), 2, 8), Rect(Point(10, 8), 2, 8)
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
        # print(f"{area}, width = {area.getWidth()}, width_r = {area.width_r}")
        # print(f"{rectangle}, width = {rectangle.getWidth()}")
        rectangle.expandLeft([], area)
        rectangle.expandRight([], area)
        # print(f"{rectangle}, width = {rectangle.getWidth()}")
        self.assertEqual(rectangle.getWidth(), area.getWidth())
        self.assertEqual(
            rectangle.getWidth(), rectangle.width_l + rectangle.width_r
        )
        self.assertEqual(
            rectangle.getHeight(), rectangle.height_d + rectangle.height_u
        )

    def testCollidesSameOrient1(self):
        vec1 = Vec(Point(0, 0), Point(0, randint(5, 10)))
        vec2 = Vec(Point(0, 0), Point(0, randint(1, vec1.end.y)))
        self.assertTrue(vec1.collidesSameOrient(vec2))
        self.assertTrue(vec2.collidesSameOrient(vec1))

    def testCollidesSameOrient2(self):
        vec1 = Vec(Point(0, 0), Point(randint(5, 10), 0))
        vec2 = Vec(Point(0, 0), Point(randint(1, vec1.end.x), 0))
        self.assertTrue(vec1.collidesSameOrient(vec2))
        self.assertTrue(vec2.collidesSameOrient(vec1))

    def testCollidesSameOrient3(self):
        vec1 = Vec(Point(0, 0), Point(randint(5, 10), 0))
        vec2 = Vec(Point(vec1.end.x, 0), Point(randint(1, randint(1, 5)), 0))
        self.assertFalse(vec1.collidesSameOrient(vec2))
        self.assertFalse(vec2.collidesSameOrient(vec1))

    def testCollidesSameOrient4(self):
        vec1 = Vec(Point(randint(0, 5), 0), Point(randint(5, 10), 0))
        vec2 = Vec(Point(vec1.start.x, 0), Point(vec1.end.x, 0))
        self.assertTrue(vec1.collidesSameOrient(vec2))
        self.assertTrue(vec2.collidesSameOrient(vec1))

    def testCollidesSameOrient5(self):
        vec1 = Vec(Point(randint(0, 5), 0), Point(randint(5, 10), 0))
        vec2 = Vec(Point(vec1.start.x - 1, 0), Point(vec1.end.x + 1, 0))
        self.assertTrue(vec1.collidesSameOrient(vec2))
        self.assertTrue(vec2.collidesSameOrient(vec1))

    def testNeighbours1(self):
        rect1 = Rect(Point(2, 2), 2, 2)
        rect2 = Rect(Point(0, 2), 2, 2)
        expected = Vec(Point(1, 1), Point(1, 3))
        self.assertEqual(rect1.neighbours(rect2), expected)

    def testNeighbours2(self):
        rect1 = Rect(Point(2, 2), 2, 2)
        rect2 = Rect(Point(-1, 2), 2, 2)
        self.assertFalse(rect1.neighbours(rect2))

    def testCommonPartX1(self):
        y = randint(-100, 100)
        start1 = Point(randint(-100, -50), y)
        end1 = Point(randint(0, 50), y)

        start2 = Point(randint(-50, 0), y)
        end2 = Point(randint(50, 100), y)

        vec1 = Vec(start1, end1)
        vec2 = Vec(start2, end2)

        result1 = vec1.commonPart(vec2)
        result2 = vec2.commonPart(vec1)
        self.assertEqual(result1, result2)


    def testCommonPartX2(self):
        y = randint(-100, 100)

        start1 = Point(randint(-100, -50), y)
        end1 = Point(randint(0, 50), y)

        start2 = Point(randint(-50, 0), y)
        end2 = Point(randint(50, 100), y)

        vec1 = Vec(start1, end1)
        vec2 = Vec(start2, end2)

        result = vec1.commonPart(vec2)
        print(vec1, vec2, result, sep="\n")
        self.assertEqual(result, Vec(vec2.start, vec1.end))


    def testCommonPartX3(self):
        y = randint(-100, 100)

        start1 = Point(randint(-100, -50), y)
        end1 = Point(randint(50, 100), y)

        start2 = Point(randint(-50, 0), y)
        end2 = Point(randint(0, 50), y)

        vec1 = Vec(start1, end1)
        vec2 = Vec(start2, end2)

        result = vec1.commonPart(vec2)
        self.assertEqual(result, Vec(vec2.start, vec2.end))


    def testCommonPartX4(self):
        y = randint(-100, 100)

        start1 = Point(randint(-100, -50), y)
        end1 = Point(randint(0, 50), y)

        start2 = Point(randint(-50, 0), y)
        end2 = Point(randint(50, 100), y)

        vec1 = Vec(start1, end1)
        vec2 = Vec(start2, end2)

        result = vec1.commonPart(vec2)
        print(vec1, vec2, result, sep="\n")
        self.assertEqual(result, Vec(start2, end1))

    def testNeighbours3(self):
        rect1 = Rect(Point(2, 2), 2, 2)
        rect2 = Rect(Point(0, 0), 2, 2)
        self.assertFalse(rect1.neighbours(rect2))

    def testNeighboursInner(self):
        inner = Rect(Point(1, 0), 2, 2)
        outer = Rect(Point.zero(), 4, 4)
        expected = set([Vec(Point(2, -1), Point(2, 1))])
        self.assertEqual(inner.neighbours(outer), expected)

    def testNeighboursEdgeCase(self):
        rect1 = Rect(Point.zero(), 4, 4)
        rect2 = Rect(Point(1, 1), 2, 2)
        expected = set(
            [Vec(Point.zero(), Point(2, 0)), Vec(Point(0, 2), Point(2, 2))]
        )
        self.assertEqual(set(rect1.neighbours(rect2)), expected)

    def testExpand(self):
        rB = Rect(Point(50, 50), 100, 100)
        r = Rect(Point(5, 5), 4, 4)
        r2 = Rect(Point(0, 0), 2, 8)
        r3 = Rect(Point(10, 0), 2, 8)
        r4 = Rect(Point(3, 8), 8, 2)
        print(
            f"BORDER = {rB}, {r.isAlignedUp(rB)}\n"
            f"r = {r}, \n"
            f"r2 = {r2}, {r.isAlignedUp(r2)}, \n"
            f"r3 = {r3}, {r.isAlignedUp(r3)}, \n"
            f"r4 = {r4}, {r.isAlignedUp(r4)}"
        )
        r.expandUp([r2, r3, r4], rB)
        print(f"Expanded r: {r}")

class TestPointClass(unittest.TestCase):
    def test_str(self):
        x, y = randint(0, 255), randint(0, 255)
        p = Point(x=x, y=y)
        self.assertEqual(f"({x}, {y})", str(p))


if __name__ == "__main__":
    unittest.main()
