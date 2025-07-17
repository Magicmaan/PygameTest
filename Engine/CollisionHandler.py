from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Engine.Entity import Entity

import math
import pygame


from Engine.Program import Program
from Engine.tilemap import TileMapHandler
from Engine.util import Vector2

angleSurfaceHeights = {
    0: (0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5),  # 12 degree
    1: (0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7),  # 22 degree
    2: (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15),  # 45 degree
    3: (1, 3, 5, 7, 9, 11, 13, 15, 15, 15, 15, 15, 15, 15, 15, 15),  # 75 degree
}


def slopeResolve(spr: Entity, rect: pygame.rect.Rect, obj, slope):
    spr.collisions["down"] = True
    spr.onGround = True

    if spr.velocity.y >= 0:
        spr.velocity.y = 0

    leftCenter = obj.rect.collidepoint(Vector2(rect.centerx + 2, rect.centery))
    rightCenter = obj.rect.collidepoint(Vector2(rect.centerx - 2, rect.centery))
    if leftCenter and rightCenter:

        # get just subpixel of tile user is on
        digitConvert = (spr.position.x + spr.rect.width / 2) % 16

        spr.position.y = (
            obj.rect.bottom - slope[int(digitConvert)] - 1 - spr.rect.height
        )
    else:
        if spr.rect.left < obj.rect.left:
            spr.position.y = obj.rect.bottom - slope[0] - spr.rect.height
        elif spr.rect.right > obj.rect.right:
            spr.position.y = obj.rect.bottom - slope[-1] - spr.rect.height


def objectCollideResolve(spr: Entity, rect: pygame.rect.Rect, obj):
    colPoint = obj.rect.collidepoint
    isSlope = False
    if obj.angle == 12:
        slope = angleSurfaceHeights[0]
        isSlope = True
    elif obj.angle == 22:
        slope = angleSurfaceHeights[1]
        isSlope = True
    elif obj.angle == 45:
        slope = angleSurfaceHeights[2]
        isSlope = True
    if isSlope:
        if obj.flipX:
            slope = tuple(reversed(slope))
        slopeResolve(spr, rect, obj, slope)
        return

    collideResolve(spr, rect, obj.rect)


game = Program()


def collideResolve(spr, sprRect: pygame.rect.Rect, objRect: pygame.rect.Rect):

    clipLine = objRect.clipline

    # down collision
    if (
        clipLine(
            sprRect.left + 1,
            sprRect.bottom + 0.1,
            sprRect.right - 1,
            sprRect.bottom + 0.1,
        )
        and not spr.collisions["down"]
        and spr.use_collisions["down"]
    ):
        spr.collisions["down"] = True
        spr.onGround = True
        spr.position.y = objRect.top - spr.rect.height
        if spr.velocity.y > 0:
            spr.velocity.y = 0

    # up collision
    elif (
        clipLine(
            sprRect.left + 1, sprRect.top - 0.1, sprRect.right - 1, sprRect.top - 0.1
        )
        and spr.velocity.y < 0
        and spr.use_collisions["up"]
    ):
        spr.collisions["up"] = True
        spr.position.y = (
            objRect.bottom
        )  # Adjust the position to be exactly below the collider

        if spr.velocity.y < 0:
            spr.velocity.y = abs(spr.velocity.y)

    sprRect = spr.rect.copy()

    # Check horizontal collisions (left and right)
    if (
        clipLine(
            sprRect.left - 0.1, sprRect.top + 2, sprRect.left - 0.1, sprRect.bottom - 2
        )
        and spr.velocity.x < 0
        and spr.use_collisions["left"]
    ):

        if (sprRect.bottom - objRect.top) <= 8:
            spr.position.x -= 1
            spr.position.y = objRect.top - spr.rect.height
            spr.collisions["bottom"] = True
            spr.onGround = True
        else:
            spr.collisions["left"] = True
            spr.position.x = objRect.right
            spr.velocity.x = 0

    elif (
        clipLine(
            sprRect.right + 0.1,
            sprRect.top + 2,
            sprRect.right + 0.1,
            sprRect.bottom - 2,
        )
        and spr.velocity.x > 0
        and spr.use_collisions["right"]
    ):

        if (sprRect.bottom - objRect.top) <= 8:
            spr.position.x -= 1
            spr.position.y = objRect.top - spr.rect.height
            spr.collisions["bottom"] = True
            spr.onGround = True
        else:
            spr.collisions["right"] = True
            spr.position.x = objRect.left - spr.rect.width
            spr.velocity.x = 0

    sprRect = spr.rect.copy()


def collideTest(rect: pygame.rect.Rect, objs: pygame.sprite.Group):
    objectCollisions = []
    # rect is x,y,width,height
    # objs is list of objects (or groups)
    # colliderect tests for intersection between rect and each obj rect in group
    for obj in objs:
        r = obj.rect.inflate(2, 2)
        if r.colliderect(rect):
            objectCollisions.append(obj)

    return objectCollisions


def collideUpdate(spr: pygame.sprite.Sprite, collideGroup, tileMap: TileMapHandler):
    # Check for collisions between the two groups on next movement
    # collisions = pygame.sprite.groupcollide(self.game.PhysSprites, self.game.floorColliders, False, False)
    futureRect = spr.rect.copy()
    futureRect.update(
        spr.position.x + round(spr.velocity.x, 2),
        spr.position.y + round(spr.velocity.y, 2),
        spr.rect[2],
        spr.rect[3],
    )
    # get collisions

    objectCollisions = collideTest(futureRect, collideGroup)
    if objectCollisions:
        for obj in objectCollisions:
            collideResolve(spr, futureRect, obj.rect)

    tile_collisions = tileMap.get_collisions(futureRect)
    if tile_collisions:

        for tileRect in tile_collisions:
            collideResolve(spr, futureRect, tileRect)
