from __future__ import annotations
from typing import TYPE_CHECKING
from Engine.debug.logger import Logger
from Engine.util import Vector2
from Engine.util.math import minmax

if TYPE_CHECKING:
    from Engine.Program import Program

from Engine.debug.logger import Logger
import pygame


class Mouse:
    def __init__(self, game: Program):
        self.game = game

        self.leftClick = False
        self.rightClick = False
        self.middleClick = False
        self.scrollUp = False
        self.scrollDown = False
        self.position = Vector2(0, 0)
        self.positionWorld = Vector2(0, 0)
        self.delta = Vector2(0, 0)

    def update(self):
        # get mouse inputs
        self.leftClick = pygame.mouse.get_pressed()[0]
        self.rightClick = pygame.mouse.get_pressed()[2]
        self.middleClick = pygame.mouse.get_pressed()[1]
        self.mousePosition = Vector2(pygame.mouse.get_pos())
        self.mousePositionWorld = self.getMousePositionWorld()

        self.delta = pygame.mouse.get_rel()
        self.position = pygame.mouse.get_pos()
        self.positionWorld = self.getMousePositionWorld()

    def getMousePositionWorld(self) -> Vector2:
        # get mouse position in world space
        # get mouse position in screen space
        # convert to world space using camera
        screenPos = self.mousePosition.copy()
        screenPos.x = screenPos.x / self.game.camera.render_ratio.x
        screenPos.y = screenPos.y / self.game.camera.render_ratio.y

        screenPos.x -= self.game.camera.position.x
        screenPos.y -= self.game.camera.position.y

        # screenPos += self.game.camera.position  # add camera position to screen pos
        # convert to world space using camera

        return screenPos


class InputHandler:
    # creates one unique instance
    _inputInstance = None

    def __new__(cls, *args, **kwargs):
        if not cls._inputInstance:
            cls._inputInstance = super(InputHandler, cls).__new__(cls)
            cls._initialized = False
        return cls._inputInstance

    def __init__(self, game: Program):
        if self._initialized:
            return
        # assert game is not None, "Game instance must be provided."

        self._initialized = True
        self.game = game
        self.keymap = {}
        self.mods = {}
        self.controls = {}
        self.keyTimer = {}
        self.UserInput = True
        self.logger = Logger("InputHandler")

        # key, state
        self.last_input: list[tuple[int, int]] = []  # list of tuples of key and state
        # 1 = down, 0 = up
        self.last_input.append((0, 0, 0))
        self.mouse = Mouse(self.game)  # create mouse object

    @classmethod
    def getInstance(cls):
        if cls._inputInstance is None:
            raise Exception("InputHandler instance not created yet.")
        return cls._inputInstance

    def setGame(self, game):
        self.game = game

    def key(self, key: pygame.key):
        k = self.keymap.get(key, False)
        if k:
            has_already_pressed = None
            # try for down state / just pressed
            try:
                has_already_pressed = self.last_input.index((key, 1))
            except ValueError:
                has_already_pressed = None

            # try for up state / just released
            try:
                has_already_pressed = self.last_input.index((key, 0))
            except ValueError:
                has_already_pressed = None

            if has_already_pressed is None:
                return key
            else:
                l = len(self.last_input)

                if has_already_pressed > minmax(0, 3, l):
                    return key
                return False

        return False

    def key_raw(self, key: pygame.key):
        # get individual key input
        # takes in pygame consts i.e. "K_CTRL"
        # retrieves attribribute in pygame
        # gets from keymap
        if not self.keymap:
            return False

        output = False
        try:
            output = self.keymap.get(key, False)
        except AttributeError:
            self.logger.warning(f"Key {key} not found in keymap.")
            return False
        return output

    def newControl(self, keyLink, keyName):
        self.controls[keyLink] = keyName

        def controlFunction():
            return self.key(self.controls[keyLink])

        setattr(self, keyLink, controlFunction)

    def update(self, event_queue):
        # self.logger.debug("Updating input handler")
        for event in event_queue:
            if event.type == pygame.QUIT:
                self.game.stop()
                return

            # check for key down events
            if event.type == pygame.KEYDOWN:

                key_name = pygame.key.name(event.key)
                self.keymap[event.key] = True

                self.last_input.append((event.key, 1))

                print(f"Key pressed: {key_name}")
                self.logger.debug(f"Key pressed: {event.key}")

            if len(self.last_input) > 10:
                self.last_input.pop(
                    0
                )  # remove the first element to keep the list size constant
            if len(self.last_input) > 0:
                if self.game.tick % 10 == 0:
                    self.logger.debug(f"Last input: {self.last_input}")
                    self.last_input.pop(
                        0
                    )  # remove the first element to keep the list size constant
            # check for key up events
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.keymap[event.key] = False
                self.last_input.append((event.key, 0))
                if len(self.last_input) > 3:

                    self.last_input.pop(0)

                print(f"Key released: {key_name}")
                self.logger.debug(f"Key released: {key_name}")

        # get raw inputs from keyboard
        # self.keymap = pygame.key.get_pressed()
        self.mods = pygame.key.get_mods()
        self.mouse.update()  # update mouse inputs

    def getMouse(self):
        return self.mouse

    def CTRL(self):
        return (
            self.keymap[getattr(pygame, "K_LCTRL")]
            or self.keymap[getattr(pygame, "K_RCTRL")]
        )

    def SHIFT(self):
        return (
            self.keymap[getattr(pygame, "K_LSHIFT")]
            or self.keymap[getattr(pygame, "K_RSHIFT")]
        )

    def ALT(self):
        return (
            self.keymap[getattr(pygame, "K_LALT")]
            or self.keymap[getattr(pygame, "K_RALT")]
        )

    def leftClick(self):
        isPressed = pygame.mouse.get_pressed()[0]

        if isPressed:
            return {
                "pressed": True,
                "screenPosition": self.getMousePosition(),
                "worldPosition": self.getMousePositionWorld(),
                "button": 1,
            }
        else:
            return {
                "pressed": False,
                "screenPosition": self.getMousePosition(),
                "worldPosition": self.getMousePositionWorld(),
                "button": 1,
            }

    def rightClick(self):
        return pygame.mouse.get_pressed()[2]
