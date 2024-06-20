import pygame
import random
import math

from Engine.TextureHandler import TextureHandler


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
        self.particleCache.clear()

        self.pwindUpdate()
        for i,particle in enumerate(self.particles):
            #take particles
            
            #get type value from particle, convert to function
            #i.e. type="default" -> self.pdefaultUpdate()
            #executes along with particles args

            if hasattr(self,"p"+particle[2]+"Update"):
                particleUpdate = getattr(self,"p"+particle[2]+"Update")
            else:
                particleUpdate = self.pdefaultUpdate
            
            particleUpdate(particle)

            img = particle[0]
            pos = particle[1]


             
            
            #if particle offscreen, kill it
            if (pos.x+img.get_width() + self.game.camera.x < 0 or pos.x + self.game.camera.x > surface.get_width()):
                particle[4] = 0

            if (pos.y + img.get_height() + self.game.camera.y < 0) or (pos.y + self.game.camera.y > self.game.camera.y + self.game.resolution[1]):
                particle[4] = 0

            

            #draw if alive, else remove
            if (particle[4] / self.game.TimeMult) > 0:
                surface.blit(img, pos + self.game.camera)
                #decrease particle lifespan
                particle[4] -= 1  
            else:
                self.particles.pop(i)
        
        

    def add(self,position,type="default",count=1,addArgs={}):
        #type links to type of particle
        if count<1:
            count = 1
        for n in range(count):
            pos = position.copy()
            #if function for type exists.
            #i.e. type="default" -> pdefaultAdd()
            if hasattr(self,"p"+type+"Add"):
                typeArgs = getattr(self,"p"+type+"Add")
            else:
                typeArgs = self.pdefaultAdd
            
            particleArgs = typeArgs(addArgs)
            #random offset for animations
            particleArgs["randomOffset"] = [random.uniform(0.25,1),random.uniform(-0.25,0.25)]

            #takes in particle img coords range for randint
            if particleArgs["randomTex"] == True:
                randomImg = random.randint(particleArgs["randomTexBounds"][0],particleArgs["randomTexBounds"][1])
                img = Texture.texture("particles",randomImg)
            else:
                img = Texture.texture("particles",particleArgs["texture"])
            
            #add spread to position
            pos.x += random.randint(-particleArgs["spread"][0],particleArgs["spread"][0])
            pos.y += random.randint(-particleArgs["spread"][1],particleArgs["spread"][1])

            #add to particle list
            self.particles.append([img,pos,type,particleArgs,particleArgs["lifespan"]])
    

    def pleafAdd(self,addArgs={}):
        addAccel = pygame.Vector2(0,0)
        if "Acceleration" in addArgs.keys():
            addAccel = addArgs["Acceleration"]
        particleArgs = {
            "UseVelocity" : True,
            "Acceleration" : pygame.Vector2(random.uniform(-1.5,1.5) + addAccel.x, random.uniform(0,10) + addAccel.y),
            "texture" : 4,
            "randomTex" : True,
            "randomTexBounds" : (4,7),
            "spread" : (20,20),
            "lifespan" : random.randint(100,300) / self.game.TimeMult,
            "canFlip" : False
        }

        return particleArgs

    def pdefaultAdd(self,addArgs={}):
        particleArgs = {
            "UseVelocity" : True,
            "Acceleration" : pygame.Vector2(random.uniform(-4,4),random.uniform(-4,4)),
            "wind" : True,
            "texture" : 0,
            "randomTex" : True,
            "randomTexBounds" : (0,3),
            "spread" : (5,5),
            "lifespan" : random.randint(100,300) / self.game.TimeMult
        }

        if "useVelocity" in addArgs.keys():
            particleArgs["useVelocity"] = addArgs["useVelocity"]
        if "Acceleration" in addArgs.keys():
            particleArgs["Acceleration"] = addArgs["Acceleration"]
        if "wind" in addArgs.keys():
            particleArgs["wind"] = addArgs["wind"]
        if "texture" in addArgs.keys():
            particleArgs["texture"] = addArgs["texture"]
        if "randomTex" in addArgs.keys():
            particleArgs["randomTex"] = addArgs["randomTex"]
            if "randomTexBounds" in addArgs.keys():
                particleArgs["randomTexBounds"] = addArgs["randomTexBounds"]
        if "spread" in addArgs.keys():
            particleArgs["spread"] = addArgs["spread"]
        if "lifespan" in addArgs.keys():
            particleArgs["lifespan"] = addArgs["lifespan"]


        return particleArgs

    def pdefaultUpdate(self,particle):
        pArgs = particle[3]

        particle[1].x += pArgs["Acceleration"].x * self.game.dt
        particle[1].y += pArgs["Acceleration"].y * self.game.dt

        if particle[3]["wind"]:
            particle[1].x += self.windOffset.x * self.game.dt
            particle[1].y += self.windOffset.y * self.game.dt
    

    

    def pleafUpdate(self,particle):
        pArgs = particle[3]
        #get cached particle physics to apply
        if not "leaf" in self.particleCache.keys():
            particleCalculations = pygame.Vector2()
            
            if random.random() < 0.3:
                input = (pArgs["lifespan"] - particle[4]) / 100
                
                if input <= 2:
                    print("input val: " + str(input))
                    particleCalculations.x = (input/2) * (input/2)
                else:
                    particleCalculations.x = 1
                
                particleCalculations.y = random.uniform(-0.75,2)
                particleCalculations.x *= self.windOffset.x
            else:
                particleCalculations.y = self.windOffset.y
                particleCalculations.x = self.windOffset.x

            self.particleCache["leaf"] = particleCalculations

        particleCalculations = self.particleCache["leaf"]

        print("Accel: " + str(particleCalculations.x))

        #update particle position
        particle[1].x += (particleCalculations.x * self.game.dt * pArgs["randomOffset"][0])
        particle[1].y += (pArgs["Acceleration"].y * self.game.dt) + pArgs["randomOffset"][1] + (particleCalculations.y * self.game.dt) 
        

        if pArgs["canFlip"]:
            if random.randint(0,5) == 0:
                particle[0] = pygame.transform.flip(particle[0],True,False)
 

    def pwindUpdate(self):
        val = (self.game.tick%360)
        self.windAxis.x = math.sin( val / 50)
        self.windAxis.x = 1
        self.windPow.x = 100
        self.windOffset = pygame.Vector2(self.windPow * self.windAxis)

        if self.windOffset == 0:
            self.windOffset = pygame.Vector2(0,0)

