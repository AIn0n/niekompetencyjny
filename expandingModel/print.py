import pygame
import random
from figureTypes import *
from genAlgorithm import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

display_width = 1000
display_height = 600
SCALE = 10
offset = 100

black = (0, 0, 0)
white = (255, 255, 255)

plot_display = pygame.display.set_mode((display_width, display_height))
plot_display.fill(white)

area = Rect(Point(0, 0), 80, 80)
squares = tuple([
    Rect(Point(0, 0), 2, 4), 
    Rect(Point(0, 0), 4, 6), 
    Rect(Point(0, 0), 12, 2),
    Rect(Point(0, 0), 8, 4),
    Rect(Point(0, 0), 8, 6),
    Rect(Point(0, 0), 4, 10)])

fitCls = FitnessClass(area, squares)
genAlg = GeneticAlgorithm(300, 0.2, 0.1, fitCls)
genAlg.repeat(7000)
bestSpieceMan = max(genAlg.generation, key = lambda x : x.fitness)
print(bestSpieceMan)
print(bestSpieceMan.fitness)

pygame.draw.rect(plot_display, black, 
        ((area.a.x * SCALE)+100, (area.a.y * SCALE)+100,
        (area.width_l + area.width_r) * SCALE, 
        (area.height_u + area.height_d) * SCALE))

for idx, x in enumerate(bestSpieceMan.chrsom):
    curr = squares[idx].cloneOffset(x)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    texture = font.render(f'x:{curr.a.x},y:{curr.a.y} //{curr.width_l + curr.width_r}, {curr.height_d + curr.height_u}', False, color)
    plot_display.blit(texture, ((area.c.x * SCALE)+offset, 0 + idx * 30))

    pygame.draw.rect(plot_display, color, 
        ((curr.a.x * SCALE)+offset, (curr.a.y * SCALE)+offset,
        (curr.width_l + curr.width_r) * SCALE, 
        (curr.height_u + curr.height_d) * SCALE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()





