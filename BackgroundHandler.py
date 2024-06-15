import pygame


class BackgroundHandler:
    def __init__(self,game,BGSequence={}):
        self.game = game

        defaultBG = [
            pygame.image.load("resources/background0.png").convert(),
            pygame.image.load("resources/background1.png").convert(),
            pygame.image.load("resources/background2.png").convert(),
        ]
        defaultBG[0].set_colorkey((0,0,0))
        defaultBG[1].set_colorkey((0,0,0))
        defaultBG[2].set_colorkey((0,0,0))

        self.bgSequence = defaultBG
    
    def draw(self,surface):
        offsets = [False,5,3]
        n=0
        for bg in self.bgSequence:
            if offsets[n]:
                camOffsetX = (self.game.camera.x % (surface.get_width()*3)) / offsets[n]

                surface.blit(bg,(camOffsetX - bg.get_width(),0))
                surface.blit(bg,(camOffsetX,0))
                surface.blit(bg,(camOffsetX + bg.get_width(),0))
            else:
                 surface.blit(bg,(0,0))

            
            n += 1