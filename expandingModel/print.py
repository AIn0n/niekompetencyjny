import random
import pygame
from RoomTemplate import RoomTemplate
from JsonIO import JsonIO
from genAlgorithm import *

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

        self.offX = self.offY = fieldHeight/2

    def getCords(self, x, y):
        return x + self.offX, y + self.offY

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

smth = JsonIO.read('expandingModel/curr.json')

for s in smth[:-1]:
    smth[-1].addNeighbour(s.name)

squares = [Rect(Point(0, 0), x.minWidth, x.minHeight) for x in smth]

fitCls = FitnessClass(area, smth)
genAlg = GeneticAlgorithm(150, 0.3, 0.1, fitCls)
genAlg.repeat(2000)
bestSpecimen = max(genAlg.generation, key=lambda x: x.fitness)
print(bestSpecimen.fitness)

printer = PrintAlg(80, 80)

black = (0, 0, 0)
printer.printRect(area, black)
rooms = []
for i in range(len(squares)):
    r = 0
    if  bestSpecimen.chrsoms['rotation'][i]:
        r = Rect(
         Point(0,0),
         squares[i].height_d + squares[i].height_u, 
         squares[i].width_r + squares[i].width_l)
    else:
        r = squares[i]
    rooms.append(r.cloneOffset(bestSpecimen.chrsoms['location'][i]))

expandRects(rooms, area, bestSpecimen.chrsoms['expansion'])

colors = [tuple(random.randint(0, 255) for n in range(3)) for _ in rooms]
for idx, rect in enumerate(rooms):
    printer.printRect(rect, colors[idx])
    renderedFront = printer.font.render(smth[idx].name, False, colors[idx])
    printer.plot_display.blit(renderedFront, (600, 30 * idx))

printer.printAll()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
