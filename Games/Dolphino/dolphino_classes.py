import pygame as py
import random

class Dolphin():

    # Initialize and define variables #
    def __init__(self):
        self.img = py.image.load("Games/Dolphino/Assets/character.png")

        # Spawn Location #
        self.x = 180
        self.y = 370

        # Speed #
        self.x_speed = 3.5
        self.y_speed = 2.5
        self.x_jump_speed = 1
        self.y_jump_vel = None
        self.y_stored_jump_vel = None

        # Movement Vars #
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.jumping = False
        self.recieved = False
     
    # IDEK tbh #
    def __repr__(self):
        return self.img

    def __str__(self):
        return "I'm a dolphin bruh"


    # Probably not the best but it works #
    def x_movement(self, x):
        if x == 1:
            self.right = True
        elif x == -1:
            self.left = True
        elif x == -2:
            self.left = False
        elif x == 2:
            self.right = False
        elif x == "stop":
            self.right = False
            self.left = False
    
    def y_movement(self, y):
        if y == 1:
            self.up = True
        elif y == -1:
            self.down = True
        elif y == -2:
            self.down = False
        elif y == 2:
            self.up = False
        elif y == "stop":
            self.up = False
            self.down = False
        
    # Read the name of the function #
    def update_position(self):
        if not self.jumping:
            if self.right and not self.left:
                self.x = self.x + self.x_speed
            elif self.left and not self.right:
                self.x = self.x - self.x_speed
            elif self.left and self.right:
                self.x = self.x
            
            if self.up and not self.down:
                self.y = self.y - self.y_speed
            elif self.down and not self.up:
                self.y = self.y + self.y_speed
            elif self.up and self.down:
                self.y = self.y
        
        else:
            self.x = self.x + self.x_jump_speed
            self.y = self.y - self.y_jump_vel

            self.y_jump_vel -= .1
            if self.y_jump_vel < -self.y_stored_jump_vel:
                self.jumping = False
                

    def jump(self, charge):
        
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        if charge < .6:
            jump_power = 1
        elif charge < 1:
            jump_power = 1.3
        elif charge < 1.3:
            jump_power = 1.5
        elif charge <1.5:
            jump_power = 1.6
        elif charge < 1.7:
            jump_power = 1.7
        else:
            jump_power = 1.75

        self.y_jump_vel = jump_power * 4
        self.y_stored_jump_vel = jump_power * 4




    # Again, self explanatory #
    def position(self):
        return (self.x, self.y)


### Ring Class ###

class Ring():
    def __init__(self):
        self.img = py.image.load("Games/Dolphino/Assets/loop.png")
        self.x = 1200
        self.y = random.randint(0, 180)
        self.x_speed = -6
    
    def __str__(self):
        return "The hoop dolphino jumps through"

    def update_position(self):
        self.x = self.x + self.x_speed

    def position(self):
        return (self.x, self.y)

    def reset(self):
        self.x = 1200
        self.y = random.randint(0, 150)



### Obstacle Class ###

class Obstacle():

    def __init__(self):
        self.img = None
        self.y = None
        self.x = None
        self.x_speed = None

        self.reset_object()

    def __str__(self):
        return "Imma kill dolphino"
    
    def update_position(self):
        self.x = self.x + self.x_speed

    def position(self):
        return (self.x, self.y)
    
    def reset_object(self):
        # Randomize Picture #
        _random = random.randint(0,4)
        if _random == 0:
            self.img = py.image.load("Games/Dolphino/Assets/rock.png")
            self.x_speed = -3
        if _random == 1:
            self.img = py.image.load("Games/Dolphino/Assets/antique.png")
            self.x_speed = -3
        if _random == 2:
            self.img = py.image.load("Games/Dolphino/Assets/fish_hook.png")
            self.x_speed = -4.5
        if _random == 3:
            self.img = py.image.load("Games/Dolphino/Assets/stone2.png")
            self.x_speed = -3
        if _random == 4:
            self.img = py.image.load("Games/Dolphino/Assets/trash.png")
            self.x_speed = -3

        # Randomize Location #
        self.x = 1200
        self.y = random.randint(280, 536)


        
        
        
