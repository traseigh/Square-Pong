'''
Created on Jul 14, 2020

@author: treokwai
'''

from random import randint
import pygame
from pygame.constants import MOUSEBUTTONDOWN

import requests

class Ball(pygame.sprite.Sprite):
    #This sprite class represents the ball
    def __init__(self,color,width,height,speed,players):
        super().__init__()
    #defined the width, height and color of ball  
        self.image = pygame.Surface([width,height]) 
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.speed = speed
        self.players = players
    #Drawing ball
        pygame.draw.rect(self.image,color,[0,0, width,height])
        self.velocity = [randint(4,8), randint(-8,8)] 
    # Get ball when called
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.collide()
        
    def collide(self):
        if self.rect.x >= 690:
            self.velocity[0] = -self.velocity[0]
        if self.rect.x<=0:
            self.velocity[0] = -self.velocity[0]
        if self.rect.y>490:
            self.velocity[1] = -self.velocity[1]
        if self.rect.y<0:
            self.velocity[1] = -self.velocity[1]          
        
        if pygame.sprite.spritecollide(self,self.players, False):
            self.bounce()  
                    
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)

        
class Paddle(pygame.sprite.Sprite):
    #Sprite represents that paddle and derives from the "Sprite" class
    def __init__(self,color,width,height,speed): 
        super().__init__()
    #defined the width, height and color of ball  
        self.image = pygame.Surface([width,height]) 
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.speed = speed
        pygame.draw.rect(self.image,color,[0,0, width,height])
        self.rect = self.image.get_rect()
        self.position = 0
   
    def update(self,ball_list):
        self.rect.y += self.position
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 400:
            self.rect.y = 400

class Opponent(pygame.sprite.Sprite):
    #Sprite represents that paddle and derives from the "Sprite" class
    def __init__(self,color,width,height,speed): 
        super().__init__()
        self.image = pygame.Surface([width,height]) 
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.speed = speed
        pygame.draw.rect(self.image,color,[0,0, width,height])
        self.rect = self.image.get_rect()
        
    def update(self,ball_list):
        if self.rect.y > ball.rect.y:
            self.rect.y -= self.speed
        if self.rect.y < ball.rect.y:
            self.rect.y += self.speed
            
        if self.rect.y > 400:
            self.rect.y = 400
    
        if self.rect.y < 0:
            self.rect.y = 0          
class Game:
    #Game manager handles ball and player updates
    def __init__(self,ball_list,player_list):
        self.ball_list = ball_list
        self.player_list = player_list
        
        
    def run (self):
        ball_list.draw(screen)
        player_list.draw(screen)
        self.player_list.update(self.ball_list)
        self.ball_list.update()
        
        
#--------------------------------------------------------------      
#             GAME SETUP
#-------------------------------------------------------------- 
pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,165,0)
RED = (255,0,0)

HEIGHT = 500
WIDTH = 700
#Program speed in frames per second
# instantiating game window 

FPSClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Square Pong")

player = Paddle(ORANGE,10,100,5)
player.rect.x = 20
player.rect.y = 200

opponent = Opponent(RED,10,100,7)
opponent.rect.x= 670
opponent.rect.y = 200


player_list = pygame.sprite.Group()
player_list.add(player)
player_list.add(opponent)



ball = Ball(WHITE,10,10,5,player_list)
ball.rect.x=345
ball.rect.y = 195
ball_list = pygame.sprite.GroupSingle()
ball_list.add(ball)
    
player_score=0
opponent_score =0

font = pygame.font.Font('freesansbold.ttf', 74)
game_on = Game(ball_list,player_list)
    
clock = pygame.time.Clock()  
#-----------------------------------------------
#             GAME RUNNER
#-----------------------------------------------
intro = True
while intro:
    screen.fill(BLACK)  
    text = font.render(str("Start Game"), 1, WHITE)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            intro = False

    screen.blit(text, (200,200))
    pygame.display.flip()
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.position -= player.speed
            if event.key == pygame.K_DOWN:
                player.position += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.position += player.speed
            if event.key == pygame.K_DOWN:
                player.position -= player.speed
        
    if ball.rect.x >= 690:
        player_score +=1
    if ball.rect.x <=0:
        opponent_score +=1
           

    screen.fill(BLACK)  
    pygame.draw.line(screen,WHITE,[349,0],[349,500], 5)
    
    
    text = font.render(str(player_score), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(opponent_score), 1, WHITE)
    screen.blit(text, (420,10))
    game_on.run()
# Drawing initial paddles
    pygame.display.flip()
    clock.tick(60)
pygame.quit()