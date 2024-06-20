import pygame
import os.path
from Engine import TextFont


if not pygame.font.get_init():
    pygame.font.init()

fontFile = 'Resources\PixeloidMono.ttf'
size = 16


font = pygame.font.Font(fontFile,size)

        
cursorpos = [0,0]
def initFont():
    #font array size
    fontSize = 5

    fontSurfaces = {}
    fontSurfaces["Blank"] = pygame.Surface((fontSize,fontSize))
    fontSurfaces["Blank"].set_colorkey((0,0,0))
    
    #constructs surfaces for font from array of pixels
    for letter,array in TextFont.letters.items():
        surface = pygame.Surface((fontSize,fontSize))
        surface.fill((0,0,0,0))
        surface.set_colorkey((0,0,0))

        for y in range(len(array)):
            for x in range(len(array[0])):
                if array[y][x] == 1:
                    surface.set_at((x,y), (255,255,255,255))

        fontSurfaces[letter] = surface
        print("Added letter: " + letter)

    return fontSurfaces

def write(text,surface,position = [0,0],color = (255,255,255,255)):
    image = font.render(text,False,[255,255,255])

    #apply tint
    image.fill(color,special_flags=pygame.BLEND_RGBA_MULT)

    surface.blit(image, [position[0],position[1]])

def writeNew(text,surface,position,font,color=(0,255,0)):
    n=0
    for l in text:
        image = font["Blank"]
        if l.upper() in font.keys():
            image = font[l.upper()]
            

        image.fill(color,special_flags=pygame.BLEND_RGBA_MULT)
        #print("printed letter")
        surface.blit(image, [position[0] + (n*(image.get_width()+1)),position[1]])
        n += 1