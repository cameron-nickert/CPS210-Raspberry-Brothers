import pygame
from player import *
from block import *
from goomba import *
from level_data import *

pygame.init()


#game initialize
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Super Raspberry Bros.")

num_joysticks = 0
joysticks = []

gravity = -.2
player_1 = Player(150,0,pygame.image.load("berry.png"))
player_2 = Player(100,0,pygame.image.load("raz.png"))

#created Level_Data so my main class wasn't messy
level_data = Level_Data()
current_level = []
fromWin = False


def menu():    
    # for al the connected joysticks
    global num_joysticks
    num_joysticks = pygame.joystick.get_count();
    for i in range(0, num_joysticks):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print "Detected joystick '",joysticks[-1].get_name(),"'"


    clock = pygame.time.Clock()
    shutdownHoldingMillis = 0
    global fromWin
    
    startPlaying = False
    keepPlaying = True
    
    while not startPlaying:
        clock.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    startPlaying = True
                    keepPlaying = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    startPlaying = True
                    keepPlaying = False
            elif event.type == pygame.JOYBUTTONDOWN:
                #shutdown request
                if(event.button==8):
                    shutdownHoldingMillis = pygame.time.get_ticks()
                
            elif event.type == pygame.JOYBUTTONUP:
                #escape/shutdownbutton end
                if event.button == 8:
                    if(pygame.time.get_ticks()-shutdownHoldingMillis > 3000):
                        from subprocess import call
                        call("sudo nohup shutdown -h now",
                        shell=True)
                    else:
                        startPlaying = True
                        keepPlaying = False
                #anyone press A to start playing
                elif event.button == 0:
                    startPlaying = True
                    keepPlaying = True

        #display start screen
        screen.fill((50,100,150))
        if(fromWin):
            screen.blit(pygame.image.load("end.png"),(0,0),(0,0,800,600))
        else:
            screen.blit(pygame.image.load("home.png"),(0,0),(0,0,800,600))
        pygame.display.flip()

                            
    #if they pressed an escape keep
    if not keepPlaying:
        pygame.quit()
    
    #load level 1 data
    global current_level
    current_level = level_data.load_level(screen,1)
    start_level()
    
    print "Main Menu"

def pause():
    print "Paused"


def play():
    print "Continued"


