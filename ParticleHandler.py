import pygame
import random
from Particles import *
from TextureHandler import TextureHandler


Texture = TextureHandler()

particleArgs = {
    "CycleImg" : True,
    "UseVelocity" : True,
    "Acceleration" : pygame.Vector2(0,2),
    "CycleImgFrequency" : 50,
    "texture" : 0,
    "randomTex" : True,
    "randomTexBounds" : (0,3),
    "spread" : (20,5),
    "lifespan" : 100
    
    }



class ParticleHandler:
    def __init__(self,game):
        Texture.loadTexture("particles",pygame.Vector2(8,8))
        self.game = game
        self.particles = []
    

    def draw(self,surface):
        for i,p in enumerate(self.particles):
            #take particles
            
            #get type value from particle, convert to function
            #i.e. type="default" -> self.default()
            #executes along with particles args
            if hasattr(self,p[2]):
                func = getattr(self,p[2])
            else:
                func = self.default
            funcArgs = p[3]
            func(p,funcArgs)

            img = p[0]
            pos = p[1]

            #decrease particle lifespan
            p[4] -= 1   
            
            #if particle offscreen, kill it
            if (pos.x + img.get_width() + self.game.camera.x < 0 or pos.x + self.game.camera.x > surface.get_width()):
                p[4] = 0

            #draw if alive, else remove
            if p[4] > 0:
                surface.blit(img, pos + self.game.camera)
            else:
                self.particles.pop(i)

    def update(self):
        pass
    


    
    

    def add(self,position,type="default",pArgs=particleArgs):
        #type links to type of particle

        #randomtexture logic
        #takes in particle img coords range for randint
        if particleArgs["randomTex"] == True:
            randomimg = random.randint(pArgs["randomTexBounds"][0],pArgs["randomTexBounds"][1])
            img = Texture.texture("particles",randomimg)
        else:
            img = Texture.texture("particles",pArgs["texture"])
        
        #add spread to position
        position.x += random.randint(-pArgs["spread"][0],pArgs["spread"][0])
        position.y += random.randint(-pArgs["spread"][1],pArgs["spread"][1])

        #add to particles
        self.particles.append([img,position,type,pArgs,pArgs["lifespan"]])
    
    def default(self,particle,pArgs=particleArgs):
        particle[1].x += pArgs["Acceleration"].x * self.game.dt
        particle[1].y += pArgs["Acceleration"].y * self.game.dt

