import pygame

from Engine import Program
from Engine.SettingsClass import Settings
from Engine.debug.Debugger import Debugger
from Engine.InputHandler import InputHandler


widgets = {
    "Text": {},
    "Button": {},
}


class GUIWidget:
    def __init__(self, namespace, rect, widget="button", WidgetSettings={}):
        pass

    def update(self, game):
        pass

    def draw(self, surface):
        if not self.active:
            return

    def getValue(self):
        pass

    def _onHover(self):
        pass

    def _onClick(self):
        if self.action:
            result = self.action()


class Button(GUIWidget):
    # define button with x,y,width,height, content, and type
    # type can be toggle button or normal button
    # _getValue is the output endpoint to get state
    def __init__(self, text, color, border, action, type="toggle", anim={}) -> None:
        self.type = type

    def update(self, game):
        pass

    def draw(self, surface):
        pass

    def _Hover(self, state):
        pass

    def _isClicked(self):
        pass

    def _toggleButton(self):
        pass

    def getValue(self):
        pass


class Slider(GUIWidget):
    # take in list or dict of values which can be selected between
    def __init__(self) -> None:
        pass

    def update(self, game):
        pass

    def draw(self, surface):
        pass

    def _getValue(self):
        pass


class GUI:
    # GUI interface to add / move
    # GUI will be its own surface
    # interaction, will look for collision within rect before doing further stuff
    def __init__(self, rect, elements=[]):
        self.elements = elements
        self.active

    def addElem(self, element, x, y):
        self.elements.append(element)
        pass

    def removeElem(self, namespace):
        # take in element namespace to remove
        pass

    def update(self, game):
        pass

    def draw(self, surface):
        if not self.active:
            return

    def _getElementStates(self):
        pass

    def _getElementState(self, namespace):
        pass


class GUIHandler:
    def __init__(self, game):
        self.active = True
        self.game = game
        self.menus = {}
        self.currentMenu = "inventory"

    def update(self, game):
        if self.game.input.key(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(self.game.pause_start_event_id))
            print("Pause End")
            self.active = not self.active

    def draw(self, surface):
        if not self.active:
            surface.fill((0, 0, 0, 0))
            return

        surface.fill((1, 1, 1, 100))
