from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Platformer.portal.portalHandler import PortalHandler
    from Platformer.portal.Portal import Portal

from pygame import Surface
import pygame
from Engine import Program
from Engine.Entity import Entity
from random import randint
import math

game = Program()


class EntityClone(Entity):
    def __init__(
        self,
        entity: Entity = None,
        anchor: pygame.math.Vector2 = None,
        identifier: str = None,
        link: Portal = None,
    ):
        super().__init__(anchor, "entity", 0, {})
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255), 100)
        self.anchor = anchor if anchor else pygame.math.Vector2(0, 0)
        self.isAlive = False
        if entity is None:
            self.entity: Entity = None
            self.position = pygame.math.Vector2(0, 0)
            self.center = pygame.math.Vector2(0, 0)
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.attributes = {}
            self.identifier = identifier if identifier else "entity_clone"
            self.image = Surface((0, 0))

        else:
            self.set(entity)

        self.link = link

        self.distance = 0
        self.angle = 0

        self.portalHandler: PortalHandler = None

    def update(self, otherClone: "EntityClone" = None):
        if not self.isAlive:
            return

        if self.portalHandler is None:
            for obj in game.allObjects:
                if obj.identifier == "portalHandler":
                    self.portalHandler = obj
                    break
            if self.portalHandler is None:
                raise Exception("PortalHandler not found in allObjects")

        # print("clone update ", self.identifier)

        # # Update the clone's position and other attributes based on the original entity
        # self.position = self.entity.position.copy()
        # self.center = self.entity.center.copy()
        # self.rect = self.entity.rect.copy()
        # self.attributes = self.entity.attributes.copy()

        self.distance = self.anchor.distance_to(self.position)
        self.angle = math.atan2(
            self.position.y - self.anchor.y,
            self.position.x - self.anchor.x,
        )
        self.angle = math.degrees(self.angle) % 360

        if otherClone and otherClone.isAlive:
            if otherClone.distance < self.distance:
                self.distance = otherClone.distance
                self.position.x = self.anchor.x + self.distance * math.cos(
                    math.radians(self.angle)
                )
                self.position.y = self.anchor.y + self.distance * math.sin(
                    math.radians(self.angle)
                )
        else:
            self.position = self.entity.position.copy()
            # self.center = self.entity.center.copy()
            self.rect = self.entity.rect.copy()

    def draw(self, surface: pygame.Surface):
        # obj rect doesn't always match sprite
        # must adjust image to be centered inside rect
        correctedPos = pygame.Vector2(
            self.rect.centerx - self.image.get_width() / 2,
            self.rect.centery - self.image.get_height() / 2,
        )
        # correctedPos.y = round(correctedPos.y, 2)

        # clip = self.rect.clip(game.)

        if self.isAlive:
            if self.useOutline:
                self.drawOutline(surface, correctedPos.copy())

            surface.blit(self.image, round(correctedPos + game.camera.position, 0))

    def kill(self):
        super().kill()
        # Remove the clone from the game
        self.isAlive = False

    def set(self, entity: Entity):
        # Set the original entity to the clone's attributes
        self.entity = entity
        self.position = entity.position.copy()
        self.rect = entity.rect.copy()
        self.attributes = entity.attributes.copy()
        # self.identifier = entity.identifier + "_clone"
        self.image = entity.image
        # self.image.fill(self.colour)  # Fill with a random colour
        self.isAlive = True
