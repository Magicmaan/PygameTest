from __future__ import annotations
from typing import TYPE_CHECKING

from Engine.renderer.utils import GLQuad
from Engine.util.vector import Vector2, tupleToVector

if TYPE_CHECKING:
    from Engine import *

import math
import pygame
from Engine import Raycaster, TextGUI
from pprint import pprint
from Engine.InputHandler import InputHandler


class Debugger:
    def __init__(
        self,
        game: Program,
        surface,
        enableDebug=False,
        enableFPS=True,
        enableObjectDebug=False,
    ):
        self.game: Program = game
        self.surface = surface
        self.lineoffset = 4

        self.enableDebug = True
        self.enableFPS = enableFPS
        self.enableObjectDebug = enableObjectDebug
        self.showcollisions = True
        self.tileGrid = False

        self.toggleTimer = 0

        self.rects = []

        self._debug_rects = [
            pygame.Rect(50, 50, 16, 16),
        ]

        self._debug_lines: list[list[Vector2, Vector2, tuple[int, int, int]]] = [
            [Vector2(0, 0), Vector2(100, 100), (255, 0, 0)],
        ]

        self.debug_objects = []

        self.identifier = "debugger"

    def printFPS(self, clock):
        TextGUI.write_debug(str(round(clock.get_fps(), 1)), self.surface, [0, 0])

        TextGUI.write_debug(
            str(len(self.game.particles.particles)), self.surface, [0, 20]
        )

    def addTarget(self, target, debugGroup):
        debugGroup.add(target)

    def removeTarget(self, target, debugGroup):
        debugGroup.remove(target)

    def add_rect(self, rect):
        if not isinstance(rect, pygame.Rect):
            raise ValueError("Expected a pygame.Rect object.")
        if self._debug_rects.__contains__(rect):
            return

        self._debug_rects.append(rect)

    def remove_rect(self, rect):
        if not isinstance(rect, pygame.Rect):
            raise ValueError("Expected a pygame.Rect object.")
        if self._debug_rects.__contains__(rect):
            self._debug_rects.remove(rect)

    def clear_rects(self):
        self._debug_rects.clear()

    def add_debug_line(self, line):
        if not isinstance(line, list):
            raise ValueError("Expected a list of objects.")
        self._debug_lines.append(line)

    def remove_debug_line(self, line):
        if not isinstance(line, list) or len(line) != 2:
            raise ValueError("Expected a list of two Vector2 objects.")
        if not isinstance(line[0], Vector2) or not isinstance(line[1], Vector2):
            raise ValueError("Expected two Vector2 objects.")
        if self._debug_lines.__contains__(line):
            self._debug_lines.remove(line)

    def clear_debug_lines(self):
        self._debug_lines.clear()

    def draw(self, surface: pygame.Surface):
        if self.game.input.key(pygame.K_f):
            self.enableDebug = not self.enableDebug

        if not self.enableDebug:
            return
        # print("DEBUGGER DRAW")
        # surface.fill((0, 255, 0))

        TextGUI.write_debug(str(round(self.game.clock.get_fps(), 1)), surface, [0, 0])

        TextGUI.write_debug(str(len(self.game.particles.particles)), surface, [0, 20])
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (20, 20, 100, 100),
            1,
        )
        for rect in self._debug_rects:
            expanded_rect = rect.copy()
            # expanded_rect.update(
            #     expanded_rect.x * self.game.camera.render_ratio.x,
            #     expanded_rect.y * self.game.camera.render_ratio.y,
            #     expanded_rect.width * self.game.camera.render_ratio.x,
            #     expanded_rect.height * self.game.camera.render_ratio.y,
            # )
            # add camera offset to get the screen position
            expanded_rect.topleft = [
                expanded_rect.x + self.game.camera.position.x,
                expanded_rect.y + self.game.camera.position.y,
            ]
            pygame.draw.rect(surface, (0, 255, 0), expanded_rect, 2)

            TextGUI.write_debug(
                str(rect),
                surface,
                [expanded_rect.x, expanded_rect.y - 12],
                size="small",
            )

        for line in self._debug_lines:
            start = line[0]
            end = line[1]
            try:
                colour = line[2]
            except IndexError:
                colour = (255, 0, 0)

            start = self.game.camera.getScreenPosition(start)
            end = self.game.camera.getScreenPosition(end)

            # start.y += 20

            pygame.draw.line(surface, colour, start, end, 5)

        if not self.enableDebug:
            return

        self.clear_debug_lines()
        self.clear_rects()

        self.printTileGrid(surface)

    def printRayCast(self, raycast: Raycaster):

        for ray in raycast.rays:
            ray: Raycaster.Ray

            end: pygame.Vector2 = ray.origin + pygame.Vector2(
                ray.length * math.cos(math.radians(ray.angle)),
                ray.length * math.sin(math.radians(ray.angle)),
            )

            # Draw the ray using screen positions
            pygame.draw.line(
                self.surface,
                "red",
                self.game.camera.getScreenPosition(ray.origin),
                self.game.camera.getScreenPosition(end),
            )

    def printTileGrid(self, surface: pygame.Surface):
        tilemap = self.game.tileMap

        # self.game.camera.renderRatio.x = outputRes[0] / nativeRes[0]
        xMult = self.game.camera.render_ratio.x
        yMult = self.game.camera.render_ratio.y
        offsetX = int(self.game.camera.position.x % 16) * xMult
        offsetY = int(self.game.camera.position.y % 16) * yMult

        tmp = 0
        for i in range(0, self.game.tileMap.width + 10, 2):
            for j in range(0, self.game.tileMap.height + 10, 1):
                if j % 2 == 0:
                    tmp = 1
                else:
                    tmp = 0

                # convert tilemap coordinates to screen coordinates
                x = ((i + tmp) * tilemap.tileSize) + self.game.camera.position.x
                y = (j * tilemap.tileSize) + self.game.camera.position.y

                pygame.draw.rect(
                    surface,
                    (0, 0, 255),
                    (
                        x,
                        y,
                        self.game.tileMap.tileSize,
                        self.game.tileMap.tileSize,
                    ),
                    1,
                )
                TextGUI.write_debug(
                    str(i) + "," + str(j),
                    surface,
                    [
                        x,
                        y,
                    ],
                    (255, 255, 255, 125),
                    size="small",
                )

                # draw tile coords above aswell
                TextGUI.write_debug(
                    str(i) + "," + str(j - 1),
                    surface,
                    [
                        x,
                        y - tilemap.tileSize,
                    ],
                    (255, 255, 255, 125),
                    size="small",
                )

    def printObjects(self, debugGroup):
        for obj in debugGroup.sprites():
            position = self.game.camera.getScreenPosition(obj.position)

            position.x /= self.game.camera.render_ratio.x
            position.y /= self.game.camera.render_ratio.y
            if position.y < 0:
                position.y = 0
            elif position.y + obj.rect.height > self.game.renderer.height:
                position.y = self.game.renderer.height - obj.rect.height

            if position.x < 0:
                position.x = 0
            elif position.x + obj.rect.width > self.game.renderer.width:
                position.x = self.game.renderer.width - 16

            position.x *= self.game.camera.render_ratio.x
            position.y *= self.game.camera.render_ratio.y

            rect = obj.rect.copy()
            rect.x = position.x
            rect.y = position.y
            rect.width = self.game.camera.applyRatio(obj.rect.width)
            rect.height = self.game.camera.applyRatio(obj.rect.height)
            # # add camera offset
            # posX += self.game.camera.x
            # posY += self.game.camera.y

            TextGUI.write_debug(
                obj.identifier + " " + obj.state,
                self.surface,
                [position.x, (position.y + obj.rect.height)],
            )
            n = 0
            l = 10 * self.game.camera.render_ratio.y
            TextGUI.write_debug(
                "X:"
                + str(round(obj.position.x, 2))
                + " V:"
                + str(round(obj.velocity.x, 2)),
                self.surface,
                [(position.x + obj.rect.width), (position.y + n * l)],
            )
            n += 1
            TextGUI.write_debug(
                "Y:"
                + str(round(obj.position.y, 2))
                + " V:"
                + str(round(obj.velocity.y, 2)),
                self.surface,
                [(position.x + obj.rect.width), (position.y + n * l)],
            )
            n = n + 2
            if obj.animations and obj.state in obj.animations.keys():
                TextGUI.write_debug(
                    "Anim:" + str(obj.animations[obj.state][obj.animationPos]),
                    self.surface,
                    [(position.x + obj.rect.width), (position.y + n * l)],
                )
            else:
                TextGUI.write_debug(
                    "Anim: None",
                    self.surface,
                    [(position.x + obj.rect.width), (position.y + n * l)],
                )

            pygame.draw.rect(
                self.surface,
                (0, 255, 0),
                (
                    position.x,
                    position.y,
                    rect.width,
                    rect.height,
                ),
                1,
            )

            if self.showcollisions:
                if obj.collisions["up"]:
                    pygame.draw.rect(
                        self.surface,
                        (255, 0, 0),
                        (
                            position.x,
                            position.y,
                            obj.rect.width,
                            2,
                        ),
                    )
                if obj.collisions["down"]:
                    pygame.draw.rect(
                        self.surface,
                        (255, 0, 0),
                        (
                            position.x,
                            position.y + obj.rect.height,
                            obj.rect.width,
                            2,
                        ),
                    )
                if obj.collisions["left"]:
                    pygame.draw.rect(
                        self.surface,
                        (255, 0, 0),
                        (
                            position.x,
                            position.y,
                            2,
                            obj.rect.height,
                        ),
                    )
                if obj.collisions["right"]:
                    pygame.draw.rect(
                        self.surface,
                        (255, 0, 0),
                        (
                            position.x + obj.rect.width - 2,
                            position.y,
                            2,
                            obj.rect.height,
                        ),
                    )
