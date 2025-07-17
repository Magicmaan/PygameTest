from Engine.Entity import Entity
from Engine.Program import Program
from Engine.InputHandler import InputHandler
import random


import pygame
import math

from Engine.debug.logger import debugCollision, debugRect
from Engine.renderer.utils import GLQuad
from Engine.util.delta import DeltaValue
from Engine.util.vector import Vector2
from Platformer.portal.portalHandler import PortalHandler

game = Program()


class Player(Entity):
    def __init__(self, position):
        texturePath = "player/chell_spritesheet"

        animations = {
            "idle": (0, 1, 2, 3, 20),
            "run": (4, 5, 6, 7, 8),
            "jump": (8, 1),
            "crouch": (9, 1),
            "afk": (8, 9, 10),
        }

        attributes = {
            "animations": animations,
            "identifier": "player",
            "rect": (10, 16),
            "useGravity": True,
            "airTimer": 0,
            "friction": 0.2,
            "canJump": True,
            "jumpCoyote": 20,
            "canMove": pygame.Vector2(1, 1),
            "maxVelocity": pygame.Vector2(100, 20),
            "use_collisions": True,
        }
        Entity.__init__(self, position, texturePath, 0, attributes)
        # self.texID = None
        # if not self.texID:
        #     self.texID = self.game.renderer.surfaceToTexture(self.image)
        # else:
        #     self.game.renderer.surfaceToTexture(self.image, self.texID)
        # self.quad = GLQuad(
        #     position=(0, 0),
        #     size=self.game.renderer.game_normalised(self.image.size),
        #     texture_id=self.texID,
        #     texture_coords=(0, 0, 1, 1),
        # )
        # self.game.renderer.add_quad(self.quad)

        self.rotation = 0
        self.jumpHeight = -200
        # self.jumpCoyote = 20
        self.flipX = False
        self.acceleration = 5
        self.airAcceleration = 5

        self.portalHandler: PortalHandler = None
        for obj in game.allObjects:
            if obj.identifier == "portalHandler":
                self.portalHandler = obj
                break
        if self.portalHandler is None:
            raise Exception("PortalHandler not found in allObjects")

    def update(self, delta, tick):
        # [script.update(self, delta) for script in self.scripts]
        self.flipX = False
        self.isMoving = False
        self.lastInput = self.input
        # game.raycaster.rays.clear()

        mousePos = game.input.mouse.positionWorld
        print(f"velocity before: {self.velocity.x}, {self.velocity.y}")
        if game.input.key_raw(pygame.K_LCTRL) and game.input.key_raw(pygame.K_LSHIFT):
            self.friction.set(1.0)
            self.acceleration = 1
            self.maxVelocity.update(0.5, 5)
            self.state = "crouch"
            # game.particles.add(pygame.Vector2(self.rect.center),"leaf",count=50)
        else:
            self.friction.set(8)
            self.acceleration = 5
            self.maxVelocity.update(1.5, 10)

        # if canJump ( if on ground, or x frames after onGround (coyote time))
        if game.input.key_raw(pygame.K_SPACE) and (self.canJump):
            # set canJump to false to prevent multiple input
            self.canJump = False

            height = self.jumpHeight * game.dt
            if self.groundTimer < 10:
                height /= (1 + self.groundTimer / 5) ** 2
            self.velocity.y = height

            # if crouching, set velocity to jump higher
            if game.input.crouch():
                self.velocity.y *= 1.1
            self.state = "jump"
            self.input = "jump"

        if (
            game.input.key_raw(pygame.K_a)
            and self.canMove[0]
            and not self.collisions["left"]
        ):

            if self.onGround:
                self.velocity.x -= self.acceleration * game.dt
                self.state = "run"
            else:
                # give grace period on jump, so can still influence direction slightly
                self.isMoving = True
                if self.airTimer < self.jumpCoyote // 2:
                    self.velocity.x -= self.acceleration * game.dt
                else:
                    self.velocity.x -= self.airAcceleration * game.dt

            if self.lastInput == "right" and self.onGround:
                self.velocity.x = math.copysign(self.velocity.x / 4, -1)

            self.isMoving = True
            self.flipX = True
            self.input = "left"

        if (
            game.input.key_raw(pygame.K_d)
            and self.canMove[0]
            and not self.collisions["right"]
        ):
            if self.onGround:
                self.velocity.x += self.acceleration * game.dt
                self.state = "run"
            else:
                self.isMoving = True
                if self.airTimer < self.jumpCoyote // 2:
                    self.velocity.x += self.acceleration * game.dt
                else:
                    self.velocity.x += self.airAcceleration * game.dt

            self.isMoving = True
            self.flipX = False
            self.input = "right"
            if self.lastInput == "left" and self.onGround:
                self.velocity.x = math.copysign(self.velocity.x / 4, 1)

        mouse = game.input.getMouse()
        if mouse.leftClick or mouse.rightClick:
            ray = game.raycaster.addRay(
                Vector2(self.rect.center), 10, to=mousePos, lifespan=5
            )

            if ray.collision:
                print("hit", ray.collisionSide, ray.contactPoint)

                if mouse.leftClick:
                    self.portalHandler.spawnOrangePortal(
                        ray.contactPoint, ray.collisionSide
                    )
                elif mouse.rightClick:
                    self.portalHandler.spawnBluePortal(
                        ray.contactPoint, ray.collisionSide
                    )
                direction_vector = pygame.Vector2(
                    ray.contactPoint.x - self.rect.center[0],
                    ray.contactPoint.y - self.rect.center[1],
                )
                if direction_vector.length() > 0:
                    direction_vector = direction_vector.normalize()
                else:
                    direction_vector = pygame.Vector2(0, 0)
                direction_vector *= 100

                pArgs = {
                    "CycleImg": True,
                    "UseVelocity": True,
                    "Acceleration": direction_vector,
                    "CycleImgFrequency": 50,
                    "texture": 0,
                    "wind": False,
                    "randomTex": True,
                    "randomTexBounds": (4, 5),
                    "spread": (5, 10),
                    "lifespan": random.randint(100, 300),
                    "canFlip": True,
                }
                game.particles.add(ray.origin, "default", count=1, addArgs=pArgs)

        print(f"velocity: {self.velocity.x}, {self.velocity.y}")

        self.gfxUpdate()
        if self.velocity.x != 0 or self.velocity.y != 0:
            print("moving")
        super().update(delta, tick)

    def gfxUpdate(self):
        feetPos = pygame.Vector2(self.rect.centerx, self.rect.bottom)
        midPos = pygame.Vector2(self.rect.center)
        randomNum = random.randint(0, 100)

        if self.velocity.x < 0:
            veloffsetX = 10
        else:
            veloffsetX = -10

    # @debugRect
    def draw(self, surface):
        # self.particles.draw(surface)
        super().draw(surface)
