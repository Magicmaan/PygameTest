from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Engine.Program import Program
    from Engine.tilemap import TileMapHandler

from collections import namedtuple
from typing import List
import math
from Engine.util import Vector2


class Ray:
    """
    A class representing a ray in a raycaster.
    Each ray has an origin point, an angle, and a length.

    :param origin: The starting point of the ray (Vector2).
    :param angle: The angle of the ray in degrees (int).
    :param length: The length of the ray (int).
    """

    def __init__(
        self,
        origin: Vector2,
        length: int,
        tilemap: TileMapHandler = None,
        angle: int = None,
        to: Vector2 = None,
        lifespan: int = 1,
    ):
        assert isinstance(origin, Vector2), "Origin must be a Vector2 object."
        assert isinstance(length, int), "Length must be an integer."

        assert (
            angle is not None or to is not None
        ), "Either 'angle' or 'to' must be provided."

        if angle is None:
            angle = math.degrees(math.atan2(to.y - origin.y, to.x - origin.x))

        self.tilemap: TileMapHandler = tilemap
        self.origin = origin
        self.angle = angle
        self.to = to
        self.length = length
        self.lifespan = lifespan
        self.counter = 0
        self.collision = False
        self.collisionSide = None
        self.contactPoint = None

        self.lastOrigin = origin.copy()

    def collideCheckRough(self, tilemap) -> list[int, int] | None:
        """
        perform rough collision check with tilemap
        check if ray is within bounds of tilemap
        """
        endPos = self.origin + Vector2(
            self.length * math.cos(math.radians(self.angle)),
            self.length * math.sin(math.radians(self.angle)),
        )
        endPosTile = tilemap.getTileScreen(endPos)
        if endPosTile[0] < 0 or endPosTile[1] < 0:
            return None

        tile = tilemap.getTile(endPosTile[0], endPosTile[1])
        if tile is None or tile == 0:
            return None

        return tile

    def update(self):

        if (self.origin - self.lastOrigin).length() > 1:
            self.lastOrigin = self.origin.copy()
            self.length = 0
            self.collision = False
        collisionSide = None
        contactPoint = None
        while not self.collision:
            self.counter += 1

            endPos = self.origin + Vector2(
                self.length * math.cos(math.radians(self.angle)),
                self.length * math.sin(math.radians(self.angle)),
            )

            tilePosition = self.tilemap.getTileScreen(endPos)
            if tilePosition[0] < 0 or tilePosition[1] < 0:
                return

            tile = self.tilemap.get_tile(tilePosition[0], tilePosition[1])

            if tile is None or tile == 0:
                # if no obstruction, increase length by 4
                self.length += 1
            else:
                # gets closest length to tile face and sets length to that
                tileWorldPos = [
                    tilePosition[0] * self.tilemap.tileSize,
                    tilePosition[1] * self.tilemap.tileSize,
                ]

                # Calculate the exact collision point
                blockEdges = {
                    "left": tileWorldPos[0],
                    "right": tileWorldPos[0] + self.tilemap.tileSize,
                    "top": tileWorldPos[1],
                    "bottom": tileWorldPos[1] + self.tilemap.tileSize,
                }

                # Determine which edge the ray intersects
                rayDirection = Vector2(
                    math.cos(math.radians(self.angle)),
                    math.sin(math.radians(self.angle)),
                )
                contactPoint = None

                if abs(rayDirection.x) > 0:  # Check vertical edges
                    if rayDirection.x > 0:  # Intersect with left edge
                        x = blockEdges["left"]
                        collisionSide = "left"
                    else:  # Intersect with right edge
                        x = blockEdges["right"]
                        collisionSide = "right"
                    if rayDirection.x != 0:  # Avoid division by zero
                        y = (
                            self.origin.y
                            + (x - self.origin.x) * rayDirection.y / rayDirection.x
                        )
                        if blockEdges["top"] <= y <= blockEdges["bottom"]:
                            contactPoint = Vector2(x, y)

                if (
                    abs(rayDirection.y) > 0 and contactPoint is None
                ):  # Check horizontal edges
                    if rayDirection.y > 0:  # Intersect with top edge
                        y = blockEdges["top"]
                        collisionSide = "top"
                    else:  # Intersect with bottom edge
                        y = blockEdges["bottom"]
                        collisionSide = "bottom"
                    if rayDirection.y != 0:  # Avoid division by zero
                        x = (
                            self.origin.x
                            + (y - self.origin.y) * rayDirection.x / rayDirection.y
                        )
                        if blockEdges["left"] <= x <= blockEdges["right"]:
                            contactPoint = Vector2(x, y)

                if contactPoint:
                    contactPoint = Vector2(
                        math.floor(contactPoint.x),
                        math.floor(contactPoint.y),
                    )
                    exactDistance = (contactPoint - self.origin).length()
                    self.length = exactDistance
                    self.collision = True

            if self.length > 500:
                self.collision = False
                break

        # print("collisionSide", collisionSide)
        self.collisionSide = collisionSide
        self.contactPoint = contactPoint

    def __repr__(self):
        return f"Ray(origin={self.origin}, angle={self.angle}, length={self.length})"


class Raycaster:
    def __init__(self, program):
        self.program = program
        self.rayLength = 10
        self.rayCount = 10
        self.rays: List[Ray] = []
        self.angle = 0

        # print("tilemap", self.program.tilemap)

    def addRay(
        self,
        origin: Vector2,
        length: int,
        angle: int = None,
        to: Vector2 = None,
        lifespan: int = 1,
    ) -> Ray:
        """
        Adds a new ray to the raycaster.

        :param origin: The starting point of the ray (Vector2).
        :param angle: The angle of the ray in degrees (int).
        :param length: The length of the ray (int).
        """

        assert isinstance(origin, Vector2), "Origin must be a Vector2 object."
        assert isinstance(length, int), "Length must be an integer."
        assert length > 0, "Length must be greater than 0."
        assert (
            angle is not None or to is not None
        ), "Either 'angle' or 'to' must be provided."

        ray = Ray(origin, length, self.program.tilemap, angle, to, lifespan)
        ray.update()
        self.rays.append(ray)

        return ray

    def update(self):
        """
        Updates the rays in the raycaster. This method should be called every frame.
        """
        for ray in self.rays:
            if ray.counter >= ray.lifespan:
                self.rays.remove(ray)
                continue
            ray.update()

        pass
