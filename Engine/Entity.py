import pygame
import math
import random
from Engine.Program import Program
from Engine.TextureHandler import TextureHandler
from Engine.CollisionHandler import *
from pprint import pprint

game = Program()
Texture = TextureHandler()

class Entity(pygame.sprite.Sprite):
    def __init__(self,position,texturePath,texturePos=0,attributes={}):
        pygame.sprite.Sprite.__init__(pygame.sprite.Sprite)
        
        self.position = position
        self.identifier = "entity"
        self.state = "idle"
        self.flip = False
        self.isAlive = True
        
        self.input = ""
        self.lastInput = self.input

        self.gravity = 10

        self.onGround = False
        self.onGroundTimer = 0
        self.friction = 10

        self.canMove = pygame.Vector2(1,1)
        self.isMoving = False
        self.isMovingTimer = 0

        self.velocity = pygame.math.Vector2(0,0)
        self.maxVelocity = pygame.math.Vector2(1.5,10)

        #collisions setup
        self.collisions = {}
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False

        #texture setup
        self.texturePath = texturePath
        self.image = Texture.texture(self.texturePath,0)

        self.useOutline = False
        self.imageOutline = False
        self.outlineColour = (255,0,255)

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
        if abs(self.velocity.x) > (self.maxVelocity.x * game.TimeMult): #max velocity speed cap
            self.velocity.x = math.copysign(self.maxVelocity.x * game.TimeMult, self.velocity.x)

        if not self.isMoving: #slow down if not moving
            self.velocity.x *= (1- self.friction * game.dt)
            if math.isclose(self.velocity.x, 0,abs_tol=0.05):
                self.velocity.x = 0
        
        if not self.onGround: #gravity if not on ground
            self.velocity.y += (self.gravity * game.dt) / game.TimeMult
        #vertical speed cap
        self.velocity.y = min(self.maxVelocity.y * game.TimeMult, self.velocity.y) 



        self.onGround = False
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False
        
        #check and update collisions
        collideUpdate(self,game.floorColliders,game.tileMap)


          
          
        self.position += self.velocity
        self.rect.update(self.position.x, self.position.y, self.rect.width, self.rect.height)

        if not self.onGround:
            self.onGroundTimer += 1
        else:
            self.onGroundTimer = 0      
        if not self.isMoving:
            self.isMovingTimer += 1
        else:
            self.isMovingTimer = 0   
        
        if self.isMovingTimer > game.afkTimer:
            self.state = "afk"


        self.animationUpdate()
        self.image = pygame.transform.flip(self.image,self.flip,False)


        
    
    def animationUpdate(self):
        if not self.hasAnimation: #if no animations, return from function
            return

        if not self.state in self.AnimationSlides.keys():
            state = "idle"
        else:
            state = self.state
            

        #gets last entry in animationSlides state, which is FPS value
        animationFPS = self.AnimationSlides[state][-1]
        #checks remainder againsts game tick, if so increment animation
        if game.tick % (animationFPS // game.TimeMult) == 0:
            self.animationPos += 1


        #animation overflow check
        if self.animationPos >= len(self.AnimationSlides[state])-1:
            self.animationPos = 0
        
        #getSprite()
        #from objects animation slides, takes in thestate values and animation position
        #this returns a number corresponding to position on spritesheet for getSprite()
        
        #get spritesheet pos
        pos = self.AnimationSlides[state][self.animationPos]
        self.image = Texture.texture(self.texturePath,pos)
        
        
    
    def draw(self,surface):
        #obj rect doesn't always match sprite
        #must adjust image to be centered inside rect
        correctedPos = pygame.Vector2(self.rect.centerx - self.image.get_width()/2, self.rect.centery - self.image.get_height()/2)
        correctedPos.y = round(correctedPos.y,2)

        if self.isAlive:
            if self.useOutline:
                self.drawOutline(surface,correctedPos.copy())

            surface.blit(self.image, round(correctedPos + game.camera,0))

    def drawOutline(self, surface, pos):
        #convert sprite to mask then back to surface to produce monochrome outline
        image = pygame.mask.from_surface(self.image).to_surface()
        image.fill(self.outlineColour,special_flags=pygame.BLEND_RGBA_MULT)
        image.set_colorkey((0,0,0))
        # Blit the BW outline, offset around main player
        surface.blit(image, (round(pos.x-1 + game.camera.x), round(pos.y + game.camera.y))) #left
        surface.blit(image, (round(pos.x+1 + game.camera.x), round(pos.y + game.camera.y))) #right
        surface.blit(image, (round(pos.x-1 + game.camera.x), round(pos.y-1 + game.camera.y))) #up
        surface.blit(image, (round(pos.x-1 + game.camera.x), round(pos.y+1 + game.camera.y))) #down



        

        