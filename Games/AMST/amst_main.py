import pygame as py
import time
import math
import random


## Initialize pygame
py.init()

## Create screen
screen = py.display.set_mode((1000, 500))


# Boolean for game loop
running = True

while running:


    ## UI
    for event in py.event.get():

        ## Key Presses
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                pass


        ## Exit window
        if event.type == py.QUIT:
            running = False
    

