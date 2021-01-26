# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:05:43 2019

@author: Matthijs Schrage
"""

import pygame
import time
import random

pygame.init()

#Used colors
black = (0, 0, 0)
white = (255, 255, 255)
crash_text_color = (255, 51, 51)
start_button_color = (51, 255, 51)
exit_button_color = (255, 102, 0)
dark_start_button_color = (51, 200, 51)
dark_exit_button_color = (255, 0, 0)

#Creating window, title and clock
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The Olypmic White Water Rapids')
clock = pygame.time.Clock()
pause = False

#Quit function
def quit_now():
    pygame.quit()
    quit()
    
#Background image
backgroundImg = pygame.image.load('Water.png').convert()

def image(img):
    Img = pygame.image.load(img).convert_alpha()
    Img_mask = pygame.mask.from_surface(Img)
    Img_rect = Img.get_rect()
    return Img, Img_mask, Img_rect

#log function
def draw_on_position(thingx, thingy, image):
    gameDisplay.blit(image, (thingx, thingy))

#Counting number of dodged things
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Points: ' + str(count), True, black)
    gameDisplay.blit(text, (0,0))

#Text on screen functions
def text_objects(text, font, color):
    textSurf = font.render(text, True, color)
    return textSurf, textSurf.get_rect()

def message_display_crash(text, color): #function dependend on the text that you want to display
    Font_and_size = pygame.font.Font('freesansbold.ttf',115) #font type and size of the message
    TextSurface, TextRectangle = text_objects(text, Font_and_size, color)
    TextRectangle.center = ((display_width/2),(display_height/2)) #The message will be in the center of the screen
    gameDisplay.blit(TextSurface, TextRectangle) #Actually shows the text
    
    pygame.display.update() #Updates the screen. Because we dont draw the boat its position wont be updated.
    
    time.sleep(2)
    
    game_loop()

#Crash function
def crash():
    message_display_crash('You crashed', crash_text_color)

"""
def noncrash(xthing, ything, w, factor, bonus, a, speed, b):
    xthing = random.randrange(0, (display_width - w))
    ything = - factor * display_height
    bonus += a
    speed += b
    """
    
def crash_collisionCheck(x1, x2, y1, y2, mask2, mask1, action=None):
    offset = (int(x1 - x2), int(y1 - y2))
    result = mask2.overlap(mask1, offset)
    if result:
        action()
    return result

#Button function
def button(msg,x,y,w,h,ic,ac,action=None):
     mousePos = pygame.mouse.get_pos()
     click = pygame.mouse.get_pressed()
        
     if x + w > mousePos[0] > x and y + h > mousePos[1] > y:
         pygame.draw.rect(gameDisplay, ac,(x, y, w, h))
         if click[0] == 1 and action != None:
             action()
     else:
         pygame.draw.rect(gameDisplay, ic,(x, y, w, h))

     Font_and_size2 = pygame.font.Font('freesansbold.ttf',20)
     textSurface, textRectangle = text_objects(msg, Font_and_size2, white)
     textRectangle.center = ( (x+(w/2) ),(y+(h/2) ) ) #The message will be in the center of the screen
     gameDisplay.blit(textSurface, textRectangle)

#Intro screen
def game_intro():
    
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_now()
        
        gameDisplay.fill(white)
        Font_and_size1 = pygame.font.Font('freesansbold.ttf',40) #font type and size of the message
        TextSurface, TextRectangle = text_objects('The Olypmic White Water Rapids', Font_and_size1, black)
        TextRectangle.center = ((display_width/2),(display_height/2)) #The message will be in the center of the screen
        gameDisplay.blit(TextSurface, TextRectangle) #Actually shows the text
        
        button('Start',250, 400, 100, 50,dark_start_button_color,start_button_color, game_loop)
        button('Quit',450, 400, 100, 50,dark_exit_button_color,exit_button_color, quit_now)

        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pause = False

#Pause screen
def paused():
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_now()
        
        draw_on_position(0, 0, backgroundImg)
        Font_and_size1 = pygame.font.Font('freesansbold.ttf',40) #font type and size of the message
        TextSurface, TextRectangle = text_objects('Paused', Font_and_size1, black)
        TextRectangle.center = ((display_width/2),(display_height/2)) #The message will be in the center of the screen
        gameDisplay.blit(TextSurface, TextRectangle) #Actually shows the text
        
        button('Continue',250, 400, 100, 50,dark_start_button_color,start_button_color, unpause)
        button('Quit',450, 400, 100, 50,dark_exit_button_color,exit_button_color, quit_now)

        pygame.display.update()
        clock.tick(15)

#Game event function
def game_loop():
    global pause
    
    #Creating a variable where we can express the location after movement
    x = (display_width * 0.42)
    y = (display_height * 0.4)
    boat_speed = 10
    x_change = 0
    y_change = 0
    
    #Making rock in a random position and checking if it does collide with boat right away
#    rock_startx = random.randrange(0, (display_width - image('Rock2.png')[2].w))
#    rock_starty = random.randrange(0.5 * display_height, (display_height - image('Rock2.png')[2].h))
#    offset_rock_boat = (int(rock_startx - x), int(rock_starty - y))
#    result_rock_boat = image('Raft.png')[1].overlap(image('Rock2.png')[1], offset_rock_boat)
#    if result_rock_boat:
#        rock_startx = random.randrange(0, (display_width - image('Rock2.png')[2].w))
#        rock_starty = random.randrange(0, (display_height - image('Rock2.png')[2].h))
    
    #Log starting values
    log_speed = 6
    log_startx = random.randrange(0, (display_width - image('Log.png')[2].w))
    log_starty = - image('Log.png')[2].h 
    
    #Log2 starting values
    log2_speed = 8
    log2_startx = random.randrange(0, (display_width - image('Log2.png')[2].w))
    log2_starty = - image('Log2.png')[2].h  
    
    #Log3 starting values
    log3_speed = 12
    log3_startx = random.randrange(0, (display_width - image('Log3.png')[2].w))
    log3_starty = - image('Log3.png')[2].h  

    nemo_speed = 10
    nemo_startx = random.randrange(0, (display_width - image('Nemo.png')[2].w))
    nemo_starty = - image('Nemo.png')[2].h
    
    baracuda_speed = 15
    baracuda_startx = random.randrange(0, (display_width - image('Baracuda.png')[2].w)) 
    baracuda_starty = - 3 * display_height
    
    points = 0

    #Creating the event
    gameExit = False
    while not gameExit:
        
        for event in pygame.event.get(): #any event that happens per frame (clicking or shooting for example)
            if event.type == pygame.QUIT: #first check if the user wants to quit
                    quit_now()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -boat_speed #moves the boat x pixels to the left
                
                elif event.key == pygame.K_RIGHT:
                    x_change = boat_speed #moves the boat x pixels to the right
                
                elif event.key == pygame.K_UP: 
                    y_change = -boat_speed
                
                elif event.key == pygame.K_DOWN:
                    y_change = boat_speed
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                
            if event.type == pygame.KEYUP: #what happens when the key is released again
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 #When the player has let go of a key the boat stops moving
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
            
        x += x_change #New x-position of the boat 
        y += y_change #New y-position of the boat
            
    
        draw_on_position(0, 0, backgroundImg) #Draw background BEFORE we draw the boat   
        
#        draw_on_position(rock_startx, rock_starty, image('Rock2.png')[0])

        draw_on_position(log_startx, log_starty, image('Log.png')[0]) #Update drawing position of log
        log_starty += log_speed #Update y-position of log
        
        if points > 14:
            draw_on_position(log2_startx, log2_starty, image('Log2.png')[0]) #Update drawing position of log2
            log2_starty += log2_speed #Update y-position of log2
        
        if points > 30:
            draw_on_position(log3_startx, log3_starty, image('Log3.png')[0]) #Update drawing position of log3
            log3_starty += log3_speed #Update y-position of log3
        
        draw_on_position(nemo_startx, nemo_starty, image('Nemo.png')[0]) #Update drawing position of nemo
        nemo_starty += nemo_speed #Update y-position of nemo
        
        draw_on_position(baracuda_startx, baracuda_starty, image('Baracuda.png')[0]) #Update drawing position of baracuda
        baracuda_starty += baracuda_speed #Update y-position of baracuda
        
        draw_on_position(x,y,image('Raft.png')[0]) #Drawing boat AFTER background at the new coördinates
       
        things_dodged(points) #Points drawn last
        
        #Logic
        #Border definition
        while x > (display_width - image('Raft.png')[2].w) or x < 0 or y + image('Raft.png')[2].h > display_height or y < 0:
            crash() #runs the crashfunction

        
        #Collision between boat and rock
#        crash_collisionCheck(rock_startx, x, rock_starty, y, image('Raft.png')[1], image('Rock2.png')[1], crash)
        
        #Makes the things come to the top again
        if log_starty > display_height:
            log_starty = - image('Log.png')[2].h
            log_startx = random.randrange(0, (display_width - image('Log.png')[2].w) )
            points += 1
            log_speed += 0.5
        
        if log2_starty > display_height and points > 14:
            log2_starty = - image('Log2.png')[2].h
            log2_startx = random.randrange(0, (display_width - image('Log2.png')[2].w) )
            points += 1
            log2_speed += 0.5
        
        if log3_starty > display_height and points > 14:
            log3_starty = - image('Log3.png')[2].h
            log3_startx = random.randrange(0, (display_width - image('Log3.png')[2].w) )
            points += 1
            log3_speed += 0.5
            
        if baracuda_starty > display_height:
            baracuda_starty = - 3 * display_height
            baracuda_startx = random.randrange(0, (display_width - image('Baracuda.png')[2].w) )
        
        if nemo_starty > display_height:
            nemo_starty = - 0.5 * display_height
            nemo_startx = random.randrange(0, (display_width - image('Nemo.png')[2].w) )
        
        crash_collisionCheck(log_startx, x, log_starty, y, image('Raft.png')[1], image('Log.png')[1], crash) #Crash between log and boat
        if points > 14:
            crash_collisionCheck(log2_startx, x, log2_starty, y, image('Raft.png')[1], image('Log2.png')[1], crash) #Crash between log2 and boat
        if points > 30:
           crash_collisionCheck(log3_startx, x, log3_starty, y, image('Raft.png')[1], image('Log3.png')[1], crash) #Crash between log3 and boat

        """
        offset_rock_log = (int(rock_startx - log_startx), int(rock_starty - log_starty))
        result_rock_log = image('Log.png')[1].overlap(image('Rock2.png')[1], offset_rock_log)
        if result_rock_log:
            log_starty = - random.randrange(image('Log.png')[2].h, display_height)
            log_startx = random.randrange(0, (display_width - image('Log.png')[2].w))
            """

        """
        offset_rock_log2 = (int(rock_startx - log2_startx), int(rock_starty - log2_starty))
        result_rock_log2 = image('Log2.png')[1].overlap(image('Rock2.png')[1], offset_rock_log2)
        if result_rock_log2:
            log2_starty = - random.randrange(image('Log2.png')[2].h, display_height)
            log2_startx = random.randrange(0, (display_width - image('Log2.png')[2].w))
            """
        
        #Collisionfunction nemo
        offset_nemo_boat = (int(nemo_startx - x), int(nemo_starty - y))
        result_nemo_boat = image('Raft.png')[1].overlap(image('Nemo.png')[1], offset_nemo_boat)
        if result_nemo_boat:
            nemo_startx = random.randrange(0, (display_width - image('Nemo.png')[2].w))
            nemo_starty = - display_height
            points += 1
            nemo_speed += 0.2
        """
        offset_rock_nemo = (int(rock_startx - nemo_startx), int(rock_starty - nemo_starty))
        result_rock_nemo = image('Nemo.png')[1].overlap(image('Rock2.png')[1], offset_rock_nemo)
        if result_rock_nemo:
            nemo_starty = - random.randrange(image('Nemo.png')[2].h, display_height)
            nemo_startx = random.randrange(0, (display_width - image('Nemo.png')[2].w))
            """
        #Collisionfunction baracuda
        offset_baracuda_boat = (int(baracuda_startx - x), int(baracuda_starty - y))
        result_baracuda_boat = image('Raft.png')[1].overlap(image('Baracuda.png')[1], offset_baracuda_boat)
        if result_baracuda_boat:
            baracuda_startx = random.randrange(0, (display_width - image('Baracuda.png')[2].w))
            baracuda_starty = - 4 * display_height
            boat_speed += 1
            baracuda_speed += 0.2
        """
        offset_rock_baracuda = (int(rock_startx - baracuda_startx), int(rock_starty - baracuda_starty))
        result_rock_baracuda = image('Baracuda.png')[1].overlap(image('Rock2.png')[1], offset_rock_baracuda)
        if result_rock_baracuda:
            baracuda_starty = - 4 * display_height
            baracuda_startx = random.randrange(0, (display_width - image('Baracuda.png')[1].w))
            """
        
        pygame.display.update() #Updates the screen in the new situation, without this the drwaings would not be shown
        clock.tick(30) #The screen will be update 30 times per second

game_intro()

quit_now()