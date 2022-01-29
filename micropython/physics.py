from colour import Colour

class Rectangle:
    def __init__(self,x,y,width,height,colour=Colour(1)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
    
    def has_collided(self, rect):
        return abs((self.x + self.width/2) - (rect.x + rect.width/2)) < self.width/2 + rect.width/2 and abs((self.y + self.height/2) - (rect.y + rect.height/2)) < self.height/2 + rect.height/2
