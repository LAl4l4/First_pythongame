import pygame
import random

WIDTH, HEIGHT = 800, 600
    
class Player:

    def __init__(self,NAME,ATK,HP):
        self.player_x, self.player_y = 400, 300
        self.player_width, self.player_height = 50, 50
        self.player_speed = 10
        self.name = NAME
        self.atk = ATK
        self.hp = HP
        
    def createplayer():
        user1 = Player("Cosmos",10,100)
        return user1
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_w]:
            self.player_y -= self.player_speed
        if keys[pygame.K_s]:
            self.player_y += self.player_speed
        
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x + self.player_width > WIDTH:
            self.player_x = WIDTH - self.player_width
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y + self.player_height > HEIGHT:
            self.player_y = HEIGHT - self.player_height
        
class barrier:
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.length = length
        
    def create_barrier(self):
        x=random.randint(0,HEIGHT-self.length/2)
        y=random.randint(0,WIDTH-self.length/2)
        bar = barrier(x,y)
        return bar