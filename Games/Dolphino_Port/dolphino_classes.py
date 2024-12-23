import pygame as py
import random
from pygame import mixer
import os
import sys

class Dolphin():

    # Initialize and define variables #
    def __init__(self):
        character_path = self.resource_path("Assets\character.png")
        self.img = py.image.load(character_path)

        # Spawn Location #
        self.x = 180
        self.y = 370

        # Speed #
        self.x_speed = 3.5
        self.y_speed = 2.5
        self.x_jump_speed = 1
        self.y_jump_speed = .3
        self.y_jump_vel = None
        self.y_stored_jump_vel = None

        # Movement Vars #
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.jumping = False
        self.recieved = False
        self.stop = False

        # Sounds #
        hurt_path = self.resource_path("Assets\hurt_sound.wav")
        ring_path = self.resource_path("Assets\collect_ring.wav")
        splash_path = self.resource_path("Assets\splash2.wav")
        
        self.hurt_sound = mixer.Sound(hurt_path)
        self.ring_sound = mixer.Sound(ring_path)
        self.splash_sound = mixer.Sound(splash_path)
     
    # IDEK tbh #
    def __repr__(self):
        return self.img

    def __str__(self):
        return "I'm a dolphin bruh"
    
    
    # For executable usage needs to get relative paths
    @staticmethod
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            # If running as a bundled executable
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # If running as a script
            return os.path.join(os.path.abspath("."), relative_path)



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
        if not self.jumping and not self.stop:
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
        
        elif self.jumping and not self.stop:

            # Limited controls while jumping #
            if self.right and not self.left:
                self.x = self.x + self.x_jump_speed
            elif self.left and not self.right:
                self.x = self.x - self.x_jump_speed
            elif self.left and self.right:
                self.x = self.x
            
            if self.up and not self.down:
                self.y = self.y - self.y_jump_speed
            elif self.down and not self.up:
                self.y = self.y + self.y_jump_speed
            elif self.up and self.down:
                self.y = self.y

            # Jump Action #
            self.x = self.x + self.x_jump_speed
            self.y = self.y - self.y_jump_vel

            self.y_jump_vel -= .15
            if self.y_jump_vel < -self.y_stored_jump_vel:
                self.jumping = False
                

    def jump(self, charge):
        
        # self.right = False
        # self.left = False
        # self.up = False
        # self.down = False
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

        self.y_jump_vel = jump_power * 5
        self.y_stored_jump_vel = jump_power * 4.75



    # Again, self explanatory #
    def position(self):
        return (self.x, self.y)

    def game_over(self):
        self.stop = True

    def sounds(self, sound):
        if sound == "hurt":
            self.hurt_sound.play()
        if sound == "ring":
            self.ring_sound.play()
        if sound == "splash":
            self.splash_sound.play()
        if sound == "cudi":
            pass
        if sound == "life":
            self.ring_sound.play()
        


### Ring Class ###

class Ring():
    def __init__(self):
        ring_path = Dolphin.resource_path("Assets/loop.png")
        self.img = py.image.load(ring_path)
        self.x = 1200
        self.y = random.randint(0, 180)
        self.x_speed = -5
    
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
            rock_path = Dolphin.resource_path("Assets/rock.png")
            self.img = py.image.load(rock_path)
            self.x_speed = -3
        if _random == 1:
            antique_path = Dolphin.resource_path("Assets/antique.png")
            self.img = py.image.load(antique_path)
            self.x_speed = -3
        if _random == 2:
            hook_path = Dolphin.resource_path("Assets/fish_hook.png")
            self.img = py.image.load(hook_path)
            self.x_speed = -4.5
        if _random == 3:
            stone2_path = Dolphin.resource_path("Assets/stone2.png")
            self.img = py.image.load(stone2_path)
            self.x_speed = -3
        if _random == 4:
            trash_path = Dolphin.resource_path("Assets/trash.png")
            self.img = py.image.load(trash_path)
            self.x_speed = -3

        # Randomize Location #
        self.x = random.randint(1200, 1400)
        self.y = random.randint(280, 536)



class Heart():
    def __init__(self):
        heart_path = Dolphin.resource_path("Assets/extra_life.png")
        self.img = py.image.load(heart_path)
        self.x = -200
        self.y = 400
        self.x_speed = -4
        self.y_vel = 3
        self.up = True
        self.collected = False
    
    def __str__(self):
        return "Extra Life"
    
    def update_position(self):
        self.x = self.x + self.x_speed
        if self.x < -200:
            self.collected = True

        if self.up:
            self.y = self.y + self.y_vel
            self.y_vel -= .08
            if self.y_vel <= -3:
                self.y_vel = 3
                self.up = False

        if not self.up:
            self.y = self.y - self.y_vel
            self.y_vel -= .08
            if self.y_vel <= -3:
                self.y_vel = 3
                self.up = True
    
    def position(self):
        return (self.x, self.y)
    
    def collect(self):
        self.x = -200
        self.collected = True

    def reset(self):
        self.collected = False
        self.x = 1200
        self.y = random.randint(250, 500)




        
        
        
