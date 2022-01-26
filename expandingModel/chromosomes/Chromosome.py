import random


class ChromMask:
    def __init__(self, mask: list, values: list) -> None:
        self.mask = mask
        self.values = values


class Chromosome:
    def __init__(self, size: int, mask=None):
        self.genes = [self.randGene() for _ in range(size)]
        if mask:
            self.mask = mask
        else:
            self.mask = ChromMask([0 for _ in range(size)], 0)

    def randGene(self):
        pass

    def __getitem__(self, key):
        return self.genes[key]

    def __len__(self):
        return len(self.genes)

    def checkMask(self, n):
        if self.mask.mask[n]:
            self.genes[n] = self.mask.values[n]

    def checkMaskAll(self):
        for i in range(len(self.genes)):
            self.checkMask(i)

    def setGenes(self, newGenes) -> None:
        self.genes = newGenes
        self.checkMaskAll()

    def setGene(self, n, val) -> None:
        self.genes[n] = val
        self.checkMask(n)

    def randomize(self) -> None:
        self.genes = map(self.randGene(), self.genes)
        self.checkMaskAll()

    def swap(self) -> None:
        (i1, i2) = random.choices(range(len(self.genes)), k=2)
        self.genes[i1], self.genes[i2] = self.genes[i2], self.genes[i1]
        self.checkMask(i1)
        self.checkMask(i2)

    def replace(self) -> None:
        n = random.choice(range(len(self.genes)))
        self.setGene(n, self.randGene())
        self.checkMask(n)

    def inverse(self) -> None:
        (minI, maxI) = sorted(random.choices(range(len(self.genes)), k=2))
        self.genes = (
            self.genes[:minI] + self.genes[minI:maxI][::-1] + self.genes[maxI:]
        )
        self.checkMaskAll()

    def mutate(self, p) -> None:
        if random.uniform(0, 1) < p:
            random.choice([self.swap, self.replace, self.inverse])()
