from functools import cache
import pygame
import math
from typing import Literal
import random


def round_to_nearest(value: float, step: float, zero: bool = False) -> float:
    """
    Rounds a value to the nearest multiple of a step.

    Args:
        value (float): The value to round.
        step (float): The step size.
        zero (bool): If True, allows rounding to zero. Default is False.

    Returns:
        float: The rounded value.
    """
    pre_val = value / step
    # if zero is true, don't allow for rounding to zero
    # i.e. if the value is 0, set it to step with
    if not zero:
        if abs(pre_val) < step:
            pre_val = math.copysign(step, pre_val)

    val = round(pre_val) * step

    return val


def fill_bordered(
    surface: pygame.Surface,
    color: tuple[int, int, int],
    rect: tuple[int, int, int, int],
    width: int = 1,
):
    # Fill the rectangle minus the border
    modified_rect = (
        rect[0] + width,
        rect[1] + width,
        rect[2] - (width * 2),
        rect[3] - (width * 2),
    )
    pygame.draw.rect(
        surface,
        color,
        modified_rect,
    )


def rect(
    surface: pygame.Surface,
    color: tuple[int, int, int],
    rect: tuple[int, int, int, int],
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
) -> pygame.Rect:
    """
    Draws a rectangle on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw on.
        color (tuple[int, int, int]): The color of the rectangle.
        rect (tuple[int, int, int, int]): The rectangle's position and size (x, y, width, height).
        width (int): The width of the rectangle's outline. Default is 0 for a filled rectangle.
        border_radius (int): The radius of the rectangle's corners. Default is -1 for no rounding.
        border_top_left_radius (int): The radius of the top-left corner. Default is -1 for no rounding.
        border_top_right_radius (int): The radius of the top-right corner. Default is -1 for no rounding.
        border_bottom_left_radius (int): The radius of the bottom-left corner. Default is -1 for no rounding.
        border_bottom_right_radius (int): The radius of the bottom-right corner. Default is -1 for no rounding.

    Returns:
        pygame.Rect: The rectangle that was drawn.
    """
    return pygame.draw.rect(
        surface,
        color,
        rect,
        width=width,
        border_radius=border_radius,
        border_top_left_radius=border_top_left_radius,
        border_top_right_radius=border_top_right_radius,
        border_bottom_left_radius=border_bottom_left_radius,
        border_bottom_right_radius=border_bottom_right_radius,
    )


def hollow_rect(
    surface: pygame.Surface,
    rect: tuple[int, int, int, int],
    color: tuple[int, int, int] = (0, 0, 255),
    line_width: int = 1,
) -> pygame.Rect:
    """
    Draws a hollow rectangle on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw on.
        color (tuple[int, int, int]): The color of the rectangle.
        rect (tuple[int, int, int, int]): The rectangle's position and size (x, y, width, height).
        width (int): The width of the rectangle's outline.

    Returns:
        pygame.Rect: The rectangle that was drawn.
    """
    x, y, width, height = rect

    pygame.draw.rect(
        surface,
        color,
        (
            x,
            y,
            width,
            height,
        ),
        line_width,
    )


@cache
def __small_1() -> pygame.Surface:
    s = pygame.Surface((4, 4))
    pixels = [
        (0, 0),  # outer points
        (3, 0),
        (0, 3),
        (3, 3),
        (1, 1),  # inner points
        (2, 1),
        (1, 2),
        (2, 2),
    ]
    s.fill((0, 0, 0))

    for pixel in pixels:
        s.set_at(pixel, (255, 0, 0))
    return s


@cache
def __small_2() -> pygame.Surface:
    s = pygame.Surface((4, 4))
    pixels = [
        (1, 1),
        (2, 2),
    ]
    s.fill((255, 0, 0))

    for pixel in pixels:
        s.set_at(pixel, (0, 0, 0))
    return s


def __small_hollow(width=1) -> pygame.Surface:
    s = pygame.Surface((8, 8))
    hollow_rect(s, (1, 1, 6, 6), (255, 0, 0), width)
    return s


def __medium_hollow(width=1) -> pygame.Surface:
    s = pygame.Surface((12, 12))
    hollow_rect(s, (1, 1, 10, 10), (255, 0, 0), width)
    return s


def __large_hollow(width=1) -> pygame.Surface:
    s = pygame.Surface((16, 16))
    hollow_rect(s, (1, 1, 14, 14), (255, 0, 0), width)
    return s


