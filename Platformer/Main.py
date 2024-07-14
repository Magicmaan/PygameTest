import __init__
import pygame
from Engine import Program
from Player import Player
from Engine import Object
from Engine.TileMap import TileMap

platform = 14    

def main():
    game = Program()
    game.setMap(TileMap())
    pygame.display.set_caption('Platformer')
    
    
    player = Player(pygame.math.Vector2(50,20))   
    game.allSprites.add(player)
    game.PhysSprites.add(player)
    game.debugger.addTarget(player,game.debugGroup)
    
    wallText = "wall"
    for n in range(platform):
        wall = Object(pygame.math.Vector2(50+(16*n),90),wallText,0,{})
        #game.allSprites.add(wall)
        #game.floorColliders.add(wall)
    
    wall2 = Object(pygame.math.Vector2(50,74),wallText,0,{})
    game.allSprites.add(wall2)
    game.floorColliders.add(wall2)

    slope22 = Object(pygame.math.Vector2(98,74),"wall",0,{"angle" : 22, "flip" : True})
    slope22.identifier = "object 22d"
    #game.allSprites.add(slope22)
    #game.floorColliders.add(slope22)
    gameTime = 1
    
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()
                return
        

        game.update()
        game.draw()
        
        

        game.camera = game.camera.smoothstep( pygame.math.Vector2(-player.position.x + game.screen.get_width()/2,game.camera.y) ,0.15)
        game.camera.y = 0
        game.dt = (game.clock.tick(game.framerate) / 1000) * game.TimeMult  

       
        
        
        game.tick=game.tick+1
        
    
    

main()      