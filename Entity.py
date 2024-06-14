import pygame
import math
from Program import Program
from TextureHandler import TextureHandler
from CollisionHandler import *
from pprint import pprint

game = Program()
Texture = TextureHandler()

class Entity(pygame.sprite.Sprite):
    def __init__(self,position,texturePath,attributes):
        pygame.sprite.Sprite.__init__(pygame.sprite.Sprite)
        
        self.position = position
        self.identifier = "entity"
        self.state = "idle"
        self.lastInput = ""
        self.flip = False
        self.isAlive = True
        
        self.gravity = 10
        self.onGround = False
        self.isMoving = False
        self.velocity = pygame.math.Vector2(0,0)
        self.maxVelocity = pygame.math.Vector2(1.5,50)

        #collisions setup
        self.collisions = {}
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False

        #texture setup
        self.texturePath = texturePath
        self.image = Texture.texture(self.texturePath,0)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
        self.attributes = attributes

        if "identifier" in attributes:
            self.identifier = attributes["identifier"]
        if "rect" in attributes:
            self.rect = pygame.Rect(self.position.x, self.position.y, attributes["rect"][0], attributes["rect"][1])
        if "maxVelocity" in attributes:
            self.maxVelocity = attributes["maxVelocity"]
        if "gravity" in attributes:
            self.gravity = attributes["gravity"]

        #Assign animation tags
        if "animations" in attributes:
            self.hasAnimation = True
            self.AnimationSlides = attributes["animations"]['AnimationSlides']
            self.animationPos = 0
        else:
            self.hasAnimation = False
        

        
        
        
    
    def update(self):
        self.onGround = False
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False
        
        #check and update collisions
        collideUpdate(self,game.floorColliders,game.tileMap)
        
        self.position += self.velocity
        self.rect.update(self.position.x, self.position.y, self.rect.width, self.rect.height)

        self.animationUpdate()

        self.image = pygame.transform.flip(self.image,self.flip,False)


        
    
    def animationUpdate(self):
        if not self.hasAnimation: #if no animations, return from function
            return

        #gets last entry in animationSlides state, which is FPS value
        animationFPS = self.AnimationSlides[self.state][-1]
        #checks remainder againsts game tick, if so increment animation
        if game.tick % animationFPS == 0:
            self.animationPos += 1


        #animation overflow check
        if self.animationPos >= len(self.AnimationSlides[self.state])-1:
            self.animationPos = 0
        
        #getSprite()
        #from objects animation slides, takes in the self.state values and animation position
        #this returns a number corresponding to position on spritesheet for getSprite()
        
        #get spritesheet pos
        pos = self.AnimationSlides[self.state][self.animationPos]
        filepath = "player/spritesheet"
        self.image = Texture.texture(self.texturePath,pos)
        
            
        
    
    def draw(self,surface):
        tx = self.position.copy()
        tx.y = round(tx.y,0)

        if self.isAlive:
            surface.blit(self.image, round(tx + game.camera,0))


        

        