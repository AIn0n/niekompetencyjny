from matplotlib.pyplot import *
from matplotlib.patches import Rectangle
from numpy import *
import knapsack_2d.figureTypes as figs


class Drawing:

    def __init__(self, field: figs.Rect):
        self.field = field
        fig, self.temp = subplots()
        self.temp.add_patch(matplotlib.patches.Rectangle((field.a.x, field.a.y), field.width, field.height, color = "red"))
        draw()
        #show()

    def add_rectangle(self, rectangle: figs.Rect):
        self.temp.add_patch(matplotlib.patches.Rectangle(rectangle.a.x, rectangle.a.y, rectangle.width, rectangle.height))
        draw()
        show()


if __name__ == '__main__':

    point = figs.Point(0, 0)
    temp = figs.Rect(point, 100, 100)
    tempd = Drawing(temp)
    show()
    Drawing.add_rectangle(tempd, figs.Rect(figs.Point(10, 10), 5, 6))
