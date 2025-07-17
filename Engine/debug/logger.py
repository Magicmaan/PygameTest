from __future__ import annotations
from typing import TYPE_CHECKING

from Engine.util.vector import Vector2, tupleToVector

if TYPE_CHECKING:
    from Engine import Program
    from Engine.Entity import Entity
    from Engine.tilemap import TileMapHandler

import logging
import pygame

# from Engine.debug.Debugger import Debugger

# from Engine.Program import Program

# game = Program()


def debugRect(func):
    def wrapper(*args: list[Entity, pygame.Surface], **kwargs):
        result = func(*args, **kwargs)
        # surface = args[1]  # Assuming the second argument is the surface to draw on
        entity: Entity = args[0]  # Assuming the first argument is 'self'

        # print("Debugging function called:", func.__name__)
        # print("Arguments:", surface, rect)
        entity.game.debugger.add_rect(entity.rect)  # Add the rect to the debugger
        return result

    return wrapper


def debugCollision(func):
    """
    Decorator to debug collisions by drawing lines on the screen.
    red: is colliding
    grey: has no collisions
    """

    def wrapper(*args: list[Entity, pygame.Surface], **kwargs):
        result = func(*args, **kwargs)
        # surface = args[1]  # Assuming the second argument is the surface to draw on
        entity: Entity = args[0]  # Assuming the first argument is 'self'

        rect: pygame.Rect = entity.rect  # Assuming the first argument is 'self'
        if not isinstance(rect, pygame.Rect):
            return result

        surface: pygame.Surface = entity.game.renderer.surface
        if not isinstance(surface, pygame.Surface):
            raise ValueError("Invalid surface type.")
        debugger = entity.game.debugger

        debugger.add_rect(entity.rect)

        closest_tile = entity.game.tilemap.getTileScreen(
            tupleToVector(entity.rect.topleft)
        )

        debugger.add_rect(
            pygame.Rect(
                closest_tile.x * entity.game.tilemap.tileSize,
                closest_tile.y * entity.game.tilemap.tileSize,
                entity.game.tilemap.tileSize,
                entity.game.tilemap.tileSize,
            ),
        )

        # draw sides with no collisions
        not entity.use_collisions["left"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topleft),
                tupleToVector(entity.rect.bottomleft),
                (50, 50, 50),
            ]
        )

        not entity.use_collisions["right"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topright),
                tupleToVector(entity.rect.bottomright),
                (50, 50, 50),
            ]
        )

        not entity.use_collisions["up"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topleft),
                tupleToVector(entity.rect.topright),
                (50, 50, 50),
            ]
        )
        not entity.use_collisions["down"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.bottomleft),
                tupleToVector(entity.rect.bottomright),
                (50, 50, 50),
            ]
        )

        # draw collision lines
        entity.collisions["left"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topleft),
                tupleToVector(entity.rect.bottomleft),
            ]
        )

        entity.collisions["right"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topright),
                tupleToVector(entity.rect.bottomright),
            ]
        )

        entity.collisions["up"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.topleft),
                tupleToVector(entity.rect.topright),
            ]
        )

        entity.collisions["down"] and debugger.add_debug_line(
            [
                tupleToVector(entity.rect.bottomleft),
                tupleToVector(entity.rect.bottomright),
            ]
        )
        return result

    return wrapper


class Logger(logging.Logger):
    def __init__(self, name: str, level: int = logging.DEBUG) -> None:
        super().__init__(name, level)
        self.setLevel(level)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        self.addHandler(ch)

    @classmethod
    def get_logger(cls, name: str) -> "Logger":
        """
        Get a logger instance with the specified name.
        """
        if name in logging.Logger.manager.loggerDict:
            return logging.getLogger(name)
        return cls(name)
