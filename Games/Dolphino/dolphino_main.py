import pygame as py
import time
import math
from dolphino_classes import Dolphin
from dolphino_classes import Ring
from dolphino_classes import Obstacle

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

### Global Vars ###

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)

# MISC #
charging = False
jumping = False
charge = None
jump_start = 0
jump_duration = 0

rings_collected = 0
ring_cool_down = 0

# Items #
p1 = Dolphin()
ring = Ring()

obstacles = []



### Functions ###

def create_obstacles():
        obstacles.append(Obstacle())

# Create First Obstacle #
create_obstacles()



### Game Loop ###

while running:
    
    # Background #
    screen.fill(blue)

    # Global Timer #
    game_start_time = time.time()

    # Screen Scrolling (??? idk) #
    i = 0
    while (i < tiles):
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1

    scroll -= 3
    if abs(scroll) > background.get_width():
        scroll = 0

    
    # Charge Background #
    py.draw.rect(screen, black, (35, 35, 150, 35), 0, 4)
    jump_text = "Jump Level"
    jump_font = py.font.Font("freesansbold.ttf", 20)
    disp_jump_text = jump_font.render(jump_text, True, black)
    screen.blit(disp_jump_text, (53, 15))   


    ### User Input ###
    for event in py.event.get():

        if event.type == py.KEYDOWN:


            if not jumping: # Cancel controls while jumping #

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
                    charging = False
                    jump_start = time.time()
                    p1.jump()

    
        # Closing Window #
        if event.type == py.QUIT:
            running = False


    ### Charge Behavior ###

    if charging == True:
        charge = abs(charge_start - time.time())
        
        # Draw charge bar #
        if (charge * 80) < 140:
            py.draw.rect(screen, lblue, (40, 40, (charge * 80), 25), 0, 2)
        else:
            py.draw.rect(screen, lblue, (40, 40, 140, 25), 0, 2)


    ### Jump Behavior ###

    if jumping == True:
        
        # Maximum charge #
        if (charge * 80) > 140:
            charge = 140/80

        jump_duration = abs(jump_start - time.time())
        if p1.jump_up:
            if jump_duration > (charge / 2):
                p1.jump_down = True
                p1.jump_up = False

        elif p1.jump_down:
            if jump_duration > charge:
                p1.jump_down = False
                jumping = False


    ### Collision Detection ###

    distance_to_ring = math.sqrt((ring.x - p1.x) ** 2 + (ring.y - p1.y) ** 2)

    if distance_to_ring < 40 and (game_start_time - ring_cool_down) > 1:
        ring_cool_down = time.time()
        rings_collected += 1


    ### Obstacle Behavior ###
    for item in obstacles:
        
        # Update and draw obstacles #
        item.update_position()
        screen.blit(item.img, item.position())

        if item.x < -200:
            item.reset_object()



   

    ### Reset Ring ###
    if ring.x < (-180):
        ring.reset()

    ### character ###
    p1.update_position()
    screen.blit(p1.img, p1.position())

    ### Ring ###
    ring.update_position()
    screen.blit(ring.img, ring.position())

    ### Update !!! ###
    clock.tick(100)
    py.display.update()