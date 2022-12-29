import pygame as py

class Dolphin():

    # Initialize and define variables #
    def __init__(self):
        self.img = py.image.load("Games/Dolphino/Assets/character.png")
        self.x = 200
        self.y = 200
        self.dx = 0
        self.dy = 0
        self.right = False
        self.left = False
        self.up = False
        self.down = False
     
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
    
    def y_movement(self, y):
        if y == 1:
            self.up = True
        elif y == -1:
            self.down = True
        elif y == -2:
            self.down = False
        elif y == 2:
            self.up = False
        
    # Read the name of the function #
    def update_position(self):
        if self.right and not self.left:
            self.x = self.x + 3
        elif self.left and not self.right:
            self.x = self.x - 3
        
        if self.up and not self.down:
            self.y = self.y - 3
        elif self.down and not self.up:
            self.y = self.y + 3

    # Again, self explanatory #
    def position(self):
        return (self.x, self.y)
        
        
