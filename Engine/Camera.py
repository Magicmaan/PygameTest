from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Engine.Program import Program

from Engine.util import Vector2


class Camera:
    def __init__(self, program: Program):
        self.position = Vector2(1, 1)
        self.game = program
        self.width = program.renderer.width
        self.height = program.renderer.width
        self.render_ratio = program.renderer.render_scale

        self.follow_target: bool = True
        self.target: Vector2 = Vector2(0, 0)
        self.lerp_offset = Vector2(32, 0)
        self.lerp_speed = 0.15

    def getScreenPosition(self, position: Vector2) -> Vector2:
        """
        Convert world coordinates to screen coordinates.

        :param position: The world position (Vector2).
        :return: The screen position (Vector2).
        """
        val = position + self.position
        val.x = int(val.x * self.render_ratio.x)
        val.y = int(val.y * self.render_ratio.y)
        return val

    def applyRatio(self, position: Vector2) -> Vector2:
        """
        Apply the render ratio to a given position.

        :param position: The position (Vector2).
        :return: The adjusted position (Vector2).
        """
        val = Vector2(
            position.x * self.render_ratio.x, position.y * self.render_ratio.y
        )
        return val

    def applyRatio(self, value: float) -> float:
        """
        Apply the render ratio to a given value.

        :param value: The value (float).
        :return: The adjusted value (float).
        """
        val = value * self.render_ratio.x
        return val

    def lerp(self, target: Vector2, speed: float) -> Vector2:
        """
        Linearly interpolate between the current position and the target position.

        :param target: The target position (Vector2).
        :param speed: The interpolation speed (float).
        :return: The new position (Vector2).
        """
        self.position.update(
            self.position.smoothstep(target, speed),
        )
        return self.position

    def update(self, delta, tick):
        # self.lerp_offset.update(
        #     (self.lerp_offset.x + 1) % (self.game.renderer.width / 2),
        #     self.lerp_offset.y,
        # )

        if (self.follow_target) and (self.target != self.position):
            self.lerp(
                Vector2(-self.target.x + self.game.renderer.width / 2, self.position.y)
                + self.lerp_offset,
                self.lerp_speed,
            )

    def follow(self, target: Vector2):
        """
        Set camera to follow a target position.
        :param target: The target position (Vector2).
        """
        self.target = target
        self.follow_target = True

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.update(value, self.position.y)

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.update(self.position.x, value)
