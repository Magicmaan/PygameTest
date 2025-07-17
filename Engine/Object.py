import pygame
from Engine.Entity import Entity
from Engine.Program import Program
from Engine.TextureHandler import TextureHandler


Texture = TextureHandler()
game = Program()


class Object(Entity):
    def __init__(self, position, texturePath, texturePos=0, attributes={}):
        super().__init__(position, texturePath, texturePos, attributes)

        self.position = position
        self.state = "solid"
        self.identifier = "object"
        self.attributes = attributes
        self.flipX = False
        self.angle = 0
        self.isAlive = True
        self.use_collisions = {
            "up": True,
            "down": True,
            "left": True,
            "right": True,
        }

        if "identifier" in attributes:
            self.identifier = attributes["identifier"]
        if "flip" in attributes:
            self.flipX = attributes["flip"]
        if "angle" in attributes:
            self.angle = attributes["angle"]

        # Assign animation tags
        if "animations" in attributes:
            self.hasAnimation = True
            self.animations = attributes["animations"]
            self.animationPos = 0
        else:
            self.hasAnimation = False

        self.image = Texture.texture(texturePath, texturePos)
        self.image = pygame.transform.flip(self.image, self.flipX, False)
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.image.get_width(),
            self.image.get_height(),
        )

    def update(self, delta, tick):
        if hasattr(self, "onTouch"):
            self.onTouch()
        if hasattr(self, "onClick"):
            self.onClick()

        self.animationUpdate()

    def draw(self, surface):
        if not (
            self.rect.right + game.camera.position.x < 0
            or self.rect.left + game.camera.position.x > surface.get_width()
        ):
            self.isAlive = True
        else:
            self.isAlive = False

        if self.isAlive:
            surface.blit(self.image, self.position + game.camera.position)

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
        self.image = Texture.texture(self.texturePath, pos)
