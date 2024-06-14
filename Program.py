import pygame
import TextGUI

from InputHandler import InputHandler
from SettingsClass import Settings
from Debugger import Debugger
from TextureHandler import TextureHandler
from ParticleHandler import ParticleHandler
from Particles import *
from TileMap import TileMap


gInput = InputHandler() #initialise input handler

class Program:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Program, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        pygame.init() #initialise pygame
        pygame.display.set_caption("Game")
        
        gInput.pollInput() 
        settings = Settings()
        
        self.Outputresolution = [settings.windowWidth,settings.windowHeight] #setup Window
        self.resolution = [settings.gameWidth,settings.gameHeight]
        self.framerate = 60
        self.screenOutput = pygame.display.set_mode(self.Outputresolution) 
        self.screen = pygame.Surface(self.resolution)
        print("Key Repeat val: " + str(pygame.key.get_repeat()))

        pygame.key.set_repeat(500,500)

        self.clock = pygame.time.Clock() 
        self.running = True
        self.dt = 0
        self.tick = 0
        self.camera = pygame.Vector2(0,0)
        
        #Sprite Groups
        self.allSprites = pygame.sprite.Group()
        self.PhysSprites = pygame.sprite.Group()
        self.allObjects = pygame.sprite.Group()
        self.wallColliders = pygame.sprite.Group()
        self.floorColliders = pygame.sprite.Group()
        self.debugGroup = pygame.sprite.Group()
        
        #Render Layers
        self.renderLayers = {
            "Background" : pygame.Surface(self.resolution), #BACKGROUND
            "Foreground" : pygame.Surface(self.resolution), #FOREGROUND
            "Particles" : pygame.Surface(self.resolution), #PARTICLES
            "GUI" : pygame.Surface(self.resolution), #GUI
        }
        for i,l in self.renderLayers.items():
            l.set_colorkey((0,0,0))
    
        


        self.textures = TextureHandler()
        self.tileMap = TileMap(self)
        self.particles = ParticleHandler(self)
        self.particles.add(pygame.Vector2(20,20),"balls")

        self.debugger = Debugger(self,self.screenOutput,True,True,True)
        
        
        
    def update(self):
        gInput.pollInput()
        
        self.allObjects.update()
        self.allSprites.update()

        self.particles.update()

        
        
    def draw(self,p):
        self.screen.fill("gray")


        for i,layer in self.renderLayers.items():
            layer.fill((0,0,0))
        
        self.drawGroup(self.allSprites,self.renderLayers["Foreground"])

        self.tileMap.draw(self.screen)
        self.particles.draw(self.renderLayers["Particles"])
        self.screen.blit(self.renderLayers["Foreground"],(0,0))
        self.screen.blit(self.renderLayers["Particles"],(0,0))
        frame = pygame.transform.scale(self.screen, self.Outputresolution) #output to frame and draw to screen
        self.screenOutput.blit(frame, frame.get_rect())
        
        self.debugger.draw()
        
        
        pygame.display.flip()   
        
    
    def stop(self):
        self.running = False

        #save settings

        


        #exit window and close pygame
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()


    def drawGroup(self,group,surface):
        for spr in group.sprites():
            if hasattr(spr,"draw"):
                spr.draw(surface)
        
