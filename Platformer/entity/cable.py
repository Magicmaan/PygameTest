import math
import pygame


from Engine.Entity import Attributes, Entity
from Engine.util.vector import Vector2
from Platformer.util.math import generate_curved_points


class Cable(Entity):
    def __init__(self, position, length, color=(255, 255, 255), width=2):
        texturePath = "cable/cable"
        attributes: Attributes = {
            "identifier": "cable",
            "rect": (width, length),
            "useGravity": False,
            "canMove": Vector2(0, 0),
            "maxVelocity": Vector2(0, 0),
            "use_collisions": False,
        }
        Entity.__init__(self, position, texturePath, 0, attributes)

        self.color = color
        self.width = width
        self.length = length
        self.drop = 8
        self.sag = 16  # Sag factor for the cable

        self.animation_speed = 0.5
        self.animation_intensity = 0.25
        self.sway_range = 0.5

        self.count = 8
        self.points = []
        self.image = pygame.Surface((length, self.sag + 1), pygame.SRCALPHA)

        self.points = generate_curved_points(
            Vector2(0, 0), Vector2(self.length, 0), self.sag, 0.25, self.count
        )
        pygame.draw.lines(
            self.image,
            self.color,
            False,
            self.points,
            self.width,
        )

    def update(self, delta, tick):
        if tick % 2 == 0:
            return

        offset = (
            math.sin(tick / (100 / self.animation_speed) * math.pi) * self.sway_range
        )
        self.image.fill((0, 0, 0, 0))
        self.points = generate_curved_points(
            Vector2(0, 0), Vector2(self.length, 0), self.sag, offset, self.count
        )
        for i, point in enumerate(self.points):

            if offset < 0:
                point.x -= (
                    (i / len(self.points)) ** point.y
                ) * self.animation_intensity
            else:
                point.x += (
                    (i / len(self.points)) ** point.y
                ) * self.animation_intensity

            if i != 0 and i != len(self.points) - 1:
                point.y -= abs(offset * 2)
        pygame.draw.lines(
            self.image,
            self.color,
            False,
            self.points,
            self.width,
        )

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
