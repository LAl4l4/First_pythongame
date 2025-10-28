import pygame
from abc import ABC, abstractmethod
import math
import glogic

class interfaceManager():
    def __init__(self, screen, basepath, gameworld):
        self.screen = screen
        self.window = "menu"
        self.basepath = basepath
        self.font = pygame.font.SysFont("Arial", 40)
        self.menu = mainMenu(self.screen, self.font)
        self.gameworld = gameworld
        
    def LoadEvents(self, events):
        self.event = events
        
    def quitHandle(self):#返回是否继续循环
        if self.window == "quit":
            return False
        return True
        
    def drawWindow(self):
        if self.window == "menu":
            self.menu.drawMenu()
        elif self.window == "game":
            self.gameworld.updateMove()
            self.gameworld.Draw()
            self.gameworld.Attack()
            self.gameworld.updateRemoveObjects()
            self.gameworld.updatePackageData()
            self.gameworld.updateDrawXY()
        
    def updateWindow(self):
        choice = None
        if self.window == "menu":
            choice = self.menu.clickHandle(self.event)   
        elif self.window == "game":
            choice = self.gameworld.escapeHandle(self.event)
                                  
        if choice == "start":
            self.window = "game"
        elif choice == "quit":
            self.window = "quit"
        elif choice == "menu":
            self.window = "menu"

class loadtexture(ABC):
    @abstractmethod
    def loadtex(self):
        pass
                    
class mainMenu(loadtexture):
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.buttons = {
            "start": pygame.Rect(300, 200, 200, 60),
            "quit": pygame.Rect(300, 300, 200, 60),
        }
        
    def loadtex(self):
        return super().loadtex()
        
    def drawMenu(self):
        self.screen.fill((30, 30, 60))
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (100, 100, 200), rect)
            label = self.font.render(text.upper(), True, (255, 255, 255))
            self.screen.blit(label, (rect.x + 50, rect.y + 15))
            
    def clickHandle(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for name, rect in self.buttons.items():
                    if rect.collidepoint(mx, my):
                        return name
        return None      


class gameLoader():
    def __init__(self, screen, basepath):
        self.screen = screen
        self.basepath = basepath
    
    def iniGame(self):
        pass