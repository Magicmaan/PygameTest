import pygame


class RenderLayer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.resolution = (width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw(self, surface: pygame.Surface):
        pass

    def process(self):
        pass