def draw_gear(
    surface: pygame.Surface,
    x: int,
    y: int,
    size: int = 16,
):
    """
    Draws a gear shape on the given surface at the specified coordinates.

    Args:
        surface (pygame.Surface): The surface to draw on.
        x (int): The x-coordinate of the center of the gear.
        y (int): The y-coordinate of the center of the gear.
    """
    # # Placeholder for actual gear drawing logic
    # pygame.draw.rect(
    #     surface, (255, 0, 0), (x, y, size, size), 50
    # )  # Example: draw a red circle

    x = x - size // 2
    y = y - size // 2

    surface.blit(__large_hollow(2), (x, y))
    small_gear_1 = __small_1()
    small_gear_2 = __small_2()
    surface.blit(
        small_gear_2,
        (
            x + size - small_gear_2.get_width() - 4,
            y + size - small_gear_2.get_height() - 4,
        ),
    )
    surface.blit(
        small_gear_1,
        (
            x + 4,
            y + 4,
        ),
    )


def cable(
    surface: pygame.Surface,
    x: int,
    y: int,
    direction: Literal["up", "down", "left", "right"] = "up",
    width: Literal[1, 2, 4] = None,
):
    """
    Draws a cable shape on the given surface at the specified coordinates.

    Args:
        surface (pygame.Surface): The surface to draw on.
        x (int): The x-coordinate of the center of the cable.
        y (int): The y-coordinate of the center of the cable.
    """
    cable_length = 32
    cable_width = random.choices(
        [1, 2, 4],
        weights=[5, 2, 1],
    )[0]
    if width is not None:
        cable_width = width

    lines = [(x, y), (x, y)]
    #
    vertical_count = 0
    horizontal_count = 0

    # default direction is up
    horiz_h_range = 8
    horiz_l_range = -8
    vert_h_range = -2
    vert_l_range = -16

    match direction:
        case "up":
            pass
        case "down":
            vert_h_range = abs(vert_l_range)
            vert_l_range = abs(vert_h_range)
        case _:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    for i in range(0, cable_length):
        previous = lines[i]

        is_horizontal = random.choices(
            [True, False],
            weights=[max(1, 8 - horizontal_count), max(1, 4 - vertical_count)],
        )[0]

        if is_horizontal:
            horizontal_count += 1
            vertical_count = 0
        else:
            vertical_count += 1
            horizontal_count = 0

        x_offset = previous[0]
        y_offset = previous[1]

        if is_horizontal:
            x_offset += round_to_nearest(
                random.randint(horiz_l_range, horiz_h_range), 8, zero=True
            )
        else:
            y_offset += round_to_nearest(
                random.randint(vert_l_range, vert_h_range), 8, zero=True
            )

        lines.append((x_offset, y_offset))

    pygame.draw.lines(surface, (0, 0, 0), False, lines, cable_width + 2)
    offset_lines = [(x + cable_width // 2, y + cable_width // 2) for x, y in lines]
    pygame.draw.lines(surface, (255, 0, 0), False, offset_lines, cable_width)
    # amount_y = round_to_nearest(math.pow(random.randint(-16, 16), 2), 8)

    # pygame.draw.line(
    #     surface,
    #     (255, 0, 0),
    #     (x, y),
    #     (x, y - amount_y),
    #     2,
    # )


def generateBackgroundDetails(
    width: int,
    height: int,
) -> dict[str, int | pygame.Surface]:
    """
    Generates the background details for the game.

    Args:
        width (int): The width of the background.
        height (int): The height of the background.

    Returns:
        dict[str, int | pygame.Surface]: A dictionary containing the background details.
    """
    texture = pygame.Surface((width, height))
    texture.fill((0, 0, 0))  # Placeholder for actual background texture

    cable(
        texture,
        width // 2,
        height // 2,
        direction="up",
    )  # Draw a cable shape in the center of the background

    cable(
        texture,
        width // 2,
        height // 2,
        direction="up",
    )  # Draw a cable shape in the center of the background

    cable(
        texture,
        width // 2,
        height // 2,
        direction="down",
    )  # Draw a cable shape in the center of the background

    cable(
        texture,
        width // 2,
        height // 2,
        direction="down",
    )  # Draw a cable shape in the center of the background

    cable(
        texture,
        width // 2,
        height // 2,
        direction="down",
    )  # Draw a cable shape in the center of the background

    draw_gear(
        texture,
        width // 2,
        height // 2,
    )  # Draw a gear shape in the center of the background
    # Placeholder for actual background generation logic
    return {
        "width": width,
        "height": height,
        "texture": texture,
    }
