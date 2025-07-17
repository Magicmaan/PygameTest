import pygame
from Engine.Entity import Entity
from Engine.Program import Program

game = Program()


class Portal(Entity):
    def __init__(self, position, texturePath, attributes={}):

        portalAttributes = {
            "type": "portal",
            "rect": (4, 16),
            "useGravity": False,
            "canMove": pygame.Vector2(0, 0),
            "use_collisions": False,
        }
        # Merge default attributes with provided attributes
        attributes = {**portalAttributes, **attributes}

        Entity.__init__(self, position, texturePath, 0, attributes)

        self._rect = self.rect.copy()
        self.state = "idle"
        self.flipX = False
        self.isAlive = True
        self.canJump = False
        self.canMove = pygame.Vector2(0, 0)  # Disable movement for the portal
        self.orientation = "right"
        self.orientationMultiplier = pygame.Vector2(1, 1)
        self.origin = pygame.Vector2(0, 0)
        self.imageOffset.update(0, 0)
        print("Portal created at", position)

    def getOppositeOrientation(self):
        match self.orientation:
            case "right":
                return "left"
            case "left":
                return "right"
            case "top":
                return "bottom"
            case "bottom":
                return "top"

    def place(self, position: pygame.Vector2, orientation="right"):
        self.image = self._image.copy()
        self.orientation = orientation

        tilemap = self.game.tilemap
        # default to true rect in default orientation (on right wall)
        self.rect = self._rect.copy()
        # is on that side, so on Right side of a wall
        match orientation:
            case "right":
                print("right")
                self.flipX = False
                self.flipY = False
                self.rotation = 0.0
                self.position.update(position.x, position.y - self.image.height / 2)
                self.imageOffset.update(0, 0)

            case "left":
                print("ON LEFT FACE")
                self.flipX = True
                self.flipY = False
                self.rotation = 180.0
                self.image = pygame.transform.flip(self.image, True, False)

                self.position.update(
                    position.x + tilemap.tileSize - self.rect.width,
                    position.y - self.image.get_height() / 2,
                )

                self.imageOffset.update(-tilemap.tileSize + self.rect.width, 0)

            case "top":
                self.flipY = False
                self.flipX = False
                self.rotation = 90.0
                self.image = pygame.transform.rotate(self.image, 90.0)
                print("TOP")
                self.rect.update(
                    self.position.x,
                    self.position.y,
                    self.rect.height,
                    self.rect.width,
                )
                self.position.update(
                    position.x,
                    position.y + tilemap.tileSize - self.rect.height,
                )

                self.imageOffset.update(0, -tilemap.tileSize + self.rect.height)

            case "bottom":
                self.flipY = True
                self.flipX = False
                self.rotation = -90.0
                self.image = pygame.transform.rotate(self.image, -90.0)

                self.position.update(
                    position.x, position.y + tilemap.tileSize - self.rect.height
                )
                self.rect.update(
                    self.position.x,
                    self.position.y,
                    self.rect.height,
                    self.rect.width,
                )
                self.imageOffset.update(0, 0)

        self.rect.update(
            self.position.x, self.position.y, self.rect.width, self.rect.height
        )

        self.updateOrigin()
        # # self.center = self.rect.center
        # match orientation:
        #     case "right":
        #         self.origin.update(self.rect.left, self.rect.top)
        #     case "left":
        #         self.origin.update(self.rect.right, self.rect.top)
        #     case "top":
        #         self.origin.update(self.rect.centerx, self.position.y)
        #     case "bottom":
        #         self.origin.update(self.rect.centerx, self.position.y + 16)

    def updateOrigin(self):
        rect = self.rect.copy()
        rect.update(
            rect.x + self.imageOffset.x,
            rect.y + self.imageOffset.y,
            rect.width,
            rect.height,
        )
        # rect += self.imageOffset
        # Update the origin based on the current position and orientation
        match self.orientation:
            case "right":
                self.origin.update(rect.left, rect.centery)
            case "left":
                self.origin.update(rect.right + 16 - rect.width, rect.centery)
            case "top":
                self.origin.update(rect.centerx, rect.y + 16)
            case "bottom":
                self.origin.update(rect.centerx, rect.y)

    def update(self, delta, tick):
        # self.image = pygame.transform.flip(self.image, self.flipX, self.flipY)
        # self.image = pygame.transform.rotate(self.image, self.rotation)
        if not self.isAlive:
            self.kill()
            return

        self.rect.update(
            self.position.x + self.imageOffset.x,
            self.position.y + self.imageOffset.y,
            self.rect.width,
            self.rect.height,
        )
        # self.updateOrigin()

    def draw(self, surface):
        super().draw(surface)

        # Draw a circle at the origin
        pygame.draw.circle(
            surface,
            (255, 0, 0),
            round(self.origin + game.camera.position, 0),
            2,
        )
