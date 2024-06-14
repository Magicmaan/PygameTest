import pygame
import os

#TextureType
#0 = single text
#1 = Spritesheet

class Texture:
    def __init__(self,filepath,isSpriteSheet=None,SpriteSize=pygame.math.Vector2(0,0)):
        fileName,fileExt = self.checkFilepath(filepath)
        filepath = fileName+fileExt
        self.filepath = filepath
        self.imageSrc = pygame.image.load(self.filepath)
        self.image = self.imageSrc
        
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        
        if self.image.get_alpha is None:
            self.image = self.image.convert()
        else:
            self.image = self.image.convert_alpha()
        
        
        if isSpriteSheet:   
            self.SpriteSheet = True
            self.SpriteSize = SpriteSize
            self.SpriteSheetSize = pygame.math.Vector2((self.width//self.SpriteSize.x),(self.height//self.SpriteSize.y))
    
    def checkFilepath(self,filepath):
        fileName, fileExtension = os.path.splitext(filepath) #split to filename and path

        if os.path.isfile(filepath): #if valid path, return
            return fileName, fileExtension
        else: 
            if not fileExtension: #if file has no extension, try again with .png on end, if not return False
                return self.checkFilepath(filepath + ".png")
            else: #if totally invalid, return False
                return False

    def getSprite(self,sprPos,returnSprite=False):
        #takes in x = 0, ..n and converts to X and Y on on large spritesheet
        #returns nothing as overrides texture image output
        w = self.imageSrc.get_width()
        h = self.imageSrc.get_height()
        #convert j = 0,n to x and y coordinate  
        topX = (sprPos % (w / 11)) * 11
        topY = (sprPos % (h / 19)) * 19
        if sprPos == 2:
            print(w)
            print(h)
            print((sprPos % (w / 11)))
            print(sprPos % (h / 19))
            print(topX)
            print(topY)
            print(sprPos % self.SpriteSheetSize.y)

        #construct pygame rect to size of sprite
        rectangle = [topX, topY, self.SpriteSize.x, self.SpriteSize.y]
        rect = pygame.Rect(rectangle)
        
        #make new surface and extract sprite from source sheet
        image = pygame.Surface(rect.size)
        image.blit(self.imageSrc, (0, 0), rect)
        
        
        if image.get_alpha is None: #check if alpha and correctly mask
            image = image.convert()
        else:
            image = image.convert_alpha()
        image.set_colorkey((0,0,0))

        #set image to sprite
        self.image = image
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        if returnSprite:
            return image

