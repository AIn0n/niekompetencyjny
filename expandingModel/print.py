import pygame
import random
from figureTypes import *
from genAlgorithm import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

display_width = 800
display_height = 600
SCALE = 5


black = (0, 0, 0)
white = (255, 255, 255)

plot_display = pygame.display.set_mode((display_width, display_height))
plot_display.fill(white)

area = Rect(Point(0, 0), 80, 80)
rectangles = tuple([
    Rect(Point(0, 0), 2, 4), 
    Rect(Point(0, 0), 4, 6), 
    Rect(Point(0, 0), 12, 2),
    Rect(Point(0, 0), 8, 4),
    Rect(Point(0, 0), 8, 6),
    Rect(Point(0, 0), 4, 10)])

fitCls = FitnessClass(area, rectangles)
genAlg = GeneticAlgorithm(250, 0.2, 0.3, fitCls)
genAlg.repeat(7000)
bestSpieceMan = max(genAlg.generation, key = lambda x : x.fitness)
print(bestSpieceMan)
print(bestSpieceMan.fitness)

pygame.draw.rect(plot_display, black, 
        (area.a.x * SCALE, area.a.y * SCALE, 
        (area.width_l + area.width_r) * SCALE, 
        (area.height_u + area.height_d) * SCALE))

rooms = [rectangles[idx].cloneOffset(x) for idx, x in enumerate(bestSpieceMan.chrsom)]

for n in range(len(rooms)):
    curr = rooms.pop(0)
    for room in rooms:
        if curr.collides(room):
            print("dupa")
    rooms.append(curr)

for n in range(len(rooms)):
    curr = rooms.pop(0)
    curr.expandLeft(rooms, area)
    curr.expandRight(rooms, area)
    curr.expandUp(rooms, area)
    curr.expandDown(rooms, area)
    rooms.append(curr)

offset = 0
pygame.draw.rect(plot_display, black, 
        (area.a.x * SCALE, area.a.y * SCALE, 
        (area.width_l + area.width_r) * SCALE, 
        (area.height_u + area.height_d) * SCALE))

for curr in rooms:
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    texture = font.render(f'{curr.width_l + curr.width_r}, {curr.height_d + curr.height_u}', False, color)
    plot_display.blit(texture, (area.c.x * SCALE, (area.c.y * SCALE) + offset))
    offset += 30

    pygame.draw.rect(plot_display, color, 
        (curr.a.x * SCALE, curr.a.y * SCALE, 
        (curr.width_l + curr.width_r) * SCALE, 
        (curr.height_u + curr.height_d) * SCALE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()





