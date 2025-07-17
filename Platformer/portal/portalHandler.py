from __future__ import annotations
from typing import TYPE_CHECKING
import math


from Platformer.portal.clone import EntityClone

if TYPE_CHECKING:
    from Engine.Program import Program
    from Engine.Entity import Entity

import pygame
from Platformer.portal.Portal import Portal


class PortalHandler(pygame.sprite.Sprite):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PortalHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, game: Program):
        if not hasattr(self, "initialised"):
            super().__init__()
            self.game = game
            self.identifier = "portalHandler"

            self.orangePortal = Portal(
                pygame.math.Vector2(0, 0),
                "portal",
                {"angle": 0, "flip": False, "identifier": "orange"},
            )
            self.bluePortal = Portal(
                pygame.math.Vector2(0, 0),
                "portal_2",
                {"angle": 0, "flip": False, "identifier": "blue"},
            )
            self.portals = [self.orangePortal, self.bluePortal]

            game.debugGroup.add(self.orangePortal)
            game.debugGroup.add(self.bluePortal)
            self.initialised = True

            self.ghost: EntityClone = EntityClone(
                anchor=self.orangePortal.position,
                identifier="orange",
                link=self.orangePortal,
            )
            self.ghost2: EntityClone = EntityClone(
                anchor=self.bluePortal.position, identifier="blue", link=self.bluePortal
            )

            # self.game.allSprites.add(self.ghost)
            # self.game.allSprites.add(self.ghost2)

    def checkPosition(self, position: pygame.Vector2, side: str = "right"):
        """
        Validates the position for placing a portal based on the surrounding tiles.
        Adjusts the position to ensure the portal is not floating, out of bounds, or obstructed.

        Args:
            position (pygame.Vector2): The position to check.
            side (str): The side where the portal is being placed ("left", "right", "top", "bottom").
        """

        # Adjust position based on the side
        if side == "left":
            position.x -= self.game.tileMap.tileSize
        elif side == "top":
            position.y -= self.game.tileMap.tileSize

        tilemap = self.game.tilemap
        tile = tilemap.getTileScreen(position)

        # Define neighbouring tiles
        px = [tile[0] + 1, tile[1]]  # +x
        mx = [tile[0] - 1, tile[1]]  # -x
        pxmy = [tile[0] + 1, tile[1] - 1]  # +x -y
        mxmy = [tile[0] - 1, tile[1] - 1]  # -x -y
        my = [tile[0], tile[1] - 1]  # -y
        py = [tile[0], tile[1] + 1]  # +y
        mxpy = [tile[0] - 1, tile[1] + 1]  # -x +y
        pxpy = [tile[0] + 1, tile[1] + 1]  # +x +y

        # Get tile values for neighbouring tiles
        pxTile = tilemap.get_tile(*px)
        mxTile = tilemap.get_tile(*mx)
        pxmyTile = tilemap.get_tile(*pxmy)
        mxmyTile = tilemap.get_tile(*mxmy)
        myTile = tilemap.get_tile(*my)
        pyTile = tilemap.get_tile(*py)
        mxpyTile = tilemap.get_tile(*mxpy)
        pxpyTile = tilemap.get_tile(*pxpy)

        # Adjust position for vertical walls (left/right sides)
        if side in ["left", "right"]:
            if pyTile != 0:  # Check above
                position.y = min(
                    position.y, (py[1] * tilemap.tileSize) - (tilemap.tileSize / 2)
                )
                # print("Adjusted position above side")
            if myTile != 0:  # Check below
                position.y = max(
                    position.y, (my[1] * tilemap.tileSize) + (tilemap.tileSize * 1.5)
                )
                # print("Adjusted position below side")

        # Adjust position for horizontal walls (top/bottom sides)
        if side in ["top", "bottom"]:
            if mxTile != 0:  # Check left
                position.x = max(
                    position.x, (mx[0] * tilemap.tileSize) + (tilemap.tileSize / 2)
                )
                # print("Adjusted position left side")
            if pxTile != 0:  # Check right
                position.x = min(
                    position.x, (px[0] * tilemap.tileSize) - (tilemap.tileSize / 2)
                )
                # print("Adjusted position right side")

        # Additional adjustments for bottom side
        if side == "bottom":
            if pxmyTile == 0:  # Top-right empty
                position.x = min(
                    position.x, (px[0] * tilemap.tileSize) - (tilemap.tileSize)
                )
                # print("Snapped to right edge")
            if mxmyTile == 0:  # Top-left empty
                position.x = max(
                    position.x, (mx[0] * tilemap.tileSize) + (tilemap.tileSize * 1.5)
                )
                # print("Snapped to left edge")

        # Additional adjustments for top side
        if side == "top":
            if pxpyTile == 0:  # Bottom-right empty
                position.x = min(
                    position.x, (px[0] * tilemap.tileSize) - (tilemap.tileSize)
                )
                # print("Snapped to right edge (top wall)")
            if mxpyTile == 0:  # Bottom-left empty
                position.x = max(
                    position.x, (mx[0] * tilemap.tileSize) + (tilemap.tileSize * 1.5)
                )
                # print("Snapped to left edge (top wall)")

        # Additional adjustments for right side
        if side == "right":
            if mxpyTile == 0:  # Bottom-left empty
                position.y = min(
                    position.y, (py[1] * tilemap.tileSize) - (tilemap.tileSize / 2)
                )
                # print("Snapped to bottom edge")
            if mxmyTile == 0:  # Top-left empty
                position.y = max(
                    position.y, (my[1] * tilemap.tileSize) + (tilemap.tileSize * 1.5)
                )
                # print("Snapped to top edge")

        # Additional adjustments for left side
        if side == "left":
            # Logic for left side adjustments can be added here if needed
            pass
            # if bottom-right is empty
            if pxpyTile == 0:
                position.y = min(
                    position.y, (py[1] * tilemap.tileSize) - (tilemap.tileSize / 2)
                )
                # print("bottom edge left wall")

            # if top-right is empty
            if pxmyTile == 0:
                position.y = max(
                    position.y, (my[1] * tilemap.tileSize) + (tilemap.tileSize * 1.5)
                )
                # print("top edge left wall")

    def spawnOrangePortal(self, position: pygame.Vector2, side: str = "right"):
        check = self.checkPosition(position, side)
        self.orangePortal.isAlive = True
        self.orangePortal.place(position, side)
        self.game.allSprites.add(self.orangePortal)

        self.ghost = EntityClone(
            anchor=self.orangePortal.origin, identifier="orange", link=self.orangePortal
        )
        # self.game.allSprites.add(self.ghost)

    def spawnBluePortal(self, position: pygame.Vector2, side: str = "right"):
        check = self.checkPosition(position, side)
        self.bluePortal.isAlive = True
        self.bluePortal.place(position, side)  # Pass the side argument
        self.game.allSprites.add(self.bluePortal)

        self.ghost2 = EntityClone(
            anchor=self.bluePortal.origin, identifier="blue", link=self.bluePortal
        )

        # self.game.allSprites.add(self.ghost2)

    def removePortals(self):
        # Remove portals from allSprites
        if self.orangePortal.isAlive:
            self.orangePortal.kill()
            self.orangePortal.isAlive = False
        if self.bluePortal.isAlive:
            self.bluePortal.kill()
            self.bluePortal.isAlive = False

        # Kill and mark clones as not alive
        if self.ghost:
            self.ghost = None
        if self.ghost2:
            self.ghost2 = None

    def proximityUpdate(self):
        physSprites = self.game.PhysSprites

        orangeSprites = []
        blueSprites = []

        foundOrange = False
        foundBlue = False
        for sprite in physSprites:
            sprite: Entity
            if sprite != self.orangePortal and sprite != self.bluePortal:
                if sprite.position.distance_to(self.orangePortal.origin) < 32:
                    if self.ghost:
                        self.ghost.set(sprite)
                        self.ghost.isAlive = True
                        foundOrange = True

                    distance = sprite.position.distance_to(self.orangePortal.origin)
                    orangeSprites.append({"sprite": sprite, "distance": distance})

                if sprite.position.distance_to(self.bluePortal.origin) < 32:
                    if self.ghost2:
                        self.ghost2.set(sprite)
                        self.ghost2.isAlive = True
                        foundBlue = True

                    distance = sprite.position.distance_to(self.bluePortal.origin)
                    blueSprites.append({"sprite": sprite, "distance": distance})

        if not foundOrange:
            if self.ghost:
                self.ghost.isAlive = False

        if not foundBlue:
            if self.ghost2:
                self.ghost2.isAlive = False

        # self.ghost2 = EntityClone(self.ghost)
        return orangeSprites, blueSprites

    def positionGhosts(self):
        if not self.ghost or not self.ghost2:
            return

        orientation = self.determineOrientationRelationship()

        # Determine which ghost is closer to its portal
        closer_ghost, farther_ghost = (
            (self.ghost, self.ghost2)
            if self.ghost.distance < self.ghost2.distance
            else (self.ghost2, self.ghost)
        )

        direction = closer_ghost.anchor - closer_ghost.position
        if direction.length() != 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        # Adjust direction based on orientation
        if orientation in ["horizontal_opposite", "vertical_opposite"]:
            direction *= -1

        if orientation == "horizontal_horizontal":
            direction.y *= -1

        # Update the position of the farther ghost
        farther_ghost.position = (
            farther_ghost.anchor + direction * closer_ghost.distance
        )

        # Apply additional adjustments based on orientation
        self.adjustPositionForOrientation(farther_ghost, orientation)

        # Update the rect of the farther ghost
        farther_ghost.rect.update(
            farther_ghost.position.x,
            farther_ghost.position.y,
            farther_ghost.rect.width,
            farther_ghost.rect.height,
        )

    def determineOrientationRelationship(self) -> str:
        """
        Determines the relative orientation between the orange and blue portals.
        Returns:
            str: A string indicating the relationship between the portals' orientations.
            Possible values are "horizontal_opposite", "vertical_opposite", "horizontal_horizontal", "vertical_vertical" or "unknown".
        """
        if (
            self.orangePortal.orientation == "right"
            and self.orangePortal.getOppositeOrientation()
            == self.bluePortal.orientation
        ) or (
            self.orangePortal.orientation == "left"
            and self.orangePortal.getOppositeOrientation()
            == self.bluePortal.orientation
        ):
            return "horizontal_opposite"
        elif (
            self.orangePortal.orientation == "top"
            and self.orangePortal.getOppositeOrientation()
            == self.bluePortal.orientation
        ) or (
            self.orangePortal.orientation == "bottom"
            and self.orangePortal.getOppositeOrientation()
            == self.bluePortal.orientation
        ):
            return "vertical_opposite"
        elif (
            self.orangePortal.orientation == "right"
            and self.bluePortal.orientation == "right"
        ) or (
            self.orangePortal.orientation == "left"
            and self.bluePortal.orientation == "left"
        ):
            return "horizontal_horizontal"
        return "unknown"

    def adjustPositionForOrientation(self, ghost, orientation):
        """
        Applies additional position adjustments based on the orientation.
        """
        if orientation == "vertical_opposite":
            ghost.position.x += ghost.rect.width / 1.5
            ghost.position.y += ghost.rect.height / 1.5
        elif orientation == "horizontal_opposite":
            ghost.position.x

    def update(self, delta, tick):
        orangeSprites, blueSprites = self.proximityUpdate()

        if self.orangePortal.isAlive and self.bluePortal.isAlive:
            orientation = self.determineOrientationRelationship()
            for portal, otherPortal, sprites in [
                (self.orangePortal, self.bluePortal, orangeSprites),
                (self.bluePortal, self.orangePortal, blueSprites),
            ]:
                if len(sprites) > 0:
                    for obj in sprites:
                        sprite: Entity = obj["sprite"]
                        distance: float = obj["distance"]

                        if sprite.rect.colliderect(portal.rect):
                            # print(f"collide with {portal.identifier}")
                            # print(f"Portal orientation: {portal.orientation}")
                            # print(
                            # f"Other portal orientation: {otherPortal.orientation}"
                            # )
                            # print(f"orientation: {orientation}")
                            sprite.use_collisions[portal.orientation] = False
                            sprite.use_collisions[portal.getOppositeOrientation()] = (
                                False
                            )
                            # print(f"sprite collisions: {sprite.use_collisions}")
                            sprite.in_portal = True
                            match orientation:
                                case "horizontal_opposite":
                                    if portal.orientation == "right":
                                        if sprite.rect.centerx < portal.origin.x:
                                            sprite.position.x = (
                                                otherPortal.origin.x
                                                - 1
                                                - sprite.rect.width / 2
                                            )
                                            sprite.position.y = portal.origin.y
                                    if portal.orientation == "left":
                                        if sprite.rect.centerx > portal.origin.x:
                                            sprite.position.x = (
                                                otherPortal.origin.x
                                                + 1
                                                + sprite.rect.width / 2
                                            )

                                            sprite.position.y = portal.origin.y
                                case "horizontal_horizontal":
                                    # if portal.orientation == "right":
                                    #     if sprite.rect.centerx < portal.origin.x:
                                    #         sprite.position.x = (
                                    #             otherPortal.origin.x
                                    #             - 1
                                    #             - sprite.rect.width / 2
                                    #         )
                                    #         sprite.position.y = portal.origin.y
                                    # print(f"portal origin: {portal.origin}")
                                    if portal.orientation == "left":
                                        if sprite.rect.centerx > portal.origin.x:
                                            sprite.position.x = otherPortal.origin.x
                                            sprite.position.y = otherPortal.origin.y

                                            sprite.flipX = not sprite.flipX
                                            sprite.velocity.x *= -1

                                case "vertical_opposite":
                                    if portal.orientation == "top":
                                        if sprite.rect.centery > portal.origin.y:
                                            sprite.position.y = (
                                                otherPortal.origin.y
                                                - 1
                                                - sprite.rect.height / 2
                                            )
                                            sprite.position.x = portal.origin.x

                                    if portal.orientation == "bottom":
                                        if sprite.rect.centery < portal.origin.y:
                                            sprite.position.y = (
                                                otherPortal.origin.y
                                                + 1
                                                + sprite.rect.height / 2
                                            )
                                            sprite.position.x = portal.origin.x

                                    sprite.flipY = not sprite.flipY
                                    sprite.velocity.y *= -1
                        elif not sprite.in_portal:
                            # # print(f"not colliding with {portal.identifier}")
                            sprite.use_collisions[portal.getOppositeOrientation()] = (
                                True
                            )
                            sprite.use_collisions[portal.orientation] = True
                            sprite.in_portal = False

            if self.ghost and self.ghost.isAlive:
                self.ghost.update(self.ghost2)
            if self.ghost2 and self.ghost2.isAlive:
                self.ghost2.update(self.ghost)

            self.positionGhosts()

            for portal in self.portals:
                portal.update(delta, tick)

        if self.game.input.key(pygame.K_r):
            self.removePortals()

    def draw(self, screen):
        if (self.ghost is not None) and self.ghost.isAlive:
            # # print("drawing orange ghost")
            self.ghost.draw(screen)
            # # print("drawing orange ghost")
        if (self.ghost2 is not None) and self.ghost2.isAlive:
            # # print("drawing blue ghost")
            self.ghost2.draw(screen)
            # # print("drawing blue ghost")
