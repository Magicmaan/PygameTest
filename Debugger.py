import pygame
import TextGUI
from pprint import pprint
from InputHandler import InputHandler


gInput = InputHandler()

class Debugger:
    def __init__(self,gameObject,surface,enableDebug = False,enableFPS = True,enableObjectDebug = False):
        self.game = gameObject
        self.surface = surface
        self.lineoffset = 4
        
        self.enableDebug = enableDebug
        self.enableFPS = enableFPS
        self.enableObjectDebug = enableObjectDebug
        self.showcollisions = True
        self.tileGrid = True

        self.toggleTimer = 0
        
        self.identifier = "debugger"
    
    def printFPS(self,clock):
        TextGUI.write(str(round(clock.get_fps(),1)),
                     self.surface,[0, 
                                   0])
        
        TextGUI.write(str(self.game.dt * 1000),
                     self.surface,[0, 
                                   20])
    
    
    def addTarget(self,target,debugGroup):
        debugGroup.add(target)
    
    def removeTarget(self,target,debugGroup):
        debugGroup.remove(target)
    
    
    def draw(self):
        if gInput.L_CTRL():
            self.enableDebug = not self.enableDebug
            self.toggleTimer = 20

        if self.toggleTimer > 0:
            self.toggleTimer -= 1

        if not self.enableDebug:
            return
        
        if self.enableObjectDebug:
            self.printObjects(self.game.Outputresolution,self.game.resolution,self.game.debugGroup)
        
        if self.enableFPS:
            self.printFPS(self.game.clock)

        if self.tileGrid:
            self.printTileGrid(self.game.Outputresolution,self.game.resolution,self.game.tileMap)

        
    def printTileGrid(self,outputRes,nativeRes,tileMap):
        xMult = outputRes[0] / nativeRes[0]
        yMult = outputRes[1] / nativeRes[1]

        offsetX = int(self.game.camera.x % 16) * xMult
        offsetY = int(self.game.camera.y % 16) * yMult
        for x in range(0,20):
            pygame.draw.line(self.surface,"red",((x *tileMap.tileSize  *xMult) +offsetX,0),((x *tileMap.tileSize  *xMult) +offsetX,2000))
        for y in range(0,20):
            pygame.draw.line(self.surface,"red",(0,(y *tileMap.tileSize  *yMult) +offsetY),(2000,(y *tileMap.tileSize  *yMult) +offsetY))
    
    def printObjects(self,outputRes,nativeRes,debugGroup):
        
        xMult = outputRes[0] / nativeRes[0]
        yMult = outputRes[1] / nativeRes[1]
        
        for obj in debugGroup.sprites():
            posX = obj.position.x
            posY = obj.position.y
            if obj.position.y < 0:
                posY = 0
            elif obj.position.y+obj.rect.height > self.game.screen.get_height():
                posY = self.game.screen.get_height() - obj.rect.height

            if obj.position.x < 0:
                posX = 0
            elif obj.position.x+obj.rect.width > self.game.screen.get_width():
                posX = self.game.screen.get_width() - 16

            #add camera offset
            posX += self.game.camera.x
            posY += self.game.camera.y

            TextGUI.write(obj.identifier,
                         self.surface,[posX  * xMult, 
                         (posY + obj.rect.height) * yMult])
            n=0
            l = 4
            TextGUI.write("X:" + str(round(obj.position.x,2)) + " V:" + str(round(obj.velocity.x,2)),
                         self.surface,[(posX + obj.rect.width)  * xMult, 
                         (posY + n*l) * yMult])
            n=n+1
            TextGUI.write("Y:" + str(round(obj.position.y,2)) + " V:" + str(round(obj.velocity.y,2)),
                         self.surface,[(posX + obj.rect.width)  * xMult, 
                         (posY + n*l) * yMult])
            n=n+2
            TextGUI.write("Anim:" + str(obj.AnimationSlides[obj.state][obj.animationPos]),
                         self.surface,[(posX + obj.rect.width)  * xMult, 
                         (posY + n*l) * yMult])

            pygame.draw.rect(self.surface, (0,255,0), (obj.rect.left*xMult + (self.game.camera.x * xMult),obj.rect.top*yMult + (self.game.camera.y * xMult),obj.rect.width*xMult,obj.rect.height*yMult), 1)
            
            (self.game.camera.y * xMult)
            if self.showcollisions:
                if obj.collisions["up"]:
                    pygame.draw.rect(self.surface, (255,0,0), (obj.rect.left*xMult + (self.game.camera.x * xMult), obj.rect.top*yMult + (self.game.camera.y * xMult), obj.rect.width*xMult, 2*yMult))
                if obj.collisions["down"]:
                    pygame.draw.rect(self.surface, (255,0,0), (obj.rect.left*xMult + (self.game.camera.x * xMult), (obj.rect.bottom-2)*yMult + (self.game.camera.y * xMult), obj.rect.width*xMult, 2*yMult))
                if obj.collisions["left"]:
                    pygame.draw.rect(self.surface, (255,0,0), (obj.rect.left*xMult + (self.game.camera.x * xMult), obj.rect.top*yMult + (self.game.camera.y * xMult), 2*xMult, obj.rect.height*yMult))
                if obj.collisions["right"]:
                    pygame.draw.rect(self.surface, (255,0,0), ((obj.rect.right-2)*xMult + (self.game.camera.x * xMult), obj.rect.top*yMult + (self.game.camera.y * xMult), 2*xMult, obj.rect.height*yMult))
                
            
    
    
    