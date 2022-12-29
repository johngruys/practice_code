import pygame as py
import random
import math 
from pygame import mixer


### Initialize Pygame ###
py.init()


### Create screen ###
screen = py.display.set_mode((800, 600))

background = py.image.load("Games/Space Invaders/SIAssets/background.png")

### Background music ###
game_ended = False
mixer.music.load("Games/Space Invaders/SIAssets/background.wav")
mixer.music.play(-1)


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

num_enemies = 1
speed_multiplier = 1
enemy_counter = 0

def create_enemies(num_enemies):
    for i in range(num_enemies):
        enemy_image.append(py.image.load("Games/Space Invaders/SIAssets/alien.png"))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 250))
        enemyX_change.append(random.randint(12, 17) / 100)
        enemyY_change.append(speed_multiplier * 0.008)

create_enemies(num_enemies)


### Bullet ###
laser_image = py.image.load("Games/Space Invaders/SIAssets/laser.png")
laserX = 0
laserY = 480
laserY_change = -.75
laser_state = "ready"

### Score ###
score_value = 0
font = py.font.Font("freesansbold.ttf", 32)

level_score_value = 0

textX = 10
textY = 10

### Game Over ###

text_color = (255, 180, 255)

game_ended = False

def game_over():
    gg_font = py.font.Font("freesansbold.ttf", 65)
    gg_text = "Game Over..."
    score_text = "Final Score: "
    disp_text1 = gg_font.render(gg_text, True, text_color)
    disp_text2 = gg_font.render(score_text + str(score_value), True, text_color)
    screen.blit(disp_text1, (140, 225))
    screen.blit(disp_text2, (140, 325))
    global game_ended 
    global playerY
    global playerX_change
    game_ended = True
    playerY = 2000
    playerX_change = 0
    el = py.image.load("Games/Space Invaders/SIAssets/L.png")
    screen.blit(el, (playerX, 480))
    

def showscore(x, y):
    score = font.render("Score: " + str(score_value), True, text_color)
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

    # Game Loop #
    for event in py.event.get():

        # Checking if X out is pressed
        if event.type == py.QUIT:
            running = False

        # Level element
        if level_score_value == 3:
            enemy_counter += 1
            speed_multiplier += 0.5
            if enemy_counter == 4:
                num_enemies += 1
                enemy_counter = 0
            level_score_value = 0
            create_enemies(num_enemies)
        
        ### If keystroke pressed, check right or left ###
        if not game_ended:
            if event.type == py.KEYDOWN:
                if event.key == py.K_LEFT:
                    playerX_change = -0.25
                if event.key == py.K_RIGHT:
                    playerX_change = 0.25
                if event.key == py.K_SPACE:
                    if laser_state == "ready":
                        laser_sound = mixer.Sound("Games/Space Invaders/SIAssets/laser.wav")
                        laser_sound.play()
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

        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000

            game_over()

            break
            

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = -1 * enemyX_change[i]
            
        elif enemyX[i] >= 734:
            enemyX_change[i] = -1 * enemyX_change[i]
            

        collision = iscollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = "ready"
            score_value += 1
            level_score_value += 1
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