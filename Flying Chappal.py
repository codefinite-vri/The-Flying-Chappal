# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 12:20:29 2020

@author: user
"""
#importing libraries
import pygame
import math
import random
from pygame import mixer

#initializing pygame
pygame.init()

#create screen
s_h=600
s_w=800
screen=pygame.display.set_mode((s_w, s_h))

#background image
background  = pygame.image.load('bgf.jpg')
background=pygame.transform.scale(background, (800,600 ))

#set caption
pygame.display.set_caption("FLYING CHAPPAL")

#set icon
icon=pygame.image.load('mothera.png')
pygame.display.set_icon(icon)

#create player
player_img=pygame.image.load('mother.png')
player_img=pygame.transform.scale(player_img, (100, 184))
playerX = 370
playerY = 420
playerX_change = 0

#kid image
kid_img=[]
kidX=[]
kidY=[]
kidX_change=[]
kidY_change=[]
num_of_kids = 5
kid_image=[pygame.transform.scale(pygame.image.load('kid.png'), (80, 100)), pygame.transform.scale(pygame.image.load('kid2.png'), (100, 100)), pygame.transform.scale(pygame.image.load('kid3.png'), (60, 100)), pygame.transform.scale(pygame.image.load('kid4.png'), (100, 60)), pygame.transform.scale(pygame.image.load('kid5.png'), (60, 100))]
for i in range(num_of_kids):
    kid_img.append(kid_image[i])
    kidX.append(random.randint(0, 700))
    kidY.append(random.randint(100,200))
    kidX_change.append(3)
    kidY_change.append(40)

#slipper
slipper_img = pygame.image.load('slipper.gif')
slipper_img=pygame.transform.scale(slipper_img, (40, 80))
slipperX=0
slipperY=420
slipperX_change=0
slipperY_change=15
slipper_state="ready"


score_value=0
font=pygame.font.Font('freesansbold.ttf', 32)
textX =10
textY = 10

#GAME OVER
game_over_font=pygame.font.Font('freesansbold.ttf',64)  
        
def player(x,y):
    screen.blit(player_img, (x, y))

def kid(x,y):
    screen.blit(kid_img[i], (x, y))
    
def slipper(x,y):
    global slipper_state
    slipper_state="fire"
    screen.blit(slipper_img,(x,y))    
    

#collision detection
def isCollision(kidX, kidY, slipperX, slipperY):
    distance = math.sqrt((math.pow(kidX - slipperX,2))+(math.pow(kidY-slipperY,2)))
    if distance<27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Score: "+str(score_value), True, (0,0,0))
    screen.blit(score,(x,y))
    
def game_over_text():
    game_over_text=game_over_font.render("GAME OVER!", True, (0,0,0))
    screen.blit(game_over_text, (200,250))

    
#main Game loop
running=True
while running:
    #RGB FORMAT
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                running=False      
                
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change = -3
            if event.key==pygame.K_RIGHT:
                playerX_change = 3
            if event.key==pygame.K_SPACE:
                if slipper_state=="ready":
                    slipper_sound=mixer.Sound('throw.wav')
                    slipper_sound.play()
                    slipperX=playerX
                    slipper(slipperX, slipperY)
                
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
    
#check boundaries
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=700:
        playerX=700
        
    
        
    #kid movement
    for i in range(num_of_kids):
        if kidY[i]>390:
            for j in range(num_of_kids):
                kidY[j]=2000
            game_over_text()
            break
        
        kidX[i]+=kidX_change[i]
        if kidX[i]<=0:
            kidX_change[i]=3
            kidY[i]+=kidY_change[i]
        elif kidX[i]>=736:
            kidX_change[i]=-3
            kidY[i]+=kidY_change[i] 
        
        
        #colision detection
        collision = isCollision(kidX[i], kidY[i], slipperX, slipperY)
        if collision:
            slipperY = 420
            slipper_state="ready"
            col_sound=mixer.Sound('ouch.wav')
            col_sound.play()
            score_value+=1
            
            #respawn the kid
            kidX[i] = random.randint(0,700)
            kidY[i]= random.randint(100,200)
    
        kid(kidX[i], kidY[i])
        
    
    #slipper movement
    if slipperY<=0:
        slipperY=420
        slipper_state="ready"
        
    if slipper_state=="fire":
        slipper(slipperX, slipperY)
        slipperY-= slipperY_change    
    
    player(playerX, playerY)
    show_score(textX, textY)
    
    #update the screen
    pygame.display.update() 
pygame.quit()
