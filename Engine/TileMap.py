import pygame
from Engine import TextGUI
import random



class TileMap:
    def __init__(self, game, tileSize = 16, offset = pygame.Vector2(0,0)):
        self.tileSize = tileSize
        self.offset = offset
        self.tilemap = [
            [1,0],
            [1,0],
            [1,1,1,1,3],
            [1,0],
            [1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        self.texturemap = {
            0 : game.textures.blank,
            1 : game.textures.texture("wall",0),

            2 : game.textures.texture("wall",1),
            3 : game.textures.texture("wall",2),
            4 : pygame.transform.flip(game.textures.texture("wall",2),True,False),
        }

        #tell tilemap to draw these around main tile
        #top, bottom, left, right
        self.toConnectTiles = {
            1 : (2, 0, 4, 3)
        }

        self.transparentTiles = {
            0 : True,
            2 : True,
            3 : True,
            4 : True,
        }

        
        self.directions = [
            (-1,-1),( 0,-1),( 1,-1),
            (-1, 0)        ,( 1, 0),
            (-1, 1),( 0, 1),( 1, 1)
        ]

        self.game = game

        self.randomSeed = random.random()
        self.renderview = pygame.Rect(0,0,20,20)
    

    def getTileScreen(self,x,y):
        #get tile at screen position location
        #i.e.
        #x,y = 50,50 on screen coords
        #x,y = x,y % tileSize + camera 
        #return getTile(x,y)
        pass

    def getTile(self,x,y):
        #get tile at exact location in tilemap
        #print(str(y) + " " + str(x))


        tile = 0
        if y < 0 or x < 0:
             return tile

        if y <= len(self.tilemap)-1:
            if x <= len(self.tilemap[y])-1:
                
                tile = self.tilemap[y][x]

        return tile


    def getTileAround(self,rect,range=1):
        #centre of sprite
        spritePos = [rect.centerx , rect.centery]
        #convert to tile grid
        onGridPos = [spritePos[0] // self.tileSize , spritePos[1] // self.tileSize]

        #print("player pos: " + str(onGridPos))
        tilesAround = []
        #for direction vectors around player pos
        for dx,dy in self.directions:
            #get new grid position
            newGridPos = [onGridPos[0] + dx , onGridPos[1] + dy]
            
            #transparent tile check
            if not self.getTile(newGridPos[0],newGridPos[1]) in self.transparentTiles:
                #if self.tilemap[newGridPos[1]][newGridPos[0]] != 0: #if not air
                newSpritePos = [newGridPos[0] * self.tileSize , newGridPos[1] * self.tileSize]

                rect = pygame.Rect(newSpritePos[0], newSpritePos[1], 16, 16)
                tilesAround.append(rect)
        

        return tilesAround
        #return list of tiles around rect sprite
        

    def draw(self,surface):

        #limit tilemap render view to within camera x range
        self.renderview.x = int(-self.game.camera.x // self.tileSize)
        if self.renderview.x < 0: self.renderview.x = 0
        self.renderview.width = int((-self.game.camera.x + surface.get_width()) // self.tileSize)+1
        
        #limit tilemap render view to within camera y range
        self.renderview.y = int(-self.game.camera.y // self.tileSize)
        if self.renderview.y < 0: self.renderview.y = 0
        self.renderview.height = int((-self.game.camera.y + surface.get_height()) // self.tileSize)+1

        #print(str(self.renderview.x) + " " + str(self.renderview.width) + "  " + str(self.renderview.y) + " " + str(self.renderview.height))
        for y in range(self.renderview.y,self.renderview.height):
            if y > len(self.tilemap)-1:
                break

            for x in range(self.renderview.x,self.renderview.width):
                if x > len(self.tilemap[y])-1:
                    break

                if self.tilemap[y][x] in self.texturemap and not self.tilemap[y][x] in self.transparentTiles:
                    tileImg = self.texturemap[self.tilemap[y][x]]
                else:
                    tileImg = False

                if tileImg:
                    surface.blit(tileImg, ((x*self.tileSize) + int(self.game.camera.x) + int(self.offset.x),(y*self.tileSize) + int(self.game.camera.y) + int(self.offset.y)))

                    #tilemap connect around logic
                    #if in toConnectTiles, will place the connector tiles above,below,left,right
                    if self.tilemap[y][x] in self.toConnectTiles:
                        if self.getTile(x,y-1) in self.transparentTiles:
                            surface.blit(self.texturemap[self.toConnectTiles[self.tilemap[y][x]][0]], ((x*self.tileSize) + int(self.game.camera.x),((y-1)*self.tileSize) + int(self.game.camera.y)))
                        if self.getTile(x,y+1) in self.transparentTiles:
                            surface.blit(self.texturemap[self.toConnectTiles[self.tilemap[y][x]][1]], ((x+1*self.tileSize) + int(self.game.camera.x),((y)*self.tileSize) + int(self.game.camera.y)))
                        if self.getTile(x+1,y) in self.transparentTiles:
                            surface.blit(self.texturemap[self.toConnectTiles[self.tilemap[y][x]][3]], ((x+1*self.tileSize) + int(self.game.camera.x),((y)*self.tileSize) + int(self.game.camera.y)))
                        if self.getTile(x-1,y) in self.transparentTiles:
                            surface.blit(self.texturemap[self.toConnectTiles[self.tilemap[y][x]][2]], ((x-1*self.tileSize) + int(self.game.camera.x),((y)*self.tileSize) + int(self.game.camera.y)))

                        if random.random() < 0.01 and self.getTile(x,y-1) in self.transparentTiles:
                            particleArgs = {
                                "UseVelocity" : True,
                                "Acceleration" : pygame.Vector2(random.uniform(-8,8),random.uniform(-10,-50)),
                                "texture" : 6,
                                "wind" : False,
                                "randomTex" : True,
                                "randomTexBounds" : (5,6,6,7,7),
                                "spread" : (10,0),
                                "lifespan" : random.randint(25,100)  / self.game.TimeMult 
                            }

                            self.game.particles.add(pygame.Vector2(x*self.tileSize,y*self.tileSize),"default",count=1,addArgs=particleArgs)
                    
        