import pygame as py

### Initialize ###
py.init()
running = True

### Screen ###
# Create object #
screen = py.display.set_mode((1000, 650))

### Title and Logo ###
py.display.set_caption(" Dolphino")
icon = py.image.load("Games/Dolphino/Assets/dolphin.png")
py.display.set_icon(icon)


while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    