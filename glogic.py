import pygame
import random
import noise

WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    
class Player:

    def __init__(self,NAME,ATK,HP):
        self.player_x, self.player_y = CENTER_X, CENTER_Y
        self.player_width, self.player_height = 50, 50
        self.player_speed = 10
        self.name = NAME
        self.atk = ATK
        self.hp = HP
        
    def createplayer():
        user1 = Player("Cosmos",10,100)
        return user1
    
    def move(self,bars):

        keys = pygame.key.get_pressed()

    # 水平方向移动
        if keys[pygame.K_a]:
            self.player_x -= self.player_speed
            for bar in bars:
                if self.iscollapse(bar):
                    self.player_x += self.player_speed
        if keys[pygame.K_d]:
            self.player_x += self.player_speed
            for bar in bars:
                if self.iscollapse(bar):
                    self.player_x -= self.player_speed

    # 垂直方向移动
        if keys[pygame.K_w]:
            self.player_y -= self.player_speed
            for bar in bars:
                if self.iscollapse(bar):
                    self.player_y += self.player_speed
        if keys[pygame.K_s]:
            self.player_y += self.player_speed
            for bar in bars:
                if self.iscollapse(bar):
                    self.player_y -= self.player_speed
                    
        self.boundary()

    
    def boundary(self):    
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x + self.player_width > 2*WIDTH:
            self.player_x = 2*WIDTH - self.player_width
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y + self.player_height > 2*HEIGHT:
            self.player_y = 2*HEIGHT - self.player_height
            
    def iscollapse(self, bar):
        if (self.player_x + self.player_width > bar.x and
            self.player_x < bar.x + bar.length and
            self.player_y + self.player_height > bar.y and
            self.player_y < bar.y + bar.length):
        #    self.hp = self.hp - 1
            return True
        return False
        
class barrier:
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.length = length
        
    def create_barrier(length):
        x=random.randint(0,int(2*WIDTH-length))
        y=random.randint(0,int(2*HEIGHT-length))
        bar = barrier(x,y,length)
        return bar
    
    def BarGetCoodi(self, player):
        Bx = self.x - player.player_x + CENTER_X
        By = self.y - player.player_y + CENTER_Y
        return Bx, By
    
class Map:
    def __init__(self,rowlen,collen,TileSize):
        scale = 0.15
        self.TileSize = TileSize
        self.rowlen = rowlen
        self.collen = collen
        self.map = [[0 for _ in range(collen)] for _ in range(rowlen)]
        for i in range(rowlen):
            for j in range(collen):
                value = noise.pnoise2(i * scale, j * scale, octaves=4)
                # 归一化到 0~1
                norm_value = (value + 1) / 2  

                # 根据区间分配不同地形
                if norm_value < 0.4:
                    tile = 1   # 水
                elif norm_value < 0.45:
                    tile = 2   # 沙滩
                elif norm_value < 0.55:
                    tile = 0   # 草地
                elif norm_value < 0.6:
                    tile = 6   # 深色草地
                else:
                    tile = 8   # 山地
                self.map[i][j] = tile
        
    def getMap(rowlen,collen,TileSize):
        map = Map(rowlen,collen,TileSize)
        return map