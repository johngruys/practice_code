import pygame as py
import random

py.init()

running = True

screen = py.display.set_mode((480, 320))

py.display.set_caption("Catchprase 2.0")

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)
tan = (200, 180, 140)

while running:
    
    hello = "hello"
    hello_font = py.font.Font("freesansbold.ttf", 35)
    hello_disp = hello_font.render(hello, True, white)
    screen.blit(hello_disp, (50, 50))
    
    
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
            
    py.display.update()
            
py.quit()
    

