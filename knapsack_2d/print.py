import pygame
import random
from knapsack_2d.figureTypes import *

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

plot_display = pygame.display.set_mode((display_width, display_height))
plot_display.fill(white)


r1 = Rect((Point.rand([0, 800], [0, 600])), random.randint(100, 200), random.randint(100, 200))
r2 = Rect((Point.rand([0, 800], [0, 600])), random.randint(100, 200), random.randint(100, 200))
r3 = Rect((Point.rand([0, 800], [0, 600])), random.randint(100, 200), random.randint(100, 200))
r4 = Rect((Point.rand([0, 800], [0, 600])), random.randint(100, 200), random.randint(100, 200))
r5 = Rect((Point.rand([0, 800], [0, 600])), random.randint(100, 200), random.randint(100, 200))


rooms = [r1, r2, r3, r4, r5]

for x in rooms:
    pygame.draw.rect(plot_display, (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)), (x.a.x, x.a.y, x.width, x.height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()





