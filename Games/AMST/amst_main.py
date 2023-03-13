import pygame as py
from pygame import time
from amst_classes import Character
# import time
import math
# import random



## Initialize pygame
py.init()

## Create screen
screen = py.display.set_mode((1000, 500))

## Logo
logo = py.image.load("Games/AMST/Assets/LatinAmericaLogo.png")
py.display.set_icon(logo)

## Title
py.display.set_caption("Latin American Trivia")

## Create clock
clock = py.time.Clock()

## Colors
white = (255, 255, 255)
black = (0, 0, 0)

## Background
background = py.image.load("Games/AMST/Assets/background1.jpg")
scroll = 0
tiles = math.ceil(1000/ background.get_width()) + 1

## Create objects
character = Character()


# Boolean for game loop
running = True

while running:


     # Screen Scrolling (??? idk) #
    i = 0
    while (i < tiles):
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1

    scroll -= 3
    
    if abs(scroll) > background.get_width():
        scroll = 0


    ## UI
    for event in py.event.get():

        ## Key Presses
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                pass


        ## Exit window
        if event.type == py.QUIT:
            running = False


    ## Update!!!!
    clock.tick(60)
    py.display.update()

    


    

