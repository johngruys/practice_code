import pygame as py

py.init()

running = True

screen = py.display.set_mode((800, 600))

squirrel = py.image.load("Practice Stuff/Game Practice/practice_assets/squirrel_crown.png")

while running:
    
    screen.blit(squirrel, (100, 100))

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False


    


            

            