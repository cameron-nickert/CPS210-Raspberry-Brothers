import pygame

class Goomba:

    #inititalize
    def __init__(self,x,y,w,h,sprite,typ):
        
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.velocity = 0;
        self.falling = True
        self.onGround = False
        self.jumping = False
        self.turbo = False
        self.groundChanged = False
        self.moveBy = -1
        self.typ = typ
        self.sprite = sprite
        self.seeImage = 5
        self.direction = 1
        self.calls = 0;


    #player jump
    def jump(self):
        if(self.onGround==True):
            self.velocity=8
            self.onGround = False
            self.jumping = True
        


    #checks turbo value before moving 
    def moveX(self,moveBy):
        self.calls += 1;
        if(self.calls==7):
            self.calls = 0
            if(moveBy>0):
                if(not self.seeImage == 18 and not self.seeImage==17):
                    self.seeImage = 17
                elif(not self.seeImage == 17 and not self.seeImage==16):
                    self.seeImage = 16
                elif(not self.seeImage == 16 and not self.seeImage==18):
                    self.seeImage = 18
            elif(moveBy<0):
                if(not self.seeImage == 13 and not self.seeImage==11):
                    self.seeImage = 11
                elif(not self.seeImage == 11 and not self.seeImage==12):
                    self.seeImage = 12
                elif(not self.seeImage == 12 and not self.seeImage==13):
                    self.seeImage = 13
            else:
                if(self.direction>0):
                    self.seeImage = 15
                else:
                    self.seeImage = 14
                    
            self.direction = moveBy
        
            
        if(self.turbo):
            return moveBy*1.5
        else:
            return moveBy

    def getLeft(self):
        return (self.x,self.y+5,20,self.height-10)
    def getRight(self):
        return (self.x+self.width-20,self.y+5,20,self.height-10)
    def getTop(self):
        return (self.x,self.y,self.width,15)
    def getBottom(self):
        return (self.x,self.y+self.height-10,self.width,10)

    def intersects(self,playerSideBox,sideBox):
        x1,y1,w1,h1 = playerSideBox
        x2,y2,w2,h2 = sideBox
        
        #check up downs
        if (x2+w2 >= x1 >= x2 and y2+h2 >= y1 >=y2):
            return True
        elif (x2+w2 >= x1 + w1 >= x2 and y2+h2 >= y1>=y2):
            return True
        elif (x2+w2 >= x1 >= x2 and y2+h2 >= y1 + h1 >=y2):
            return True
        elif (x2+w2 >= x1 + w1 >= x2 and y2+h2 >= y1 + h1 >=y2):
            return True


    #detects collisions with itself
    def doesCollide(self,block):
        x2 = block.x
        y2 = block.y
        w2 = block.width
        h2 = block.height
        typ = block.typ

        up = ""
        down = ""
        left = ""
        right = ""

        collided = False

        #intersects the left side of block, then its on my right                        
        if( self.intersects( self.getRight(), block.getLeft() ) ):
            if(typ=="block"):
                self.x-=1
                self.moveBy = -1
                collided = True
        elif( self.intersects( self.getLeft(),block.getRight() ) ):
            if(typ=="block"):
                self.x+=1
                self.moveBy = 1
                collided = True
        elif( self.intersects( self.getBottom(),block.getTop() ) ):
            if(typ=="block"):
                self.falling = False
                self.onGround = True
                self.groundChanged = True
                if(not self.jumping):
                    self.velocity = 0;
                
                self.y=block.y-self.height
                collided = True
        elif( self.intersects( self.getTop(),block.getBottom() ) ):
            if(typ=="block"):
                self.onGround = False
                self.falling = True
                self.velocity = -8;
                self.Jumping = False
                self.groundChanged = True
                self.y = block.y + block.height
                collided = True
        
        return collided
    #update values
    def update(self, gravity, blockList):
        self.groundChanged = False
        
        #falling?
        if(self.velocity<0):
            self.falling = True
            self.jumping = False


        up = ""
        down = ""
        left = ""
        right = ""
        blockX,blockY,blockW,blockH = 0,0,0,0



        #iterate through every block in the level
        for block in blockList:

            #changes values if it collides
            if(768>=block.x>=0):
                self.doesCollide(block)
                    

        if(self.groundChanged==False):
            self.onGround = False

        #only fall if on ground
        if(not self.onGround or self.falling):
            self.velocity += gravity

            if(self.velocity>8):
                self.velocity = 8
            elif(self.velocity<-5):
                self.velocity = -5


        self.x += self.moveX(self.moveBy)            
        self.y -= self.velocity



        

    #draw object
    def render(self,screen):
        #pygame.draw.rect(screen,(0,100,0),(self.x,self.y,self.width,self.height))
        screen.blit(self.sprite,(self.x,self.y))
        

        
