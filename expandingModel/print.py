import pickle
import random
import pygame
from JsonIO import JsonIO
from Door import Door
from genAlgorithm import *
from figures.figures import *


class PrintAlg:
    display_width = 720
    display_height = 480
    white = (255, 255, 255)

    def __init__(self, fieldWidth, fieldHeight) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.plot_display = pygame.display.set_mode(
            (self.display_width, self.display_height)
        )
        self.plot_display.fill(self.white)

        self.inter_display = pygame.Surface((fieldWidth, fieldHeight))
        self.inter_display.blit(
            pygame.transform.flip(self.inter_display, False, True), (0, 0)
        )

        self.offX = self.offY = fieldHeight / 2

    def getCords(self, x, y):
        return x + self.offX, y + self.offY

    def printRect(self, r: Rect, color: tuple) -> None:
        x, y = self.getCords(r.a.x, r.a.y)
        pygame.draw.rect(
            self.inter_display,
            color,
            (x, y, r.width_l + r.width_r, r.height_u + r.height_d),
        )

    def printDoor(self, door: Door, color: tuple) -> None:
        self.printCircle(door.coords, color)

    def printCircle(self, coords: Point, color: tuple) -> None:
        # Adjusting by offset
        x, y = self.getCords(coords.x, coords.y)
        pygame.draw.circle(
            self.inter_display, color, (x, y), radius=1
        )

    def printAll(self) -> None:
        self.scaleSurface()
        self.plot_display.blit(self.inter_display, (0, 0))
        pygame.display.flip()

    def scaleSurface(self) -> None:
        self.inter_display = pygame.transform.scale(
            self.inter_display, (self.display_height, self.display_height)
        )


area, smth = JsonIO.read("expandingModel/input_data/curr.json")
fitCls = FitnessClass(area, smth)
rcts = [Rect(Point(0, 0), x.minWidth, x.minHeight) for x in smth]

printer = PrintAlg(area.getWidth(), area.getHeight())

bestSpecimen = pickle.load(open("expandingModel/output_data/out.bin", "rb"))
doors = fitCls.validNeighborsAndGetDoors(rcts, bestSpecimen.chrsoms['doors'])
black = (0, 0, 0)
printer.printRect(area, black)
rects = []
for i in range(len(rcts)):
    r = 0
    if bestSpecimen.chrsoms["rotation"][i]:
        r = Rect(
            Point(0, 0),
            rcts[i].height_d + rcts[i].height_u,
            rcts[i].width_r + rcts[i].width_l,
        )
    else:
        r = rcts[i]
    rects.append(r.cloneOffset(bestSpecimen.chrsoms["location"][i]))

expandRects(rects, area, bestSpecimen.chrsoms["expansion"])

colors = [tuple(random.randint(0, 255) for n in range(3)) for _ in rects]
for idx, rect in enumerate(rects):
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
