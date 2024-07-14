import __init__
import pygame
import random
import math
from Engine import Program
from Engine import Object

colours = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

figures = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
    ]

class Tetro:
    def __init__(self,position):
        self.position = position
        self.type = random.randint(0, len(figures) - 1)
        self.rotation = 0
    

    

def update(self):
    
    print("buh")
    self.allObjects.update()
    self.allSprites.update()

    self.GUI.update(self)

def main():
    game = Program()
    setattr(game,'update',update)
    pygame.display.set_caption('Tetris')
    

    gameTime = 1
    
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()
                return
        

        game.update()
        game.draw()
        
        

        game.camera = pygame.math.Vector2(0,0)
        game.camera.y = 0
        game.dt = (game.clock.tick(game.framerate) / 1000) * game.TimeMult  

       
        
        
        game.tick=game.tick+1
        
    
    

main()      