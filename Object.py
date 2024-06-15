import pygame
from Program import Program
from TextureHandler import TextureHandler


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
        
        self.image = Texture.texture(texturePath,texturePos)
        self.image = pygame.transform.flip(self.image,self.flip,False)

       

        
        
        
        
        
        
        self.rect = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
    
    
    def draw(self,surface):
        if not (self.rect.right + game.camera.x < 0 or self.rect.left + game.camera.x > surface.get_width()):
            self.isAlive = True
        else:
            self.isAlive = False
        
        if self.isAlive:
            surface.blit(self.image, self.position + game.camera)
    