import random

class Chromosome:
    def __init__(self, size):
        self.genes = [self.randGene() for x in range(size)]

    def randGene(self):
        pass
    
    def randomize(self) -> None:
        self.genes = map(self.randGene(), self.genes)
    
    def swap(self) -> None:
        (i1, i2) = random.choices(range(len(self.genes)), k = 2)
        self.genes[i1], self.genes[i2] = self.genes[i2], self.genes[i1]

    def replace(self) -> None:
        self.genes[random.choice(range(len(self.genes)))] = self.randGene()

    def inverse(self) -> None:
        (minI, maxI) = sorted(random.choices(range(len(self.genes))))
        self.genes = \
            self.genes[:minI] + \
            self.genes[minI:maxI][::-1] + \
            self.genes[maxI]

    def mutate(self, p) -> None:
        if random.uniform(0, 1) < p:
            random.choice([self.swap, self.replace, self.inverse])()