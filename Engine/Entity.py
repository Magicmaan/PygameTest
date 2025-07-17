from __future__ import annotations
from typing import Literal
from Engine.renderer.utils import GLQuad
from Engine.util.math import minmax
import pygame
import math
import random

# from Engine.Program import Program
from Engine.TextureHandler import TextureHandler
from Engine.CollisionHandler import *
from pprint import pprint
from types import SimpleNamespace
from Engine.debug.logger import debugRect
from Engine.util import Vector2

from typing import TypedDict

from Engine.util.delta import DeltaValue


game = Program()
Texture = TextureHandler()


class Attributes(TypedDict, total=False):
    identifier: str
    rect: tuple[int, int]
    maxVelocity: pygame.math.Vector2
    gravity: int
    useGravity: bool
    use_collisions: bool
    airTimer: int
    friction: float
    canJump: bool
    jumpCoyote: int
    canMove: pygame.math.Vector2
    animations: dict[str, list[int]]
    type: str


class Entity(pygame.sprite.Sprite):
    class Collisions(TypedDict):
        up: bool
        down: bool
        left: bool
        right: bool

    def __init__(
        self,
        position: Vector2,
        texturePath,
        texturePos=0,
        attributes: Attributes = {
            "identifier": "entity",
            "rect": None,
            "maxVelocity": pygame.math.Vector2(1.5, 10),
            "gravity": 10,
            "useGravity": True,
            "use_collisions": True,
            "airTimer": 0,
            "friction": 10,
            "canJump": True,
            "jumpCoyote": 20,
            "canMove": Vector2(1, 1),
            "animations": None,
        },
    ):
        pygame.sprite.Sprite.__init__(pygame.sprite.Sprite)
        self.scripts = []
        self.position = position
        self.center = self.position.copy()
        self.game = game

        self.logger = game.logger.get_logger("Entity")

        # Default attributes table
        default_attributes: Attributes = {
            "identifier": "entity",
            "rect": None,
            "maxVelocity": pygame.math.Vector2(1.5, 10),
            "gravity": 10,
            "useGravity": True,
            "use_collisions": True,
            "airTimer": 0,
            "friction": 10,
            "canJump": True,
            "jumpCoyote": 20,
            "canMove": Vector2(1, 1),
            "animations": None,
            "type": "entity",
        }

        # Merge default attributes with provided attributes
        self.attributes = {**default_attributes, **attributes}

        self.identifier = self.attributes["identifier"]
        self.type = self.attributes["type"]

        Texture.load_texture(texturePath, (16, 16))
        self.rect = (
            pygame.Rect(
                self.position.x,
                self.position.y,
                self.attributes["rect"][0] if self.attributes["rect"] else 0,
                self.attributes["rect"][1] if self.attributes["rect"] else 0,
            )
            if self.attributes["rect"]
            else pygame.Rect(
                self.position.x,
                self.position.y,
                Texture.texture(texturePath, 0).get_width(),
                Texture.texture(texturePath, 0).get_height(),
            )
        )
        self.screen_rect = self.rect.copy()
        self.maxVelocity: Vector2 = self.attributes["maxVelocity"]
        self.gravity: int = self.attributes["gravity"]
        self.useGravity: bool = self.attributes["useGravity"]

        self.airTimer: int = self.attributes["airTimer"]
        self.friction: DeltaValue = DeltaValue(self, self.attributes["friction"])
        self.canJump: bool = self.attributes["canJump"]
        self.jumpCoyote: int = self.attributes["jumpCoyote"]
        self.canMove: Vector2 = self.attributes["canMove"]

        self.use_collisions: Entity.Collisions = {
            "up": self.attributes["use_collisions"],
            "down": self.attributes["use_collisions"],
            "left": self.attributes["use_collisions"],
            "right": self.attributes["use_collisions"],
        }

        self.state = "idle"
        self.flipX = False
        self.flipY = False
        self.rotation = 0
        self.isAlive = True

        self.input = ""
        self.lastInput = self.input

        self.onGround = False
        self.groundTimer = 0

        self.isMoving = False
        self.isMovingTimer = 0

        self.velocity = pygame.math.Vector2(0, 0)

        # collisions setup
        self.collisions: Entity.Collisions = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.in_portal = False

        # texture setup
        self.texturePath = texturePath
        self._image = Texture.texture(self.texturePath, texturePos)
        self.image = self._image.copy()
        self.imageOffset = Vector2(-3, 0)

        self.useOutline = False
        self.imageOutline = False
        self.outlineColour = (255, 0, 255)

        # Animation setup
        if self.attributes["animations"]:
            self.hasAnimation = True
            self.animations = self.attributes["animations"]
            self.animationPos = 0
        else:
            self.hasAnimation = False
            self.animations = None
            self.animationPos = 0

        # test_delta = DeltaValue(self, 1.0)

        self._has_updated = False
        self._current_tick = -1

    def update(self, delta, tick):
        if self._current_tick == tick:
            self._has_updated = True
            return
        self._current_tick = tick
        [script.update(self, delta, tick) for script in self.scripts]

        if abs(self.velocity.x) > (
            self.maxVelocity.x * game.TimeMult
        ):  # max velocity speed cap
            self.velocity.x = math.copysign(
                self.maxVelocity.x * game.TimeMult, self.velocity.x
            )

        self.logger.info(
            f"friction: {self.friction}, velocity: {self.velocity.copy().x}"
        )
        if not self.isMoving:  # slow down if not moving
            self.velocity.x = self.velocity.x * (1 - self.friction)
            if math.isclose(self.velocity.x, 0, abs_tol=0.05):
                self.velocity.x = 0

        if (
            self.useGravity and self.canMove.y
        ):  # Apply gravity only if useGravity is True
            self.velocity.y += (self.gravity * game.dt) / game.TimeMult
        # vertical speed cap
        self.velocity.y = min(self.maxVelocity.y * game.TimeMult, self.velocity.y)

        self.onGround = False
        self.isFalling = False
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False

        if self.canMove.x or self.canMove.y:
            # check and update collisions
            collideUpdate(self, game.floorColliders, game.tileMap)
            # collideUpdate(self,game.PhysSprites,game.tileMap)

        if self.canMove.x:
            self.position.x += self.velocity.x
        if self.canMove.y:
            self.position.y += self.velocity.y

        # Since rect isn't always same size as image, we need to update it manually
        # to match the position of the image
        self.rect.update(
            self.position.x, self.position.y, self.rect.width, self.rect.height
        )
        self.screen_rect.update(
            self.rect.x + game.camera.x + self.imageOffset.x,
            self.rect.y + game.camera.y + self.imageOffset.y,
            self.rect.width,
            self.rect.height,
        )

        if not self.onGround:
            self.airTimer += 1
            self.groundTimer = 0
            if self.airTimer > self.jumpCoyote:
                self.canJump = False
        else:
            self.groundTimer += 1
            self.canJump = True
            self.isFalling = False
            self.airTimer = 0

        if not self.isMoving:
            self.isMovingTimer += 1
        else:
            self.isMovingTimer = 0

        if (self.velocity.x == 0) and (self.velocity.y == 0):
            self.state = "idle"

        if self.isMovingTimer > game.afkTimer:
            self.state = "afk"

        self.animationUpdate()

        self.image = pygame.transform.flip(self.image, self.flipX, self.flipY)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        self.logger.debug(
            f"Entity after update velocity: {self.velocity}, position: {self.position}, state: {self.state}"
        )

    def animationUpdate(self):
        if not self.hasAnimation:  # if no animations, return from function
            return

        if not self.state in self.animations.keys():
            state = "idle"
        else:
            state = self.state

        # gets last entry in animationSlides state, which is FPS value
        animationFPS = self.animations[state][-1]
        # checks remainder againsts game tick, if so increment animation
        if game.tick % (animationFPS // game.TimeMult) == 0:
            self.animationPos += 1

        # animation overflow check
        if self.animationPos >= len(self.animations[state]) - 1:
            self.animationPos = 0

        # getSprite()
        # from objects animation slides, takes in thestate values and animation position
        # this returns a number corresponding to position on spritesheet for getSprite()

        # get spritesheet pos
        pos = self.animations[state][self.animationPos]
        self._image = Texture.texture(self.texturePath, pos)
        self.image = self._image.copy()

    def draw(self, surface: pygame.Surface):
        # obj rect doesn't always match sprite
        # must adjust image to be centered inside rect
        # correctedPos = Vector2(
        #     self.rect.centerx - self.image.get_width() / 2,
        #     self.rect.centery - self.image.get_height() / 2,
        # )
        # correctedPos.y = round(correctedPos.y, 2)

        if self.isAlive:
            if self.useOutline:
                self.drawOutline(surface, self.position.copy())

            surface.blit(
                self.image,
                self.screen_rect,
            )

    def drawOutline(self, surface, pos):
        # convert sprite to mask then back to surface to produce monochrome outline
        image = pygame.mask.from_surface(self.image).to_surface()
        image.fill(self.outlineColour, special_flags=pygame.BLEND_RGBA_MULT)
        image.set_colorkey((0, 0, 0))
        # Blit the BW outline, offset around main player
        surface.blit(
            image, (round(pos.x - 1 + game.camera.x), round(pos.y + game.camera.y))
        )  # left
        surface.blit(
            image, (round(pos.x + 1 + game.camera.x), round(pos.y + game.camera.y))
        )  # right
        surface.blit(
            image, (round(pos.x - 1 + game.camera.x), round(pos.y - 1 + game.camera.y))
        )  # up
        surface.blit(
            image, (round(pos.x - 1 + game.camera.x), round(pos.y + 1 + game.camera.y))
        )  # down
