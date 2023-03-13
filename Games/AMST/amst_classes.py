import pygame as py


class Character():
    ## Constructor
    def __init__(self):

        self.img = py.image.load("Games/AMST/Assets/character1.png")

        self.x = 100
        self.y = 250

    def getPos(self):
        return (self.x, self.y)
    

