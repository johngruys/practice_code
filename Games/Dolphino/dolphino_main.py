import pygame as py
from dolpino_classes import Dolphin

### Initialize ###
py.init()

# Run condition
running = True

### Screen (Object) ###
screen = py.display.set_mode((1100, 600))

### Title and Logo ###
py.display.set_caption(" Dolphino")

icon = py.image.load("Games/Dolphino/Assets/dolphin.png")
py.display.set_icon(icon)

### Clock ###
clock = py.time.Clock()

### Global Vars ###

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)

# Items #
p1 = Dolphin()



### Game Loop ###

while running:
    
    # White Background #
    screen.fill(blue)


    ### User Input ###
    for event in py.event.get():

        if event.type == py.KEYDOWN:
            if event.key == py.K_DOWN:
                p1.y_movement(-1)
            elif event.key == py.K_UP:
                p1.y_movement(1)
            elif event.key == py.K_LEFT:
                p1.x_movement(-1)
            elif event.key == py.K_RIGHT:
                p1.x_movement(1)
            
        if event.type == py.KEYUP:
            if event.key == py.K_DOWN:
                p1.y_movement(-2)
            elif event.key == py.K_UP:
                p1.y_movement(2)
            elif event.key == py.K_LEFT:
                p1.x_movement(-2)
            elif event.key == py.K_RIGHT:
                p1.x_movement(2)











        # Closing Window #
        if event.type == py.QUIT:
            running = False
    
    

    p1.update_position()
    screen.blit(p1.img, p1.position())
    

    ### Update !!! ###
    clock.tick(60)
    py.display.update()