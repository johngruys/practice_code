import pygame as py
import time
import math
import random
from pygame import mixer
from dolphino_classes import Dolphin
from dolphino_classes import Ring
from dolphino_classes import Obstacle
from dolphino_classes import Heart

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

### Background ###
background = py.image.load("Games/Dolphino/Assets/background.png")
scroll = 0

tiles = math.ceil(1100/ background.get_width()) + 1

### Clock ###
clock = py.time.Clock()

### Background Music ###
mixer.music.load("Games/Dolphino/Assets/say_hey.wav")
mixer.music.play(-1)

### Global Vars ###

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)
tan = (200, 180, 140)


# Jumping #
charging = False
jumping = False
charge = None
jump_start = 0
jump_duration = 0
out_of_water = False

# Rings #
rings_collected = 0
prev_ring_captured = 0

# Lives #
lives = 3
damage_cooldown = 0
prev_heart_captured = 0
game_ended = False
played = False
empty_heart = py.image.load("Games/Dolphino/Assets/empty_heart.png")
full_heart = py.image.load("Games/Dolphino/Assets/full_heart.png")
heart_cordinate_1 = (930, 15)
heart_cordinate_2 = (980, 15)
heart_cordinate_3 = (1030, 15)



# Objects #
p1 = Dolphin()
ring = Ring()
heart = Heart()

obstacles = []
created_obstacles = {0: True}
create_obstacle_cooldown = 0


### Functions ###

def create_obstacles():
        obstacles.append(Obstacle())

# To play gg audio once #


def game_over():
    p1.game_over()
    py.mixer.music.stop()
    gg_font = py.font.Font("freesansbold.ttf", 60)
    text1 = "Game Over"
    text2 = "Rings Collected: "
    text1_render = gg_font.render(text1, True, blue)
    text2_render = gg_font.render(text2 + str(rings_collected), True, blue)
    screen.blit(text1_render, (370, 230))
    screen.blit(text2_render, (280, 300))
    global played
    if played == False:
        p1.sounds("cudi")
        played = True


# Create First Obstacle #
create_obstacles()

# Global Timer #
game_start_time = time.time()

### Game Loop ###

