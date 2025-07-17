# from Platformer.platform import Platform
# import __init__
import os
import sys
import time
import pygame

# from Engine.Entity import Entity
from Engine.debug.View import SurfaceViewer
from Engine.util.vector import Vector2
from Platformer.entity.cable import Cable



from Engine import Program
from Platformer.entity.Player import Player
from Engine import Object
from Engine.tilemap import TileMapHandler
from Platformer.portal.portalHandler import PortalHandler

# from Engine import Entity

from Platformer.objects.platform import Platform

p = 14


def main():
    game = Program()
    game.setMap(TileMapHandler(game))
    pygame.display.set_caption("Platformer")

    portalHandler = PortalHandler(game)
    game.allObjects.add(portalHandler)

    player = Player(pygame.math.Vector2(50, 20))

    game.allSprites.add(player)
    game.PhysSprites.add(player)
    game.debugger.addTarget(player, game.debugGroup)
    game.camera.follow(player.position)

    test_cube = Object(
        pygame.math.Vector2(50, 20), "player", 0, {"angle": 0, "flip": False}
    )
    game.allObjects.add(test_cube)
    game.PhysSprites.add(test_cube)

    cable = Cable(Vector2(64, 32), 256, (255, 0, 0), 2)
    game.allObjects.add(cable)

    wallText = "wall"
    for n in range(p):
        wall = Object(pygame.math.Vector2(50 + (16 * n), 90), wallText, 0, {})
        # game.allSprites.add(wall)
        game.floorColliders.add(wall)

    wall2 = Object(pygame.math.Vector2(50, 74), wallText, 0, {})
    game.allSprites.add(wall2)
    game.floorColliders.add(wall2)

    # platform_test = Platform(64, 64, (255, 0, 0))
    # game.allObjects.add(platform_test)

    slope22 = Object(
        pygame.math.Vector2(98, 74), "wall", 0, {"angle": 22, "flip": True}
    )
    slope22.identifier = "object 22d"
    # game.allSprites.add(slope22)
    # game.floorColliders.add(slope22)
    gameTime = 1
    # viewer = SurfaceViewer()
    # viewer.show_surface(game.textures.texture("world/sheet", 0, [128, 128]))
    while game.running:
        game.update()
        game.draw()

        game.camera.y = 0


main()
