from random import Random
import pygame
from genAlgorithm import *
import pickle

class PrintAlg:
    display_width = 720
    display_height = 480
    white = (255, 255, 255)

    def __init__(self, fieldWidth, fieldHeight) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.plot_display = pygame.display.set_mode((self.display_width, self.display_height))
        self.plot_display.fill(self.white)

        self.inter_display = pygame.Surface((fieldWidth, fieldHeight))
        self.inter_display.blit(pygame.transform.flip(self.inter_display, False, True), (0, 0))

        self.offX = fieldWidth/2
        self.offY = fieldHeight/2

    def getCords(self, x, y):
        return (x + self.offX,
                y + self.offY)

    def printRect(self, r: Rect, color: tuple) -> None:
        x, y = self.getCords(r.a.x, r.a.y)
        pygame.draw.rect(self.inter_display, color,
                         (x, y, r.width_l + r.width_r, r.height_u + r.height_d))

    def printAll(self) -> None:
        self.scaleSurface()
        self.plot_display.blit(self.inter_display, (0, 0))
        pygame.display.flip()

    def scaleSurface(self) -> None:
        self.inter_display = pygame.transform.scale(self.inter_display, (self.display_height, self.display_height))


area = Rect(Point(0, 0), 80, 80)
squares = tuple([
    Rect(Point(0, 0), 2, 4),
    Rect(Point(0, 0), 4, 6),
    Rect(Point(0, 0), 12, 2),
    Rect(Point(0, 0), 8, 4),
    Rect(Point(0, 0), 8, 6),
    Rect(Point(0, 0), 4, 10)])

fitCls = FitnessClass(area, squares)
genAlg = GeneticAlgorithm(100, 0.2, 0.1, fitCls)
genAlg.repeat(1)
bestSpecimen = max(genAlg.generation, key=lambda x: x.fitness)
print(bestSpecimen)
print(bestSpecimen.fitness)

area = Rect(Point(0, 0), 100, 100)
r = [Rect(Point(5, 5), 4, 4), Rect(Point(0, 0), 2, 8), Rect(Point(10, 0), 2, 8), Rect(Point(3, 8), 8, 2)]

for n in range(len(r)):
    curr = r.pop(0)
    curr.expandUp(r, area)
    curr.expandLeft(r, area)
    curr.expandRight(r, area)
    curr.expandDown(r, area)
    r.append(curr)

printer = PrintAlg(area.width_l, area.height_d)
[printer.printRect(n, [random.randint(0, 255) for n in range(3)]) for n in r]

printer.printAll()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()