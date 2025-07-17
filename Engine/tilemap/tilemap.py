from __future__ import annotations
from pathlib import Path
import pygame

import random
import json
from pprint import pprint
from typing import TYPE_CHECKING, TypedDict

from Engine.types import TileMap, TileMapLayer, Tile
from Engine.util.vector import Vector2, tupleToVector

if TYPE_CHECKING:
    from Engine import Program


temp = {
    "tileSize": 16,
    "mapWidth": 13,
    "mapHeight": 4,
    "layers": [
        {
            "name": "Layer_0",
            "tiles": [
                {"id": "0", "x": 0, "y": 1},
                {"id": "0", "x": 0, "y": 2},
                {"id": "0", "x": 0, "y": 3},
                {"id": "0", "x": 4, "y": 3},
                {"id": "0", "x": 0, "y": 4},
                {"id": "0", "x": 1, "y": 4},
                {"id": "0", "x": 2, "y": 4},
                {"id": "0", "x": 3, "y": 4},
                {"id": "0", "x": 4, "y": 4},
                {"id": "0", "x": 5, "y": 4},
                {"id": "0", "x": 6, "y": 4},
                {"id": "0", "x": 7, "y": 4},
                {"id": "0", "x": 8, "y": 4},
                {"id": "0", "x": 9, "y": 4},
                {"id": "0", "x": 10, "y": 4},
                {"id": "0", "x": 11, "y": 4},
                {"id": "0", "x": 12, "y": 4},
            ],
            "collider": False,
        }
    ],
}


def load_tilemap(path: Path) -> TileMap:
    tilemap = None
    with open(path) as json_data:
        tilemap = json.load(json_data)
        json_data.close()

    if tilemap is None:
        raise FileNotFoundError(f"Tilemap {path} not found.")

    old_layers = tilemap["layers"]
    new_layer: TileMapLayer = {
        "name": "Layer_0",
        "tiles": {},
    }
    for layer in old_layers:
        tiles = layer["tiles"]

        for t in tiles:
            print(t)
            x = int(t["x"])
            y = int(t["y"])

            tile_object: Tile = {
                "id": int(t["id"]),
                "transparent": False,
                "collision": True,
                "portal_surface": False,
                "properties": {},
                "x": x,
                "y": y,
            }
            new_layer["tiles"][x, y] = tile_object

        print(new_layer["tiles"])

    new_tilemap: TileMap = {
        "tileSize": tilemap["tileSize"],
        "mapWidth": tilemap["mapWidth"],
        "mapHeight": tilemap["mapHeight"],
        "layers": [new_layer],
    }

    return new_tilemap


DEFAULT_TILEMAP = load_tilemap(
    Path.cwd() / "Resources/world/map.json"
)


