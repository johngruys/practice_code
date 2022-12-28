import pygame as py
import random

### Initialize Pygame ###
py.init()


### Create screen ###
screen = py.display.set_mode((800, 600))

background = py.image.load("Games/Space Invaders/SIAssets/background.png")


### Title and icon ###
py.display.set_caption("(IN) Vision")

icon = py.image.load("Games/Space Invaders/SIAssets/vision_pixelated.png")
py.display.set_icon(icon)

### Creating Player ###
player_image = py.image.load("Games/Space Invaders/SIAssets/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

### Creating Enemy ###
enemy_image = py.image.load("Games/Space Invaders/SIAssets/alien.png")
enemyX = random.randint(0, 734)
enemyY = random.randint(50, 250)
enemyX_change = 0.15
enemyY_change = 30

### Bullet ###
laser_image = py.image.load("Games/Space Invaders/SIAssets/laser.png")
laserX = 0
laserY = 480
laserY_change = -.75
laser_state = "ready"


### fire laser function, 16 and 10 are offsets ###
def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_image, (x + 8, y - 8))



def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y):
    screen.blit(enemy_image, (x, y))


### Game loop ###

running = True
while running:

    # Background color (RGB) 
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
   

    # Checking if X out is pressed
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        ### If keystroke pressed, check right or left ###
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                playerX_change = -0.1
            if event.key == py.K_RIGHT:
                playerX_change = 0.1
            if event.key == py.K_SPACE:
                # fire_laser(playerX, laserY)
                if laser_state == "ready":
                    laserX = playerX
                    laser_state = "fire"

        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0

    
    ### Increments the x position ###
    playerX += playerX_change

    ### Creates boundary for left and right side ###
    if playerX > 768:
        playerX = 768
    if playerX < 0:
        playerX = 0

    ### Moving the alien ###
    enemyX += enemyX_change

    ### Boundary ###

    if enemyX <= 0:
        enemyX_change = -1 * enemyX_change
        enemyY += enemyY_change
    if enemyX >= 734:
        enemyX_change = -1 * enemyX_change
        enemyY += enemyY_change


    ### Bullet movement ###
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY += laserY_change

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    ### Draws the player using passed coordinates ###
    player(playerX, playerY)
    enemy(enemyX, enemyY)

 
    # Updates screen with all new info 
    py.display.update()