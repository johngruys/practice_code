import pygame as py
import random
import time
# from pygame import mixer


### Initialize ###
py.init()
running = True

### Screen (Object) ###
screen = py.display.set_mode((900, 600))

### Title and Logo ###
py.display.set_caption(" Snake")

icon = py.image.load("Games/snake/Assets/snake.png")
py.display.set_icon(icon)

### Background ###
# background = py.image.load("Games/snake/Assets/background.png")


### Clock ###
clock = py.time.Clock()



# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)
tan = (200, 180, 140)

while running:
    
    # Overwrite screen with background
    # screen.blit(background, (0, 0))
    
    
    
    ### User Input ###
    for event in py.event.get():

        if event.type == py.KEYDOWN:
            pass
        
        # Closing Window #
        if event.type == py.QUIT:
            running = False
            
    
    ### Update !!! ###
    clock.tick(60)
    py.display.update()