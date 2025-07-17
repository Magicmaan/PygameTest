import pygame
from Engine.Entity import Entity
from Engine.Program import Program
from Engine.util.vector import Vector2, tupleToVector

game: Program = Program()


class Platform(Entity):
    def __init__(self, x, y, color=(255, 0, 0)):
        super().__init__(
            Vector2(x, y),
            "platform",
            0,
            {
                "rect": (16, 4),
                "gravity": 0,
                "use_collisions": False,
                "useGravity": False,
            },
        )
        self.width = 16
        self.height = 4
        self.color = (255, 0, 0)
        self.imageOffset.update(0, 0)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)

        self.__points = [
            Vector2(self.rect.left, self.rect.bottom),
            Vector2(self.rect.right, self.rect.bottom),
            Vector2(self.rect.right, self.rect.bottom),
            Vector2(self.rect.right, self.rect.top),
        ]

    #  _________________________________
    # |                                 |
    # |                                 |
    # ------X----------------------------
    #       |                     |
    #    |                     |
    #  |                     |
    #  Y                     |
    def update_points(self):
        occupiedTile = game.tileMap.getTileScreen(
            tupleToVector((self.rect.centerx, self.rect.bottom + 16))
        )
        x, y = (
            (occupiedTile[0] * game.tileMap.tileSize),
            occupiedTile[1] * game.tileMap.tileSize,
        )
        # print(occupiedTile, x, y)
        self.__points[0].update(
            self.rect.left + 2 + self.game.camera.x,
            self.rect.bottom + 1 + self.game.camera.y,
        )
        self.__points[1].update(
            self.rect.right + self.game.camera.x,
            max(
                self.rect.bottom + 2,
                self.rect.bottom
                - ((self.rect.bottom - y) / 2)
                - 0.5
                + self.game.camera.y,
            ),
        )
        self.__points[2].update(
            self.rect.right + self.game.camera.x,
            max(
                self.rect.bottom + 4,
                self.__points[1].y + 2,
            ),
        )
        # print(self.__points[0])
        self.__points[3].update(x + self.game.camera.x, y + self.game.camera.y)
        # print(self.__points[1])

    def update(self, delta, tick):
        self.position.y += 0.25
        super().update(delta, tick)

    def draw(self, surface):
        super().draw(surface)
        self.update_points()
        # print(self.__points[0])
        pygame.draw.lines(
            surface,
            (0, 255, 0),
            False,
            self.__points,
            1,
        )
