import pygame as py

### Initialize Pygame ###
py.init()


### Create screen ###
screen = py.display.set_mode((800, 600))


### Title and icon ###
py.display.set_caption("(IN) Vision")

icon = py.image.load("c:/Users/johnd/OneDrive/Documents/GitHub/Practice-Code/Games/Space Invaders/vision_pixelated.png")
py.display.set_icon(icon)

### Creating Player ###
player_image = py.image.load("c:/Users/johnd/OneDrive/Documents/GitHub/Practice-Code/Games/Space Invaders/spaceship.png")
playerX = 370
playerY = 480

def player():
    screen.blit(player_image, (playerX, playerY))


### Game loop ###

running = True
while running:

    # Background color (RGB) 
    screen.fill((50, 0, 255))
   

    # Checking if X out is pressed
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Calls player function to load player
    player()
 
    # Updates screen with all new info 
    py.display.update()