import pygame
import TextGUI

class TileMap:
    def __init__(self,game, tileSize = 16):
        self.tileSize = tileSize
        self.tilemap = [
            [1],
            [1],
            [1,1,1,1],
            [1],
            [1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        self.texturemap = {
            0 : False,
            1 : pygame.image.load("resources/wall.png").convert()
        }
        self.directions = [
            (-1,-1),( 0,-1),( 1,-1),
            (-1, 0)        ,( 1, 0),
            (-1, 1),( 0, 1),( 1, 1)
        ]

        self.game = game

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
            

            if self.getTile(newGridPos[0],newGridPos[1]) != 0:
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
                if self.tilemap[y][x] in self.texturemap:
                    tileImg = self.texturemap[self.tilemap[y][x]]
                
                if tileImg:
                    surface.blit(tileImg, ((x*self.tileSize) + int(self.game.camera.x),(y*self.tileSize) + int(self.game.camera.y)))
                    TextGUI.write((str(x) + " " + str(y)),surface,[(x*self.tileSize) + int(self.game.camera.x),(y*self.tileSize) + int(self.game.camera.y)])
        