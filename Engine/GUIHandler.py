import pygame

from Engine.SettingsClass import Settings
from Engine.Debugger import Debugger
from Engine.InputHandler import InputHandler
gInput = InputHandler() #initialise input handler



class GUIHandler:
    def __init__(self,game):
        pass

        self.active = False
        self.game = game
        self.menus = {}
        self.currentMenu = "inventory"
    
    

    def update(self,game):
        if gInput.escape():
            self.active = not self.active
        if not self.active:
            self.game.TimeMult = 1
            return

        game.TimeMult = 0.5

    def draw(self,surface):
        if not self.active:
            surface.fill((0,0,0,0))
            return
        
        surface.fill((1,1,1,100))