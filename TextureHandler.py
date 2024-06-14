import pygame
import os


class TextureHandler:
    _textureInstance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._textureInstance:
            cls._textureInstance = super(TextureHandler, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._textureInstance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.textureMap = {}
        self.spritesheet = {}

    def checkFilepath(self,filepath):
        if os.path.isfile(filepath): #if valid path, return
            return True
        return False


    def loadTexture(self,filepath,sprSize=pygame.Vector2(16,16)):
        originalFilepath = filepath
        filepath = "Resources/" + filepath + ".png"
        if not self.checkFilepath(filepath):
            return False

        if str(filepath) in self.textureMap:
            return

        #load file
        texture = pygame.image.load(filepath).convert()
        texture.set_colorkey((0,0,0))

        self.textureMap[originalFilepath] = (texture, sprSize)




    def texture(self,filepath,pos):
        if not str(filepath) in self.textureMap:
            self.loadTexture(filepath,pygame.Vector2(16,16))

        sprsheet = self.textureMap[filepath][0]
        sprSize = self.textureMap[filepath][1]

        SprRow = sprsheet.get_width() / sprSize.x
        topX = (pos % SprRow) * sprSize.x
        topY = (pos // SprRow) * sprSize.x


        rect = pygame.Rect(topX,topY,sprSize.x,sprSize.y)
        img = pygame.Surface(rect.size)
        img.blit(sprsheet, (0, 0), rect)
        img.set_colorkey((0,0,0))

        return img
    
        
            
        
    