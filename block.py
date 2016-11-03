import pygame

class Block:
    #inititalize
    def __init__(self,x,y,width,height,sprite,typ):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0;
        self.sprite = sprite
        self.typ = typ


    def getLeft(self):
        return (self.x,self.y+5,20,self.height-10)
    def getRight(self):
        return (self.x+self.width-20,self.y+5,20,self.height-10)
    def getTop(self):
        return (self.x,self.y,self.width,15)
    def getBottom(self):
        return (self.x,self.y+self.height-5,self.width,5)


        
    #draw object
    def render(self,screen):
        screen.blit(self.sprite,(self.x,self.y))
