from sense_hat import SenseHat
from src.utils.colors import R, W, O, Y, N, G, O, S, B
from random import randint

s = SenseHat()

bricks = []
selectedBrick = None

pixels = [N for i in range(64)]
occupied = [[False for x in range(8)] for y in range(8)]

figures = [
    [[[B, B, B, B]], [[B], [B], [B], [B]], [[B, B, B, B]], [[B], [B], [B], [B]]],
    [
        [[O, 0, 0], [O, O, O]],
        [[O, O], [O, 0], [O, 0]],
        [[O, O, O], [0, 0, O]],
        [[0, O], [0, O], [O, O]],
    ],
    [
        [[0, 0, G], [G, G, G]],
        [[G, 0], [G, 0], [G, G]],
        [[G, G, G], [G, 0, 0]],
        [[G, G], [0, G], [0, G]],
    ],
    [[[Y, Y], [Y, Y]], [[Y, Y], [Y, Y]], [[Y, Y], [Y, Y]], [[Y, Y], [Y, Y]]],
    [
        [[0, R, R], [R, R, 0]],
        [[R, 0], [R, R], [0, R]],
        [[0, R, R], [R, R, 0]],
        [[R, 0], [R, R], [0, R]],
    ],
    [
        [[0, S, 0], [S, S, S]],
        [[S, 0], [S, S], [S, 0]],
        [[S, S, S], [0, S, 0]],
        [[0, S], [S, S], [0, S]],
    ],
    [
        [[W, W, 0], [0, W, W]],
        [[0, W], [W, W], [W, 0]],
        [[W, W, 0], [0, W, W]],
        [[0, W], [W, W], [W, 0]],
    ],
]


def clear():
    global pixels
    for x in range(8):
        for y in range(8):
            if not occupied[x][y]:
                pixels[x + y * 8] = N


def putpixel(x, y, c):
    if x < 8 and not occupied[x][y]:
        pixels[x + y * 8] = c


class Brick:
    def __init__(self, type, rotation, xpos, ypos):
        self.type = type
        self.rotation = rotation
        self.xpos = xpos
        self.ypos = ypos

    def render(self):
        for y in range(len(figures[self.type][self.rotation])):
            for x in range(len(figures[self.type][self.rotation][y])):
                if figures[self.type][self.rotation][y][x] != 0:
                    putpixel(
                        self.xpos + x,
                        self.ypos + y,
                        figures[self.type][self.rotation][y][x],
                    )

    def dropped(self):
        if self.ypos + len(figures[self.type][self.rotation]) - 1 >= 7:
            return True

        dropped = False
        for i in range(len(figures[self.type][self.rotation][0])):
            if occupied[self.xpos + i][
                self.ypos + len(figures[self.type][self.rotation]) - 1
            ]:
                dropped = True
        return dropped

    def markActives(self):
        for y in range(len(figures[self.type][self.rotation])):
            for x in range(len(figures[self.type][self.rotation][y])):
                if figures[self.type][self.rotation][y][x] != 0:
                    occupied[self.xpos + x][self.ypos + y] = True

    def left(self):
        if self.xpos > 0:
            self.xpos -= 1

    def down(self):
        self.ypos += 1

    def drop(self):
        while not self.dropped():
            self.down()

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def right(self):
        if self.xpos < 8 - len(figures[self.type][self.rotation][0]):
            self.xpos += 1


def newfigure():
    return Brick(randint(0, 6), 0, 3, 0)


def mainloop():
    global selectedBrick

    if selectedBrick.dropped():

        selectedBrick.markActives()
        selectedBrick = newfigure()

    for i in range(len(occupied)):
        if all(cell[i] for cell in occupied):
            for j in range(i - 1, 0):
                occupied[j + 1] = occupied[j]

    for event in s.stick.get_events():
        if event.direction == "left" and event.action != "released":
            selectedBrick.left()
        if event.direction == "down" and event.action != "released":
            selectedBrick.down()
        if event.direction == "middle" and event.action == "released":
            selectedBrick.drop()
        if event.direction == "up" and event.action == "pressed":
            selectedBrick.rotate()
        if event.direction == "right" and event.action != "released":
            selectedBrick.right()
    clear()

    selectedBrick.render()
    s.set_pixels(pixels)


def tetris():
    global selectedBrick
    selectedBrick = newfigure()
    while True:
        mainloop()
