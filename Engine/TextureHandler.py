from functools import cache
from pathlib import Path
from typing import TypedDict
import pygame
from os import path

from Engine.debug.logger import Logger


class TextureHandler:
    _textureInstance = None

    def __new__(cls, *args, **kwargs):
        if not cls._textureInstance:
            cls._textureInstance = super(TextureHandler, cls).__new__(
                cls, *args, **kwargs
            )
            cls._initialized = False
        return cls._textureInstance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.texture_map: dict[str, tuple[pygame.Surface]] = {}
        self.sprite_cache: dict[str, dict[int, pygame.Surface]] = {}
        self.spritesheet = {}
        self.logger = Logger.get_logger("TextureHandler")

        self.blank = pygame.Surface((16, 16))
        self.blank.set_colorkey((0, 0, 0))

    def load_texture(self, filepath: str, sprite_size: tuple[int, int] = (16, 16)):
        originalFilepath = filepath
        filepath = "Resources/" + filepath + ".png"
        if not path.isfile(filepath):  # if file not found, return
            return False

        if str(filepath) in self.texture_map:
            return

        # load file
        texture = pygame.image.load(filepath).convert()
        texture.set_colorkey((0, 0, 0))

        self.texture_map[originalFilepath] = (texture, sprite_size)

    @cache
    def get_section(
        self,
        path: str,
        spritesheet: pygame.Surface,
        position: int,
        width: int,
        height: int,
    ) -> pygame.Surface:
        if path not in self.texture_map:
            self.logger.warning(
                f"Texture {path} not found in texture map. Returning blank texture."
            )
            return self.blank
        if path not in self.sprite_cache:
            self.sprite_cache[path] = {}

        cache_key = position + width + height
        if cache_key in self.sprite_cache.get(path, {}):
            return self.sprite_cache[path][cache_key]

        SprRow = spritesheet.get_width() / width
        topX = (position % SprRow) * width
        topY = (position // SprRow) * height

        rect = pygame.Rect(topX, topY, width, height)
        img = pygame.Surface(rect.size)
        img.blit(spritesheet, (0, 0), rect)
        img.set_colorkey((0, 0, 0))

        self.sprite_cache[path][cache_key] = img
        return img

    def texture(
        self, filepath: Path, pos: int, size: tuple[int, int] | None = None
    ) -> pygame.Surface:
        if not filepath in self.texture_map:
            self.logger.warning(
                f"Texture {filepath} not found in texture map. Returning blank texture."
            )
        try:
            spritesheet = self.texture_map[filepath][0]
            sprite_size = self.texture_map[filepath][1]
        except:
            spritesheet = self.blank
            sprite_size = [16, 16]

        if size is not None:
            sprite_size = size
            if sprite_size[0] == 0 or sprite_size[0] == 0:
                sprite_size[0] = 16
                sprite_size[1] = 16

            if sprite_size[0] > spritesheet.get_width():
                sprite_size[0] = spritesheet.get_width()
            if sprite_size[1] > spritesheet.get_height():
                sprite_size[1] = spritesheet.get_height()

        image = self.get_section(
            filepath, spritesheet, pos, sprite_size[0], sprite_size[1]
        )

        return image


sprite_cache: dict[str, dict[int, pygame.Surface]] = {}
