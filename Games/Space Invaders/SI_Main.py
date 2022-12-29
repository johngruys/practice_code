import pygame as py
import random
import math 

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
# enemy_image = py.image.load("Games/Space Invaders/SIAssets/alien.png")
# enemyX = random.randint(0, 736)
# enemyY = random.randint(50, 250)
# enemyX_change = 0.15
# enemyY_change = 30

### Multiple Enemies ###
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemies = 6

for i in range(num_enemies):
    enemy_image.append(py.image.load("Games/Space Invaders/SIAssets/alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(0.15)
    enemyY_change.append(30)


### Bullet ###
laser_image = py.image.load("Games/Space Invaders/SIAssets/laser.png")
laserX = 0
laserY = 480
laserY_change = -.75
laser_state = "ready"

### Score ###
score_value = 0
font = py.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

def showscore(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


### fire laser function, 16 and 10 are offsets ###
def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_image, (x + 8, y - 8))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def iscollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt(((enemyX - laserX) ** 2) + ((enemyY - laserY) ** 2))
    if distance < 27:
        return True
    else:
        return False





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
    # enemyX[i] += enemyX_change[i]

    ### Boundary ###
    for i in range(num_enemies):

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = -1 * enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 734:
            enemyX_change[i] = -1 * enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        


    ### Bullet movement ###
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY += laserY_change

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    ### Checking for collision ### (moved to for loop)

    # collision = iscollision(enemyX, enemyY, laserX, laserY)
    # if collision:
    #     laserY = 480
    #     laser_state = "ready"
    #     score += 1
    #     print(score)
    #     enemyX = random.randint(0, 736)
    #     enemyY = random.randint(50, 150)
        

    ### Draws the player using passed coordinates ###
    player(playerX, playerY)
    # enemy(enemyX, enemyY) (moved to for loop)

    ### Show score ###
    showscore(textX, textY)

 
    # Updates screen with all new info 
    py.display.update()