import pygame
import time
import os.path
from Engine import TextFont
from Engine.TextureHandler import TextureHandler
from Engine.util.vector import Vector2, Vector3

Texture = TextureHandler()


if not pygame.font.get_init():
    pygame.font.init()

fontFile = "Resources/PixeloidMono.ttf"
size = 16

global FONT
global FONT_SMALL
FONT = pygame.font.Font(fontFile, size)
FONT_SMALL = pygame.font.Font(fontFile, 8)


sequence = (
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "?",
    "!",
    ".",
    ",",
    ":",
    ";",
    '"',
    "(",
    ")",
    '"',
    "/",
    "-1",
    "-1",
    "%",
    "-",
    "+",
    "*",
    "=",
    "<",
    ">",
    "-1",
    "-1",
    "-1",
    "-1",
    "-1",
    "-1",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
)

widthModifiers = {
    "M": (5, 7),
    "m": (5, 7),
    "l": (3, 7),
    ":": (3, 7),
    ";": (3, 7),
    ".": (3, 7),
    ",": (3, 7),
}

cursorpos = [0, 0]


def initFont():
    # font array size
    fontSize = (5, 7)

    fontSurfaces = {}
    fontSurfaces["Blank"] = pygame.Surface(fontSize)
    fontSurfaces["Blank"].set_colorkey((0, 0, 0))

    Texture.load_texture("TextFont", fontSize)

    pos = 0
    for char in sequence:
        img = Texture.texture("TextFont", pos)

        rect = pygame.Rect(0, 0, 4, 7)
        if char in widthModifiers:
            rect = pygame.Rect((0, 0), widthModifiers[char])
        img = pygame.Surface((rect.width, rect.height))
        img.blit(Texture.texture("TextFont", pos), (0, 0), rect)
        img.set_colorkey((0, 0, 0))

        fontSurfaces[char] = img

        pos += 1

    return fontSurfaces

    # constructs surfaces for font from array of pixels
    for letter, array in TextFont.letters.items():
        surface = pygame.Surface((fontSize, fontSize))
        surface.fill((0, 0, 0, 0))
        surface.set_colorkey((0, 0, 0))

        for y in range(len(array)):
            for x in range(len(array[0])):
                if array[y][x] == 1:
                    surface.set_at((x, y), (255, 255, 255, 255))

        fontSurfaces[letter] = surface
        print("Added letter: " + letter)

    return fontSurfaces


def write_debug(
    text,
    surface: pygame.Surface,
    position=[0, 0],
    color=(255, 255, 255, 255),
    size="normal",
):
    font = FONT if size == "normal" else FONT_SMALL

    image = font.render(text, False, color)

    # apply tint
    image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    image.set_alpha(color[3] if len(color) == 4 else 255)

    surface.blit(image, [position[0], position[1]])


def write_vector_debug(
    vector: Vector2 | Vector3,
    surface,
    position=[0, 0],
    color=(255, 255, 255, 255),
):
    text = f"X: {vector.x:.2f} Y: {vector.y:.2f}"
    if isinstance(vector, Vector3):
        text += f" Z: {vector.z:.2f}"

    write_debug(text, surface, position, color)


def write(text, surface, position, font, color=(0, 255, 0), scale=1):
    if scale < 1:
        scale = 1
    scale = round(scale, 0)
    x_offset = 0

    for char in text:
        image = font["Blank"]
        if char in font.keys():
            image = font[char]

        if scale != 1:
            image = pygame.transform.scale_by(image, scale)

        image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(image, (position[0] + (x_offset * scale), position[1]))

        x_offset += image.get_width() / scale + 1
