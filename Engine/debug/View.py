from functools import cache
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image
import pygame

from typing import Dict, Any, Tuple


class SurfaceViewer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SurfaceViewer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self._init()

    def _init(self):
        # Initialize your singleton instance here
        pass

    # memoise so same surface can't be shown multiple times
    # this is a bit of a hack, but it works. nah this is a good idea
    @cache
    def show_surface(self, surface: pygame.Surface, title: str = "Surface"):
        """
        Display a pygame surface in a new window using PIL.
        """
        # Convert the pygame surface to a PIL image
        mode = "RGBA" if surface.get_bytesize() == 4 else "RGB"
        data = pygame.image.tobytes(surface, mode)
        size = surface.get_size()
        image = Image.frombytes(mode, size, data)

        ax, fig = plt.subplots()

        fig.imshow(np.array(image))
        fig.axis("off")
        plt.title(title)
        plt.pause(0.001)
        plt.show(block=False)
