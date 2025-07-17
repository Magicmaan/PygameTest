from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from Engine.background.generator import generateBackgroundDetails

if TYPE_CHECKING:
    from Engine.Program import Program
import pygame


class BackgroundManager:
    def __init__(self, game: Program, BGSequence={}):
        self.game = game

        default_background = [
            pygame.image.load(Path.cwd() / "Resources" / "background0.png").convert(),
            pygame.image.load(Path.cwd() / "Resources" / "background1.png").convert(),
            pygame.image.load(Path.cwd() / "Resources" / "background2.png").convert(),
        ]
        default_background[0].set_colorkey((0, 0, 0))
        default_background[1].set_colorkey((0, 0, 0))
        default_background[2].set_colorkey((0, 0, 0))

        self.background: list[dict[str, int | pygame.Surface]] = [
            {"texture": default_background[0], "offset": 0},
            {"texture": default_background[1], "offset": 0},
            {"texture": default_background[2], "offset": 0},
        ]

        # TODO
        # background_detail = generateBackgroundDetails(
        #     width=game.renderer.width,
        #     height=game.renderer.height,
        # )
        # self.addBackground(
        #     background_detail["texture"],
        #     offset=0,
        # )

    def addBackground(self, bg, offset=0):
        self.background.append({"texture": bg, "offset": offset})

    def draw(self, surface: pygame.Surface):
        for background in self.background:
            bg = background["texture"]
            if background["offset"]:
                offset: int = background["offset"]
                camOffsetX = self.game.camera.x

                surface.blit(bg, (camOffsetX, 0))
                surface.blit(bg, (camOffsetX, 0))
                surface.blit(bg, (camOffsetX, 0))
            else:
                surface.blit(bg, (0, 0))
