import pygame as py
import math

py.init()
running = True
clock = py.time.Clock()


screen = py.display.set_mode((800, 600))
py.display.set_caption("Scrolling Background")

### Load background ###
background = py.image.load("Practice Stuff/Game Practice/skyandwater.png")
scroll = 0

tiles = math.ceil(800/ background.get_width()) + 1




while running:

    # screen.blit(background, (0, 0))

    i = 0
    while (i < tiles):
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1

    scroll -= 3
    if abs(scroll) > background.get_width():
        scroll = 0

    # Input ###
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    



    clock.tick(60)
    py.display.update()
