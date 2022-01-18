import unittest
from random import randint
from LocationChromosome import LocationChromosome as lChrsom
from BinaryChromosome import BinaryChromosome as BinChrsom


class TestLocationChromosome(unittest.TestCase):
    def testConstructor(self):
        size = randint(1, 255)
        rX = (randint(0, 16), randint(16, 32))
        rY = (randint(0, 16), randint(16, 32))
        new = lChrsom(size, rY, rX)
        self.assertEqual(size, len(new.genes))
        self.assertEqual(rX, new.rX)
        self.assertEqual(rY, new.rY)

    def testRandGene(self):
        rX = (randint(0, 16), randint(16, 32))
        rY = (randint(0, 16), randint(16, 32))
        new = lChrsom(randint(0, 255), rY, rX)
        for gene in new.genes:
            self.assertTrue(rX[0] <= gene.x <= rX[1])
            self.assertTrue(rY[0] <= gene.y <= rY[1])


class TestBinaryChromosome(unittest.TestCase):
    def testConstructorAndRandGene(self):
        size = randint(0, 255)
        new = BinChrsom(size)
        self.assertEqual(len(new.genes), size)
        for num in new.genes:
            self.assertTrue(0 <= num <= 1)


if __name__ == "__main__":
    unittest.main()
