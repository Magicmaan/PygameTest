from typing import TypedDict


class Tile(TypedDict):
    id: int
    transparent: bool
    collision: bool
    portal_surface: bool
    properties: dict[str, str]
    x: int | None
    y: int | None

    @classmethod
    def from_dict(cls, data: dict) -> "Tile":
        return cls(
            id=data["id"],
            transparent=data.get("transparent", False),
            collision=data.get("collision", False),
            portal_surface=data.get("portal_surface", False),
            properties=data.get("properties", {}),
        )


class TileMapLayer(TypedDict):
    name: str
    # tile = tiles[x][y]
    tiles: dict[tuple[int, int], Tile]


class TileMap(TypedDict):
    """
    TileMap structure.
    tileSize: int
    mapWidth: int
    mapHeight: int
    layers: list[TileMapLayer]
    """

    tileSize: int
    mapWidth: int
    mapHeight: int
    layers: list[TileMapLayer]
