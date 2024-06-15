import pygame
import random
from TextureHandler import TextureHandler
import math

Texture = TextureHandler()

class ParticleHandler:
    def __init__(self,game):
        Texture.loadTexture("particles",pygame.Vector2(8,8))
        self.game = game
        self.particles = []
        self.particleCache = {}
        #power controls amount of offset / effect 0 - 1
        self.windPow = pygame.Vector2(1,0)
        #axis will range from -1 to 1
        self.windAxis = pygame.Vector2(-0.5,0)
    

    

    def draw(self,surface):
        self.windUpdate()
        

        for i,particle in enumerate(self.particles):
            #take particles
            
            #get type value from particle, convert to function
            #i.e. type="default" -> self.default()
            #executes along with particles args

            if hasattr(self,particle[2]):
                particleUpdate = getattr(self,particle[2])
            else:
                particleUpdate = self.defaultUpdate
            
            particleUpdate(particle)

            img = particle[0]
            pos = particle[1]

            #decrease particle lifespan
            particle[4] -= 1   
            
            #if particle offscreen, kill it
            if (pos.x+img.get_width() + self.game.camera.x < 0 or pos.x + self.game.camera.x > surface.get_width()):
                particle[4] = 0

            if (pos.y + img.get_height() + self.game.camera.y < 0) or (pos.y + self.game.camera.y > self.game.camera.y + self.game.resolution[1]):
                particle[4] = 0

            #draw if alive, else remove
            if particle[4] > 0:
                surface.blit(img, pos + self.game.camera)
            else:
                self.particles.pop(i)
        
        self.particleCache.clear()

    def update(self):
        pass
    


    
    

    def add(self,position,type="default",count=1,addArgs={}):
        #type links to type of particle
        if count<1:
            count = 1
        for n in range(count):
            pos = position.copy()
            if hasattr(self,type+"Add"):
                typeArgs = getattr(self,type+"Add")
            else:
                typeArgs = self.defaultAdd
            
            particleArgs = typeArgs(addArgs)
            #random offset for animations
            particleArgs["randomOffset"] = [random.uniform(-1,1),random.uniform(-0.25,0.25)]

            #randomtexture logic
            #takes in particle img coords range for randint
            if particleArgs["randomTex"] == True:
                randomImg = random.randint(particleArgs["randomTexBounds"][0],particleArgs["randomTexBounds"][1])
                img = Texture.texture("particles",randomImg)
            else:
                img = Texture.texture("particles",particleArgs["texture"])
            
            #add spread to position
            pos.x += random.randint(-particleArgs["spread"][0],particleArgs["spread"][0])
            pos.y += random.randint(-particleArgs["spread"][1],particleArgs["spread"][1])
            #add to particles
            self.particles.append([img,pos,type+"Update",particleArgs,particleArgs["lifespan"]])
    

    def leafAdd(self,addArgs={}):
        if "Acceleration" in addArgs.keys():
            addAccel = addArgs["Acceleration"]
        else:
            addAccel = pygame.Vector2(0,0)
        
        particleArgs = {
            "CycleImg" : True,
            "UseVelocity" : True,
            "Acceleration" : pygame.Vector2(random.uniform(-2.5,2.5) + addAccel.x, random.uniform(10,15) + addAccel.y),
            "CycleImgFrequency" : 50,
            "texture" : 4,
            "randomTex" : True,
            "randomTexBounds" : (4,5),
            "spread" : (10,5),
            "lifespan" : random.randint(100,300),
            "canFlip" : True
        }

        return particleArgs

    def defaultAdd(self,addArgs={}):
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

        return particleArgs

    def defaultUpdate(self,particle):
        pArgs = particle[3]

        particle[1].x += pArgs["Acceleration"].x * self.game.dt + self.windOffset.x
        particle[1].y += pArgs["Acceleration"].y * self.game.dt + self.windOffset.y
    

    def leafUpdate(self,particle):
        pArgs = particle[3]


        #get cached particle physics to apply
        if not "leaf" in self.particleCache.keys():
            particleCalculations = pygame.Vector2()

            particleCalculations.x = math.sin(self.game.tick%360/random.randint(2,5))
            particleCalculations.y = math.cos((self.game.tick%360)/6)

            particleCalculations = particleCalculations + self.windOffset

            self.particleCache["leaf"] = particleCalculations

        particleCalculations = self.particleCache["leaf"]


        #update particle position
        particle[1].x += particleCalculations.x + pArgs["randomOffset"][0]
        particle[1].y += (pArgs["Acceleration"].y * self.game.dt) + particleCalculations.y + pArgs["randomOffset"][1]
        

        if pArgs["canFlip"]:
            if random.randint(0,5) == 0:
                particle[0] = pygame.transform.flip(particle[0],True,False)
 

    def windUpdate(self):
        self.windAxis.x = math.sin((self.game.tick%360) / 100)

        self.windOffset = pygame.Vector2(self.windPow * self.windAxis)

        if self.windOffset == 0:
            self.windOffset = pygame.Vector2(0,0)

