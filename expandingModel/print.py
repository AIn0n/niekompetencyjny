import pygame
import random
from figureTypes import *
from genAlgorithm import *

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

plot_display = pygame.display.set_mode((display_width, display_height))
plot_display.fill(white)

squares = tuple([
    Rect(Point(0, 0), 2, 4), 
    Rect(Point(0, 0), 4, 6), 
    Rect(Point(0, 0), 12, 2),
    Rect(Point(0, 0), 8, 4),
    Rect(Point(0, 0), 8, 6),
    Rect(Point(0, 0), 4, 10)])
fitCls = FitnessClass(Rect(Point(0, 0), 80, 80),squares)
genAlg = GeneticAlgorithm(150, 0.1, 0.2, fitCls)
genAlg.repeat(3000)
bestSpieceMan = max(genAlg.generation, key = lambda x : x.fitness)
print(bestSpieceMan)
print(bestSpieceMan.fitness)

for idx, x in enumerate(bestSpieceMan.chrsom):
    curr = squares[idx].cloneOffset(x)
    pygame.draw.rect(plot_display, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
        (curr.a.x, curr.a.y, 
        (curr.width_l + curr.width_r), 
        (curr.height_u + curr.height_d)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()





