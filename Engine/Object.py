import pygame
from Engine.Program import Program
from Engine.TextureHandler import TextureHandler


Texture = TextureHandler()
game = Program()



class Object(pygame.sprite.Sprite):
    def __init__(self,position,texturePath,texturePos=0,attributes={}):
        pygame.sprite.Sprite.__init__(pygame.sprite.Sprite)
        
        self.position = position
        self.state = "solid"
        self.identifier = "object"
        self.attributes = attributes
        self.flip = False
        self.angle = 0
        self.isAlive = True

        if "identifier" in attributes:
            self.identifier = attributes["identifier"]
        if "flip" in attributes:
            self.flip = attributes["flip"]
        if "angle" in attributes:
            self.angle = attributes["angle"]
        
        #Assign animation tags
        if "animations" in attributes:
            self.hasAnimation = True
            self.AnimationSlides = attributes["animations"]['AnimationSlides']
            self.animationPos = 0
        else:
            self.hasAnimation = False

        self.image = Texture.texture(texturePath,texturePos)
        self.image = pygame.transform.flip(self.image,self.flip,False)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
    
    

    def update(self):
        if hasattr(self,"onTouch"):
            self.onTouch()
        if hasattr(self,"onClick"):
            self.onClick()
        

        self.animationUpdate()


    def draw(self,surface):
        if not (self.rect.right + game.camera.x < 0 or self.rect.left + game.camera.x > surface.get_width()):
            self.isAlive = True
        else:
            self.isAlive = False
        
        if self.isAlive:
            surface.blit(self.image, self.position + game.camera)
    
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
    