def start_level():
    global player_1
    global player_2
    
    clock = pygame.time.Clock()
    shutdownHoldingMillis = 0
    fromDeath = False
    global fromWin
    fromWin = False
    blockList = []
    enemyList = []
    #reading data and creating world
    for y in range(0,len(current_level)):
        for x in range(0,len(current_level[y])):
            #1 is plain block
            if (current_level[y][x]==1):
                blockList.append(Block(x*32,y*32,32,32,pygame.image.load("block.png"),"block"))
            elif(current_level[y][x]==2):
                blockList.append(Block(x*32,y*32,64,64,pygame.image.load("pipe.gif"),"block"))
            elif(current_level[y][x]==3):
                enemyList.append(Goomba(x*32,y*32,32,32,pygame.image.load("goomba.gif"),"goomba"))
            elif(current_level[y][x]==8):
                enemyList.append(Goomba(x*32,y*32,32,32,pygame.image.load("bigGoomba.png"),"goomba"))
            elif(current_level[y][x]==9):
                blockList.append(Block(x*32,y*32,32,32,pygame.image.load("pipe.gif"),"flag"))


    #player move values
    player_1X,player_1Y=0,0
    player_2X,player_2Y=0,0
    
    
    keepPlaying = True
    while keepPlaying:

        #every 60 milliseconds
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "Received event 'Quit', exiting."
                    keepPlaying = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print "Escape key pressed, exiting."
                    keepPlaying = False
                
                elif event.type == pygame.JOYBUTTONDOWN:
                    #print "Joystick '",event.joy," - ",joysticks[event.joy].get_name(),"' button",event.button,"down."


                    #shutdown request
                    if(event.button==8):
                        shutdownHoldingMillis = pygame.time.get_ticks()
                    else:
                        #player 1 input-end
                        if event.joy == 0:
                            if event.button == 0:
                                player_1.jump()
                                print "1 A"
                            elif event.button == 1:
                                player_1.turbo = True
                            else:
                                print "1 ",event.button
                        #player 2 input-end
                        elif event.joy == 1:
                            if event.button == 0:
                                player_2.jump()
                                print "1 A"
                            elif event.button == 1:
                                player_2.turbo = True
                            else:
                                print "2 ",event.button

                elif event.type == pygame.JOYBUTTONUP:
                    #print "Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up."

                    #escape/shutdownbutton end
                    if event.button == 8:
                        if(pygame.time.get_ticks()-shutdownHoldingMillis > 3000):
                            from subprocess import call
                            call("sudo nohup shutdown -h now",
                            shell=True)
                        else:
                            keepPlaying = False
                    else:
                        
                        #player 1 input-end
                        if event.joy == 0:

                            if event.button == 0:
                                print "1 A - release"
                            elif event.button == 1:
                                print "1 B"
                                player_1.turbo = False
                            else:
                                print "1 ",event.button
                        #player 2 input-end
                        elif event.joy == 1:
                            if event.button == 0:
                               print "2 A - release"
                            elif event.button == 1:
                                print "2 B"
                                player_2.turbo = False
                            else:
                                print "2 ",event.button

                        
                elif event.type == pygame.JOYHATMOTION:
                    #player 1 input dpad
                    if event.joy == 0:
                        if event.value == (-1,0) or event.value == (-1,1) or event.value == (-1,-1):
                            player_1X = -2 #left
                        elif event.value ==(1,0) or event.value == (1,1) or event.value == (1,-1):
                            player_1X = 2 #right
                        elif event.value ==(0,-1):
                            print "1 down"
                        else:
                            player_1X = 0
                    #player 2 input dpad
                    elif event.joy == 1:
                        if event.value == (-1,0) or event.value == (-1,1) or event.value == (-1,-1):
                            player_2X = -2 #left
                        elif event.value ==(1,0) or event.value == (1,1) or event.value == (1,-1):
                            player_2X = 2 #right
                        elif event.value ==(0,-1):
                            print "2 down"
                        else:
                            player_2X = 0
 

        #render after input checks
        screen.fill((50,100,150))


        #as far as the player 1 moves, shift everything else
        if(player_1.x <= level_data.left_viewbox):
            view_difference = level_data.left_viewbox - player_1.x
            player_1.x = level_data.left_viewbox
            player_2.x += view_difference
            for block in blockList:
                block.x += view_difference
            for enemy in enemyList:
                enemy.x += view_difference
        if(player_1.x >= level_data.right_viewbox):
            view_difference = level_data.right_viewbox - player_1.x
            player_1.x = level_data.right_viewbox
            player_2.x += view_difference
            for block in blockList:
                block.x += view_difference
            for enemy in enemyList:
                enemy.x += view_difference

        #as far as the player 2 moves, shift everything else
        if(player_2.x <= 0):
            player_2X = 5
        elif(player_2.x >= 768):
            player_2X = -5

        for block in blockList:
            block.render(screen)
        for enemy in enemyList:
            if(768>=enemy.x>=0):
                enemy.update(gravity,blockList)
            enemy.render(screen)
            
        player_1.update(gravity,blockList,enemyList,player_1X)
        player_1.render(screen)

        if num_joysticks>1:
            player_2.update(gravity,blockList,enemyList,player_2X)
            player_2.render(screen)

        pygame.display.flip()

        if(player_1.die or player_2.die or player_1.y>600 or player_2.y>600):
            fromDeath = True
            break
        elif(player_1.win or player_2.win):
            fromWin = True
            break

    #if the game is done because of death, start over
    if(fromDeath):
        player_1 = Player(150,0,pygame.image.load("berry.png"))
        player_2 = Player(100,0,pygame.image.load("raz.png"))
        start_level()
    if(fromWin)
        menu()
        
menu()
pygame.quit()
