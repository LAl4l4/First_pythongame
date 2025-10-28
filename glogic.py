import pygame
import random
import noise
import math
from abc import ABC, abstractmethod


WIDTH, HEIGHT = 1200, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    
    

class GameWorld():#干脆就把整个gameworld类传进去吧，省的各种打包
    def __init__(self, totalObj, 
                 drawable, movable, 
                 screen, player):
        self.totalObj = totalObj
        self.drawable = drawable
        self.movable = movable
        self.screen = screen
        self.player = player
        self.attackable = []
        self.canAttack = []
        self.obstacle = []
        self.removedObj = []
        self.DrawXYneeder = []

    def escapeHandle(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
        return None
    
    #统一先传obstacle，全都绕道走
    def updateMove(self):
        for obj, params in self.movable:
            obj.Move(self.obstacle, *params)
            
    def updateDrawXY(self):
        for obj in self.DrawXYneeder:
            obj.updateScreenXY(self.player)
    
    def Draw(self):
        for obj, params in self.drawable:
            obj.Draw(*params)
    
    def generateEnemy():
        pass
                             
    def Attack(self):
        for obj in self.canAttack:
            obj.Atk(self.attackable, self.screen)
            for target in self.attackable:
                if target.hp <= 0 and not isinstance(target, Player):
                    self.removedObj.append(target)

    def updatePackageData(self):
        self.obstacle = []
        self.canAttack = []
        self.attackable = []
        self.DrawXYneeder = []
        for obj in self.totalObj:
            if obj.IsCollidable:
                self.obstacle.append(obj)
            if isinstance(obj, CanAttack):
                self.canAttack.append(obj)
            if isinstance(obj, Attackable):
                self.attackable.append(obj)
            if isinstance(obj, ScreenXYUpdater):
                self.DrawXYneeder.append(obj)
                
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
        self.removedObj = []

class Movable(ABC):
    @abstractmethod
    def Move():
        pass

class AtkSystem(ABC):
    def Atk(self, target, screen):
        self.AtkStatus(target)
        if not self.IsAttacking:
            return
        self.drawAtk(screen)
        if not self.IsDamageTick():
            return
        for TargetObj in target:
            if self.atkType == "player":
                self.AtkPlayer(TargetObj, screen)
            if self.atkType == "enemynormal":
                self.AtkEnemyNormal(TargetObj, screen)
            
    def AtkPlayer(self, target, screen):    #need: IsAttacking，CanAtkWho，atk，hp
        CanAtk = False
        for obj in self.CanAtkWho:
            if isinstance(target, obj):
                CanAtk = True
        if self.IsInRadius(target) and CanAtk:  
            target.hp = target.hp - self.atk
            target.drawOnAtk(screen)
        
    def AtkEnemyNormal(self, target, screen):  #need: IsAttacking，CanAtkWho，atk，hp
        CanAtk = False
        for obj in self.CanAtkWho:
            if isinstance(target, obj):
                CanAtk = True
        if self.IsInRadius(target) and CanAtk:  
            target.hp = target.hp - self.atk
            target.drawOnAtk(screen)
    
    def IsInRadius(self, target): #need：x, y, atkradius
        selfX, selfY = self.GetCenterCoordinate()
        targetX, targetY = target.GetCenterCoordinate()
        dx = selfX - targetX
        dy = selfY - targetY
        return dx*dx + dy*dy <= self.atkradius * self.atkradius
    
    @abstractmethod
    def GetCenterCoordinate(self):    
        pass
    
class Attackable(AtkSystem):
    @abstractmethod
    def drawOnAtk(self, screen):
        pass
    
class CanAttack(AtkSystem):
    @abstractmethod
    def drawAtk(self, screen):
        pass
    
    @abstractmethod
    def AtkStatus(self, targetlist):#更新攻击状态
        pass
    
    @abstractmethod
    def IsDamageTick(self):
        pass
   
class HasCoordinate(ABC):
    @abstractmethod
    def GetScreenXY(self):
        pass
    
    @abstractmethod
    def GetCoordinate(self):
        pass

class ScreenXYUpdater(HasCoordinate):
    def updateScreenXY(self, player):
        playerScreenX, playerScreenY = player.GetScreenXY()
        playerX, playerY = player.GetCoordinate()
        selfX, selfY = self.GetCoordinate()
        screenX = selfX - playerX + playerScreenX
        screenY = selfY - playerY + playerScreenY
        self.LoadScreenCoordinate(screenX, screenY)

    @abstractmethod
    def LoadScreenCoordinate(self, X, Y):
        pass

class Drawable(HasCoordinate):
    @abstractmethod
    def Draw():
        pass
       

class Player(Movable, CanAttack, Drawable, Attackable):
    def __init__(self, NAME, ATK, HP, width, height):
        self.player_width, self.player_height = width, height
        self.player_speed = 10
        self.name = NAME
        self.atk = ATK
        self.hp = HP
        self.atkradius = 150
        self.player_x, self.player_y = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        self.Drawx, self.Drawy = CENTER_X - self.player_width//2, CENTER_Y - self.player_height//2
        self.AtkCounter = 0
        self.facing_right = True 
        
        self.isdmgtick = False
        self.IsAttacking = False
        self.CanAtkWho = [barrier, Enemy]
        self.IsCollidable = False
        self.atkType = "player"

    def GetCoordinate(self):
        return self.player_x, self.player_y
    
    def GetScreenXY(self):
        return self.Drawx, self.Drawy
    
    def GetCenterCoordinate(self):    
        return self.player_x + self.player_width//2, self.player_y + self.player_height//2
         
    def Draw(self, screen, ImgLeft, ImgRight):
        if  self.facing_right:
            screen.blit(ImgRight, (self.Drawx, self.Drawy))
        else:
            screen.blit(ImgLeft, (self.Drawx, self.Drawy))
    
    @staticmethod
    def createplayer(name, atk, hp, width, height):#外部调用的接口
        user1 = Player(name, atk, hp, width, height)
        return user1
    
    def AtkStatus(self, tglist):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.AtkCounter == 0:
            self.AtkCounter = 40
        if self.AtkCounter > 0:
            self.AtkCounter -= 1
        if self.AtkCounter == 35:
            self.isdmgtick = True
        else:
            self.isdmgtick = False
        if self.AtkCounter > 30:
            self.IsAttacking = True
            return
        self.IsAttacking = False
           
    def drawOnAtk(self, screen):
        pass
    
    def drawAtk(self,screen):
        attack_radius = self.atkradius
        player_center = (self.Drawx + self.player_width//2,
                         self.Drawy + self.player_height//2)
        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (player_center[0] - attack_radius, player_center[1] - attack_radius))
    
    def IsDamageTick(self):
        return self.isdmgtick
    
    def Move(self,bars):#传入障碍物数组
        keys = pygame.key.get_pressed()
    # 水平方向移动
        if keys[pygame.K_a]:
            self.player_x -= self.player_speed
            self.facing_right = False
            for bar in bars:
                if self.iscollapse(bar):
                    self.player_x += self.player_speed
        if keys[pygame.K_d]:
            self.player_x += self.player_speed
            self.facing_right = True
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
        
class barrier(ScreenXYUpdater, Attackable, Drawable):
    def __init__(self,x,y,length, Img):
        self.x = x
        self.y = y
        self.length = length
        self.Img = Img
        self.ScreenX = self.x
        self.ScreenY = self.y
        
        self.IsCollidable = True
        self.hp = 1
      
    def create_barrier(length, player, Img):
        x=random.randint(0,int(2*WIDTH-length))
        y=random.randint(0,int(2*HEIGHT-length))
        if x > player.player_x - length and x < player.player_x + player.player_width:
            x = x + length + player.player_width
        if y > player.player_y - length and y < player.player_y + player.player_height:
            y = y + length + player.player_height
        bar = barrier(x,y,length, Img)
        return bar
    
    def BarGetCoodi(self, player):#传入玩家实例
        Bx = self.x - player.player_x + player.Drawx
        By = self.y - player.player_y + player.Drawy
        return Bx, By#返回障碍物在屏幕中的位置

    def drawOnAtk(self, screen):
        pass
    
    def LoadScreenCoordinate(self, X, Y):
        self.ScreenX = X
        self.ScreenY = Y
    
    def GetCoordinate(self):
        return self.x, self.y
        
    def GetScreenXY(self):
        return self.ScreenX, self.ScreenY
        
    def GetCenterCoordinate(self):
        x = self.x
        y = self.y
        return x + self.length//2, y + self.length//2
    
    #draw方法
    def Draw(self, screen, player):
        #出屏幕就不画
        if -self.length < self.ScreenX < WIDTH and -self.length < self.ScreenY < HEIGHT:
            screen.blit(self.Img, (self.ScreenX, self.ScreenY))
    
class Map(Drawable):
    def __init__(self,rowlen,collen,TileSize):
        self.IsCollidable = False
        self.x = 0
        self.y = 0
        self.ScreenX = 0
        self.ScreenY = 0
        
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
    
    @staticmethod    
    def getMap(rowlen,collen,TileSize):#外部调用方法
        map = Map(rowlen,collen,TileSize)
        return map
    
    def GetScreenXY(self):
        return self.ScreenX, self.ScreenY
    
    def GetCoordinate(self):
        return self.x, self.y
    
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
                    
class Enemy(ScreenXYUpdater, CanAttack, Attackable, Movable, Drawable):
    def __init__(self,atk,hp,speed,radius, atkradius, Img):
        self.hp = hp
        self.atk = atk
        self.speed = speed
        self.radius = radius
        self.x = random.randint(0, 2*WIDTH)
        self.y = random.randint(0, 2*HEIGHT)
        self.Img = Img
        self.screen_x = self.x
        self.screen_y = self.y
        
        self.Counter = 0
        self.atkradius = atkradius
        self.IsAttacking = False
        self.isdmgtick = False
        self.CanAtkWho = [Player]
        self.IsCollidable = False
        self.atkType = "enemynormal"
    
    def getEnemy(atk,hp,speed,radius,atkradius, Img):
        enemy = Enemy(atk,hp,speed,radius,atkradius, Img)
        return enemy
    
    def Move(self, notusedobst, player):
        # 计算敌人到玩家的方向向量
        dx = player.player_x - self.x
        dy = player.player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # 如果距离大于0，按比例移动
        if distance > 20:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
            
    def GetCoordinate(self):
        return self.x, self.y
    
    def GetScreenXY(self):
        return self.screen_x, self.screen_y
    
    def LoadScreenCoordinate(self, X, Y):
        self.screen_x = X
        self.screen_y = Y
    
    def Draw(self, screen, player):
        if -self.radius < self.screen_x < WIDTH and -self.radius < self.screen_y < HEIGHT:
            screen.blit(self.Img, (self.screen_x, self.screen_y))
    
    def drawAtk(self, screen):
        attack_radius = self.atkradius
        x, y = self.GetScreenXY()
        x = x + self.radius
        y = y + self.radius
        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (x - attack_radius, y - attack_radius))
    
    def AtkStatus(self, targetlist):
        Atk = False
        for target in targetlist:
            if not self.IsInRadius(target):
                continue
            for cawobj in self.CanAtkWho:
                if isinstance(target, cawobj):
                    Atk = True
        if self.Counter > 0:
            self.Counter -= 1
        if self.Counter == 55:
            self.isdmgtick = True
        elif True:
            self.isdmgtick = False
        if self.Counter > 50:
            self.IsAttacking = True
            return
        if self.Counter == 0 and Atk == True:
            self.Counter = 60
        self.IsAttacking = False
    
    def IsDamageTick(self):
        return self.isdmgtick
    
    def drawOnAtk(self, screen):
        pass
    
    def GetCenterCoordinate(self):
        return self.x + self.radius, self.y + self.radius