while running:

    ### End Game ###
    if lives < 1:
        game_over()

    
    # Frame Timer #
    frame_start_time = time.time()

    # Screen Scrolling (??? idk) #
    i = 0
    if not p1.stop:
        while (i < tiles):
            screen.blit(background, (background.get_width() * i + scroll, 0))
            i += 1

        scroll -= 3
        if abs(scroll) > background.get_width():
            scroll = 0


    # Charge Background #
    py.draw.rect(screen, tan, (35, 20, 150, 35), 0, 4)
    jump_text = "Jump"
    jump_font = py.font.Font("freesansbold.ttf", 16)
    disp_jump_text = jump_font.render(jump_text, True, black)
    


    ### User Input ###
    for event in py.event.get():

        if event.type == py.KEYDOWN:


            # if not game_ended: # Cancel controls after dying #

                # Dolphin Movement #
                if event.key == py.K_DOWN:
                    p1.y_movement(-1)
                elif event.key == py.K_UP:
                    p1.y_movement(1)
                elif event.key == py.K_LEFT:
                    p1.x_movement(-1)
                elif event.key == py.K_RIGHT:
                    p1.x_movement(1)
                
                # Charge jump #
                if not jumping:
                    if event.key == py.K_SPACE:
                        charging = True
                        charge_start = time.time()


            
        if event.type == py.KEYUP:
            
            # Dolphin Movement #
            if event.key == py.K_DOWN:
                p1.y_movement(-2)
            elif event.key == py.K_UP:
                p1.y_movement(2)
            elif event.key == py.K_LEFT:
                p1.x_movement(-2)
            elif event.key == py.K_RIGHT:
                p1.x_movement(2)

            # Space released #
            if not jumping:
                if event.key == py.K_SPACE:
                    jumping = True
                    p1.jumping = True
                    charging = False
                    if (charge * 80) > 140:
                        charge = 140/80
                    p1.jump(charge)

    
        # Closing Window #
        if event.type == py.QUIT:
            running = False

         
    ### Borders ###
    if p1.x < 0:
        p1.x = 0
    if p1.x > 1036:
        p1.x = 1036
    if p1.y > 536:
        p1.y = 536
    if not jumping:
        if p1.y < 245:
            p1.y = 245

    ### Splash Sound ###
    if jumping:
        if (240 - p1.y) > 0:
            out_of_water = True
        if out_of_water == True and p1.y > 245:
            p1.sounds("splash")
            out_of_water = False


    ### Charge Behavior ###
    if charging == True:
        charge = abs(charge_start - time.time())
        
        # Draw charge bar #
        if (charge * 80) < 140:
            py.draw.rect(screen, blue, (40, 25, (charge * 80), 25), 0, 2)
        else:
            py.draw.rect(screen, lblue, (40, 25, 140, 25), 0, 2)


    ### Ending Jump ###
    if p1.jumping == False:
        jumping = False

    ### Collision Detection ###
    distance_to_ring = math.sqrt(((ring.x -10) - p1.x) ** 2 + ((ring.y + 18) - p1.y) ** 2)

    if distance_to_ring < 40 and (frame_start_time - prev_ring_captured) > 1:
        prev_ring_captured = time.time()
        rings_collected += 1
        p1.sounds("ring")

    distance_to_heart = math.sqrt((heart.x - p1.x) ** 2 + (heart.y - p1.y) ** 2)
    if distance_to_heart < 50 and (frame_start_time - prev_heart_captured) > 1:
        if lives < 3:
            prev_heart_captured = time.time()
            lives += 1
            heart.collect()
            p1.sounds("life")


    ### Obstacle Behavior ###
    if not p1.stop:
        for item in obstacles:
            
            # Update and draw obstacles #
            item.update_position()
            screen.blit(item.img, item.position())

            # Reset when off screen #
            if item.x < random.randint(-400, -200):
                item.reset_object()

            # Collision Detection #
            distance_to_obstacle = math.sqrt(((item.x - 20) - p1.x) ** 2 + ((item.y - 15) - p1.y) ** 2)
            if distance_to_obstacle < 45 and (frame_start_time - damage_cooldown) > 1.4:
                damage_cooldown = time.time()
                lives -= 1
                p1.sounds("hurt")


    ### Draw Hearts ###
    screen.blit(empty_heart, heart_cordinate_1)
    screen.blit(empty_heart, heart_cordinate_2)
    screen.blit(empty_heart, heart_cordinate_3)

    if lives >= 1:
        screen.blit(full_heart, heart_cordinate_1)
    if lives >= 2:
        screen.blit(full_heart, heart_cordinate_2)
    if lives >= 3:
        screen.blit(full_heart, heart_cordinate_3)

    ### Draw Score ###
    score_text = str(rings_collected)
    score_text_words = "Score: "
    score_font = py.font.Font("freesansbold.ttf", 35)
    words_font = py.font.Font("freesansbold.ttf", 32)
    # score_to_disp = score_font.render(score_text, True, black)
    score_text_words_disp = words_font.render(score_text_words + score_text, True, black)
    # screen.blit(score_to_disp, (550, 45))
    screen.blit(score_text_words_disp, (940, 70))
    
    ### Add obstacles ###
    # if rings_collected % 4 == 0 and (frame_start_time - create_obstacle_cooldown) > 20 and rings_collected != 0:
    #     create_obstacle_cooldown = time.time()
    #     create_obstacles()

    if rings_collected % 4 == 0 and rings_collected not in created_obstacles:
        create_obstacles()
        created_obstacles[rings_collected] = True
    
    ### Reset Ring ###
    if ring.x < (-350):
        ring.reset()

    ### character ###
    life_rng = random.randint(0, 1100)
    if life_rng == 44 and heart.collected == True:
        heart.reset()

    if not p1.stop:
        p1.update_position()
        screen.blit(p1.img, p1.position())

        ### Ring ###
        ring.update_position()
        screen.blit(ring.img, ring.position())

        ### Extra Lifes ###
        heart.update_position()
        screen.blit(heart.img, heart.position())

    ### Update !!! ###
    clock.tick(60)
    py.display.update()