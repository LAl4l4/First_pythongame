import pygame
import random
import noise
import math

WIDTH, HEIGHT = 1000, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    
class Player:

    def __init__(self,NAME,ATK,HP):

        self.player_width, self.player_height = 50, 50
        self.player_speed = 10
        self.name = NAME
        self.atk = ATK
        self.hp = HP
        self.player_x, self.player_y = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        self.Drawx, self.Drawy = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        
    def createplayer():
        user1 = Player("Cosmos",10,100)
        return user1
    
    def attack(self, bars, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            attack_radius = 100  # 攻击范围半径
            player_center = (self.player_x + self.player_width//2,
                             self.player_y + self.player_height//2)
            self.drawAtk(screen)
            for bar in bars[:]:
                bar_center = (bar.x + bar.length//2,
                              bar.y + bar.length//2)

                # 距离检测
                distance = math.dist(player_center, bar_center)
                if distance <= attack_radius:
                    bars.remove(bar) 
         
        
    
    
    def drawAtk(self,screen):
        attack_radius = 100
        player_center = (self.Drawx + self.player_width//2,
                         self.Drawy + self.player_height//2)

        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (player_center[0] - attack_radius, player_center[1] - attack_radius))
    
    
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
        Bx = self.x - player.player_x + player.Drawx
        By = self.y - player.player_y + player.Drawy
        return Bx, By
    
    def isAttacked(self, player):
        i = 1
    
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
    
    def draw_map(screen, map_obj, textures, player):
        for row in range(map_obj.rowlen):
            for col in range(map_obj.collen):
                texture_index = map_obj.map[row][col]
                texture = textures[texture_index]

                world_x = row * map_obj.TileSize
                world_y = col * map_obj.TileSize
                screen_x = world_x - player.player_x + player.Drawx
                screen_y = world_y - player.player_y + player.Drawy

                if -map_obj.TileSize < screen_x < WIDTH and -map_obj.TileSize < screen_y < HEIGHT:
                    screen.blit(texture, (screen_x, screen_y))