import pygame as py


class Character():
    ## Constructor
    def __init__(self):

        self.img = py.image.load("Games/AMST/Assets/character1.png")

        self.x = 100
        self.y = 250

    def getPos(self):
        return (self.x, self.y)
    
class Npc():
    def __init__(self):

        self.img = py.image.load("Games/AMST/Assets/npc1.png")
        self.x = 100
        self.y = 40

    def getPos(self):
        return (self.x, self.y)
        
    
class Scroll():
    def __init__(self):
        self.rate = 0.1
        self.stop = False

    def scroll(self):
        if self.rate < 5 and self.stop == False:
            self.rate += 0.02
            return self.rate
        elif self.rate > 5:
            self.stop = True
            self.rate -= 0.02
            return self.rate
        elif self.rate < 5 and self.rate > 0:
            self.rate -= 0.02
            return self.rate
        else:
            self.rate = 0
            return self.rate
    
    def reset(self):
        self.rate = 0.1
        self.stop = False
    

