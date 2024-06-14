from Entity import Entity
from Texture import Texture
from Program import Program
from InputHandler import InputHandler
import random

gInput = InputHandler()


import pygame
import math

game = Program()

class Player(Entity):
    def __init__(self,position):
        texturePath = "player/spritesheet"

        animations = {}
        animations['AnimationSlides'] = {
            "idle": (0,1,2,3,20),
            "run": (4,5,6,7,8),
            "jump": (8,1),
            "crouch" : (9,1),
        }
        
        attributes = {
            "animations" : animations,
            "identifier" : "player",
        }

        Entity.__init__(self,position,texturePath,attributes)

       
        self.jumpHeight = -5
        self.accel = 1
        self.friction = 10

        
        
        
    
        
    
    def Position(self):
        if abs(self.velocity.x) > (self.maxVelocity.x): #max velocity speed cap
            self.velocity.x = math.copysign(self.maxVelocity.x, self.velocity.x)


        if not self.isMoving: #slow down if not moving
            self.velocity.x = self.velocity.x * (1-self.friction * game.dt)
            if math.isclose(self.velocity.x, 0,abs_tol=0.05):
                self.velocity.x = 0
        
        if not self.onGround: #gravity if not on ground
            self.velocity.y += self.gravity * game.dt

        #vertical speed cap
        self.velocity.y = min(self.maxVelocity.y, self.velocity.y) 

        
    
    
    
    def update(self):
        self.isMoving = False
        self.state = "idle"
        
        if gInput.jump() and self.onGround:
            self.onGround = False
            self.velocity.y = self.jumpHeight 
            self.lastInput = "jump"
            self.state = "jump"
            
        if gInput.left() and not self.collisions["left"]:
            self.velocity.x -= self.accel * game.dt
            self.isMoving = True
            self.flip = True
            self.state = "run"
        if gInput.right() and not self.collisions["right"]:
            self.velocity.x += self.accel * game.dt
            self.isMoving = True
            self.flip = False
            self.state = "run"
        
        if gInput.L_CTRL():
            self.state = "crouch"

        
        
        

        self.Position() 

        self.gfxUpdate()

        super().update()
    

    def gfxUpdate(self):
        feetPos = pygame.Vector2(self.rect.centerx,self.rect.bottom)
        midPos = pygame.Vector2(self.rect.center)
        randomNum = random.randint(0,100)

        if self.velocity.x < 0:
            veloffsetX = 10
        else:
            veloffsetX = -10

        pArgs = {
            "CycleImg" : True,
            "UseVelocity" : True,
            "Acceleration" : pygame.Vector2(random.uniform(-5,5) + veloffsetX,random.uniform(5,25)),
            "CycleImgFrequency" : 50,
            "texture" : 0,
            "randomTex" : True,
            "randomTexBounds" : (0,3),
            "spread" : (5,10),
            "lifespan" : random.randint(25,80),
        }

        if self.velocity.x == 0:
            if randomNum < 2: game.particles.add(midPos,"default",pArgs)
        else:
            if randomNum < 8: game.particles.add(midPos,"default",pArgs)


