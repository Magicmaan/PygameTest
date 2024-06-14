import pygame


if not pygame.font.get_init():
    pygame.font.init()

fontFile = 'Resources\PixeloidMono.ttf'
size = 16


font = pygame.font.Font(fontFile,size)

        
cursorpos = [0,0]
    
    
def write(text,surface,position = []):
    if not position:
        position = cursorpos
    
    image = font.render(text,False,[255,255,255])
    
    surface.blit(image, [position[0],position[1]])