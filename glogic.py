import pygame
import random
import noise
import math
from abc import ABC, abstractmethod


WIDTH, HEIGHT = 1000, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    
class Attackable(ABC):
    @abstractmethod
    def GetCoordinate(self):    
        pass
    
    @abstractmethod
    def OnAttack(self,player):#返回true如果这个物体被消灭
        pass

class Movable(ABC):
    @abstractmethod
    def Move():
        pass

class Drawable(ABC):
    @abstractmethod
    def Draw():
        pass
    
class CanAttack(ABC):
    @abstractmethod
    def Attack():
        pass

class GameWorld:
    def __init__(self, totalObj, drawable, movable, attackable, canAttack):
        self.totalObj = totalObj
        self.drawable = drawable
        self.movable = movable
        self.attackable = attackable
        self.canAttack = canAttack
        self.removedObj = []
        self.IsUserAttacking = False
        
    def updateMove(self):
        for obj, params in self.movable:
            obj.Move(*params)
            
    def updateDraw(self):
        for obj, params in self.drawable:
            obj.Draw(*params)
    
    def updateAttack(self):
        for obj, params in self.attackable:
            if not self.IsUserAttacking:
                return
            if obj.OnAttack(*params):
                self.removedObj.append(obj)
        self.IsUserAttacking = False
                
    def updateCanAttack(self):
        for obj, params in self.canAttack:
            if obj.Attack(*params):
                self.IsUserAttacking = True
                
    def updateRemoveObjects(self):
        for obj in self.removedObj:
            if obj in self.totalObj:
                self.totalObj.remove(obj)
            
        for obj, params in self.drawable[:]:
            if obj in self.removedObj:
                self.drawable.remove((obj, params))
        
        for obj, params in self.movable[:]:
            if obj in self.removedObj:
                self.movable.remove((obj, params))
                
        for obj, params in self.attackable[:]:
            if obj in self.removedObj:
                self.attackable.remove((obj, params))
        
        self.removedObj = []
    
class Player(Movable, CanAttack):
    def __init__(self,NAME,ATK,HP):
        self.player_width, self.player_height = 50, 50
        self.player_speed = 10
        self.name = NAME
        self.atk = ATK
        self.hp = HP
        self.atkradius = 100
        self.player_x, self.player_y = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        self.Drawx, self.Drawy = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        self.AtkCounter = 0
        
    def createplayer():#外部调用的接口
        user1 = Player("Cosmos",10,100)
        return user1
    
    def Attack(self, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.AtkCounter == 0:
            self.AtkCounter = 40 
        if self.AtkCounter > 0:
            self.AtkCounter -= 1
        if self.AtkCounter > 30:
            self.drawAtk(screen)
            return True
        return False
           
    def drawAtk(self,screen):
        attack_radius = self.atkradius
        player_center = (self.Drawx + self.player_width//2,
                         self.Drawy + self.player_height//2)
        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (player_center[0] - attack_radius, player_center[1] - attack_radius))
    
    
    def Move(self,bars):#传入障碍物数组
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
            
    def iscollapse(self, bar):#传入障碍物
        if (self.player_x + self.player_width > bar.x and
            self.player_x < bar.x + bar.length and
            self.player_y + self.player_height > bar.y and
            self.player_y < bar.y + bar.length):
            return True
        return False
        
class barrier(Attackable, Drawable):
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.length = length
        
        
    def create_barrier(length):
        x=random.randint(0,int(2*WIDTH-length))
        y=random.randint(0,int(2*HEIGHT-length))
        bar = barrier(x,y,length)
        return bar
    
    def BarGetCoodi(self, player):#传入玩家实例
        Bx = self.x - player.player_x + player.Drawx
        By = self.y - player.player_y + player.Drawy
        return Bx, By#返回障碍物在屏幕中的位置
    #被攻击直接消失，返回true
    def OnAttack(self, player):
        px = player.player_x + player.player_width // 2
        py = player.player_y + player.player_height // 2
        closestX = max(self.x, min(px, self.x + self.length))
        closestY = max(self.y, min(py, self.y + self.length))
        dx = px - closestX
        dy = py - closestY
        distance_sq = dx * dx + dy * dy
        if distance_sq <= player.atkradius * player.atkradius: 
            return True
        return False
        
    def GetCoordinate(self):
        x = self.x
        y = self.y
        return x, y
    
    #draw方法
    def Draw(self, screen, player):
        #算出距离玩家绘制坐标的差值
        screen_x = self.x - player.player_x + player.Drawx
        screen_y = self.y - player.player_y + player.Drawy
        #出屏幕就不画
        if -self.length < screen_x < WIDTH and -self.length < screen_y < HEIGHT:
            pygame.draw.rect(screen, (128,255,128), (screen_x,screen_y,self.length,self.length))
    
class Map(Drawable):
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
        
    def getMap(rowlen,collen,TileSize):#外部调用方法
        map = Map(rowlen,collen,TileSize)
        return map
    
    def Draw(self, screen, textures, player):#map_obj是getmap返回的，textures是被切割好的图形数组
        for row in range(self.rowlen):
            for col in range(self.collen):
                texture_index = self.map[row][col]
                texture = textures[texture_index]

                world_x = row * self.TileSize
                world_y = col * self.TileSize
                screen_x = world_x - player.player_x + player.Drawx
                screen_y = world_y - player.player_y + player.Drawy

                if -self.TileSize < screen_x < WIDTH and -self.TileSize < screen_y < HEIGHT:
                    screen.blit(texture, (screen_x, screen_y))
                    
class Enemy(Attackable, Movable, Drawable, ABC):
    def __init__(self,atk,hp,speed,radius):
        self.hp = hp
        self.atk = atk
        self.speed = speed
        self.radius = radius
        self.x = random.randint(0, 2*WIDTH)
        self.y = random.randint(0, 2*HEIGHT)
        
    def getEnemy(atk,hp,speed,radius):
        enemy = Enemy(atk,hp,speed,radius)
        return enemy
    
    def Move(self, player):
        # 计算敌人到玩家的方向向量
        dx = player.player_x - self.x
        dy = player.player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # 如果距离大于0，按比例移动
        if distance > 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
            
    def Draw(self, screen, player):
        screen_x = self.x - player.player_x + player.Drawx
        screen_y = self.y - player.player_y + player.Drawy
        if -self.radius < screen_x < WIDTH and -self.radius < screen_y < HEIGHT:
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, self.radius, self.radius))
    
    def OnAttack(self, player):
        px = player.player_x + player.player_width // 2
        py = player.player_y + player.player_height // 2
        closestX = max(self.x, min(px, self.x + self.radius))
        closestY = max(self.y, min(py, self.y + self.radius))
        dx = px - closestX
        dy = py - closestY
        distance_sq = dx * dx + dy * dy
        if distance_sq <= player.atkradius * player.atkradius: 
            self.hp = self.hp - player.atk
        if self.hp < 0 :
            return True
        return False
    
    def GetCoordinate(self):
        return self.x,self.y