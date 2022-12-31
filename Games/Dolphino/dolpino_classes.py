import pygame as py
import random

class Dolphin():

    # Initialize and define variables #
    def __init__(self):
        self.img = py.image.load("Games/Dolphino/Assets/character.png")

        # Location #
        self.x = 200
        self.y = 200

        # Speed #
        self.x_speed = 3
        self.y_speed = 2
        self.x_jump_speed = 1
        self.y_jump_up_speed = 3.5
        self.y_jump_down_speed = 3.5

        # Movement Vars #
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.jump_up = False
        self.jump_down = False
     
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
        if not self.jump_up and not self.jump_down:
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

        elif self.jump_up:
            self.x = self.x + self.x_jump_speed
            self.y = self.y - self.y_jump_up_speed

        elif self.jump_down:
            self.x = self.x + self.x_jump_speed
            self.y = self.y + self.y_jump_down_speed



    # Again, self explanatory #
    def position(self):
        return (self.x, self.y)


    def jump(self):

        # Stop current movement #
        # self.right = False
        # self.left = False
        # self.up = False
        # self.down = False

        # Jump #
        self.jump_up = True


class Ring():
    def __init__(self):
        self.picture = py.image.load("Games/Dolphino/Assets/loop.png")
        self.x = 1200
        self.y = random.randint(0, 180)
        self.x_speed = -3
    
    def __str__(self):
        return "The hoop dolphino jumps through"

    def update_position(self):
        self.x = self.x + self.x_speed

    def position(self):
        return (self.x, self.y)

    def reset(self):
        self.x = 1200
        self.y = random.randint(0, 180)

        
        
        