class TileMapHandler:
    def __init__(self, game: Program, tileSize=16, offset=pygame.Vector2(0, 0)):
        self.offset = offset
        self.game: Program = game
        self.game.textures.load_texture("world/sheet", (16, 16))
        self.texturemap: dict[int, pygame.Surface] = {
            0: self.game.textures.texture("world/sheet", 1),
            1: self.game.textures.texture("world/sheet", 2),
            2: self.game.textures.texture("world/sheet", 3),
            3: self.game.textures.texture("world/sheet", 4),
            4: self.game.textures.texture("world/sheet", 5),
            5: self.game.textures.texture("world/sheet", 6),
        }

        self._tilemap: TileMap = DEFAULT_TILEMAP

        # tell tilemap to draw these around main tile
        # top, bottom, left, right
        # self.toConnectTiles = {1: (2, 0, 4, 3)}
        self.toConnectTiles = {}

        self.transparentTiles = {0: True}

        self.randomSeed = random.random()
        self.view_rect = pygame.Rect(0, 0, 20, 20)

        self.surface = None

    def load_tilemap(self, tilemap: TileMap):
        self._tilemap = tilemap

    def getTileScreen(self, position: Vector2) -> Vector2:
        """
        Get the tile position on the grid based on the game position.

        Args:
                position (pygame.Vector2): The game position of the tile.

        Returns:
                pygame.Vector2: The tile position on the grid.
        """
        return position.copy() // self.tileSize

    def get_tile(self, x, y) -> Tile | None:
        # get tile at exact location in tilemap
        tiles = self._tilemap["layers"][0]["tiles"]
        # go through all tiles in the tilemap and find the one at x, y
        tile = tiles.get((x, y), None)
        return tile

    def get_collisions(self, rect: pygame.Rect) -> list[pygame.Rect]:
        """
        Get the collisions of a rectangle with the tilemap.

        Args:
            rect (pygame.Rect): The rectangle to check for collisions.

        Returns:
            list[pygame.Rect]: A list of rectangles representing the collisions.
        """
        tiles_around = self.get_tiles_around(rect=rect, r=1)
        collisions = []

        collision_tiles = [tile for tile in tiles_around if tile["collision"]]

        for tile in collision_tiles:
            tile_rect = self.get_tile_rect(tile["x"], tile["y"])
            collisions.append(tile_rect)

            self.game.debugger.add_rect(tile_rect)

        return collisions

    def get_tile_rect(self, x, y) -> pygame.Rect:
        """
        Get the rectangle of a tile at a given position.

        Args:
            x (int): The x position of the tile.
            y (int): The y position of the tile.

        Returns:
            pygame.Rect: The rectangle of the tile.
        """
        return pygame.Rect(
            x * self.tileSize + self.offset.x,
            y * self.tileSize + self.offset.y,
            self.tileSize,
            self.tileSize,
        )

    def get_tiles_around(
        self, rect: pygame.Rect = None, position: pygame.Vector2 = None, r=1
    ) -> list[Tile]:
        """
        Get the tiles around a given rectangle or position within a specified range.

        Args:
            rect (pygame.Rect, optional): The rectangle to check around.
            position (pygame.Vector2, optional): The position to check around.
            range (int, optional): The range of tiles to check around. Defaults to 1.

        Returns:
            list[pygame.Rect]: A list of rectangles representing the tiles around the given rectangle or position.
        """
        assert rect or position, "Either 'rect' or 'position' must be provided."

        # Determine the centre position on the grid
        if rect:
            centre_pos = self.getTileScreen(tupleToVector(rect.center))
        else:
            centre_pos = self.getTileScreen(position)

        tiles_around = []

        # Iterate through the range around the centre position
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx == 0 and dy == 0:
                    continue  # Skip the centre tile

                grid_pos = (centre_pos[0] + dx, centre_pos[1] + dy)

                tile = self.get_tile(grid_pos[0], grid_pos[1])
                if tile is None:
                    continue

                tiles_around.append(tile)

        return tiles_around

    def draw(self, surface: pygame.Surface):
        self.view_rect.update(
            -self.game.camera.x // self._tilemap["tileSize"],
            self.game.camera.y // self._tilemap["tileSize"],
            20,
            20,
        )
        if self.view_rect.x < 0:
            self.view_rect.x = 0
        if self.view_rect.y < 0:
            self.view_rect.y = 0

        if not self.surface:
            self.surface = pygame.Surface(
                (surface.get_width(), surface.get_height()), pygame.SRCALPHA
            )
            self.surface.fill((0, 255, 0, 0))
            self.surface.set_colorkey((0, 0, 0, 0))

            tiles = self._tilemap["layers"][0]["tiles"]
            for x, y in tiles.keys():
                tile = tiles[(x, y)]
                # check if tile exists in the tilemap
                if int(tile["id"]) in self.texturemap.keys():
                    tile_image = self.texturemap[int(tile["id"])]

                    self.surface.blit(
                        tile_image,
                        ((x * self.tileSize), (y * self.tileSize)),
                    )

        surface.blit(
            self.surface,
            (
                int(self.game.camera.position.x) + int(self.offset.x),
                int(self.game.camera.position.y) + int(self.offset.y),
            ),
        )

    @property
    def width(self):
        return self._tilemap["mapWidth"]

    @property
    def height(self):
        return self._tilemap["mapHeight"]

    @property
    def tileSize(self):
        return self._tilemap["tileSize"]

    @property
    def tilemap(self):
        return self._tilemap["layers"][0]["tiles"]
