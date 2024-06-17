from Entity import Entity
from Program import Program
from InputHandler import InputHandler
import random
import numpy

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
            "afk" : (8,9,10)
        }
        
        attributes = {
            "animations" : animations,
            "identifier" : "player",
            "rect" : (10,16),
            #"maxVelocity" : pygame.Vector2(100,20)
        }

        Entity.__init__(self,position,texturePath,attributes)

       
        self.jumpHeight = -2.5
        self.jumpCoyote = 10

        self.accel = 5
        self.friction = 10


        
    def Position(self):
        return
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
        self.lastInput = self.input

        if gInput.crouch():
            self.friction = 5
            self.jumpHeight = -3
            self.accel = 1
            self.maxVelocity.update(0.5,5)
            self.state = "crouch"
            #game.particles.add(pygame.Vector2(self.rect.center),"leaf",count=50)
        else:
            self.jumpHeight = -2.5
            self.friction = 10
            self.accel = 5
            self.maxVelocity.update(1.5,10)


        #if on ground, or x number of frame after being on ground
        if gInput.jump() and self.velocity.y >= 0 and ((self.onGround or self.onGroundTimer < self.jumpCoyote)):
            self.onGround = False
            self.velocity.y = self.jumpHeight
            if gInput.crouch():
                self.velocity.y *= 1.5
            self.state = "jump"
            self.input = "jump"
            game.particles.add(pygame.Vector2(self.rect.center),"leaf",count=10)


        if gInput.left() and self.canMove[0] and not self.collisions["left"]:
            self.velocity.x -= self.accel * game.dt
            self.isMoving = True
            self.flip = True
            self.state = "run"
            self.input = "left"
            if self.lastInput == "right":
                self.velocity.x = -abs(self.velocity.x / 1.5)

        if gInput.right() and self.canMove[0] and not self.collisions["right"]:
            self.velocity.x += self.accel * game.dt
            self.isMoving = True
            self.flip = False
            self.state = "run"
            self.input = "right"
            if self.lastInput == "left":
                self.velocity.x = abs(self.velocity.x / 1.5)
        

        


            

        
        
        

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
            "Acceleration" : pygame.Vector2(random.uniform(-2.5,2.5) + veloffsetX,random.uniform(10,50)),
            "CycleImgFrequency" : 50,
            "texture" : 0,
            "randomTex" : True,
            "randomTexBounds" : (4,5),
            "spread" : (5,10),
            "lifespan" : random.randint(100,300),
            "canFlip" : True
        }

        #if self.velocity.x == 0:
        #    if randomNum < 50: game.particles.add(midPos,"leaf")
        #else:
        #    if randomNum < 80: game.particles.add(midPos,"leaf",{"Acceleration":pygame.Vector2(veloffsetX,0)})


