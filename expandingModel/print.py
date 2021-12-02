import pygame
import random
from figureTypes import *
from genAlgorithm import *

class PrintAlg:
    display_width = 1280
    display_height = 820
    white = (255, 255, 255)

    def __init__(self, offsetX, offsetY) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.plot_display = pygame.display.set_mode((self.display_width, self.display_height))
        self.plot_display.fill(self.white)
        self.offX = offsetX
        self.offY = offsetY

    def getCords(self, x, y):
        return  (x + self.offX, 
                self.display_height - self.offY + y)

    def printRect(self, r :Rect, color :tuple) -> None:
        x, y = self.getCords(r.a.x, r.a.y)
        pygame.draw.rect(self.plot_display, color, 
            (x, y, r.width_l + r.width_r, r.height_u + r.height_d))

area = Rect(Point(0, 0), 80, 80)
squares = tuple([
    Rect(Point(0, 0), 2, 4), 
    Rect(Point(0, 0), 4, 6), 
    Rect(Point(0, 0), 12, 2),
    Rect(Point(0, 0), 8, 4),
    Rect(Point(0, 0), 8, 6),
    Rect(Point(0, 0), 4, 10)])

fitCls = FitnessClass(area, squares)
genAlg = GeneticAlgorithm(150, 0.2, 0.1, fitCls)
genAlg.repeat(1000)
bestSpecimen = max(genAlg.generation, key = lambda x : x.fitness)
print(bestSpecimen)
print(bestSpecimen.fitness)

printer = PrintAlg(area.width_l, area.height_u)

black = (0, 0, 0)
printer.printRect(area, black)

for idx, x in enumerate(bestSpecimen.chrsom):
    curr = squares[idx].cloneOffset(x)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    printer.printRect(curr, color)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()




