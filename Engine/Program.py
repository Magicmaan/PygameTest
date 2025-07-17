from __future__ import annotations
import time


import pygame
import moderngl
from Engine import TextGUI
from Engine.debug.logger import Logger
from Engine.renderer import PygameRenderer
from Engine.renderer.renderer import GLPoint, GLRenderer
from Engine.tilemap import TileMapHandler
from Engine.Raycaster import Raycaster, Ray
from Engine.Camera import Camera
from Engine.InputHandler import InputHandler
from Engine.SettingsClass import Settings
from Engine.debug.Debugger import Debugger
from Engine.TextureHandler import TextureHandler
from Engine.ParticleHandler import ParticleHandler
from Engine.background.background import BackgroundManager
from Engine.GUIHandler import GUIHandler
from Engine.util.vector import toVector
from Engine.util import Vector2

# gInput = InputHandler()  # initialise input handler


class Program:
    _instance = None

    pause_start_event_id: int = pygame.event.custom_type()
    pause_end_event_id: int = pygame.event.custom_type()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Program, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.logger = Logger("Program")
        self.input = InputHandler(self)  # get input handler instance
        # self.input.update()
        settings = Settings(self)

        self.output_resolution = Vector2(
            settings.windowWidth,
            settings.windowHeight,
        )  # setup Window
        self.resolution = Vector2(settings.gameWidth, settings.gameHeight)
        self.renderer = GLRenderer(
            toVector(self.resolution), toVector(self.output_resolution)
        )

        # self.screenOutput = pygame.display.set_mode(
        #     self.output_resolution, pygame.NOFRAME
        # )
        # self.screen = pygame.Surface(self.resolution)

        # print("Key Repeat val: " + str(pygame.key.get_repeat()))

        pygame.key.set_repeat(500, 500)

        self.afkTimer = 36000
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.TimeMult = 1
        self.tick = 0

        self.camera = Camera(self)

        # scripts group
        self.scripts: list[object] = []

        # Sprite Groups
        self.allSprites = pygame.sprite.Group()
        self.PhysSprites = pygame.sprite.Group()
        self.allObjects = pygame.sprite.Group()
        self.wallColliders = pygame.sprite.Group()
        self.floorColliders = pygame.sprite.Group()
        self.debugGroup: pygame.sprite.Group = pygame.sprite.Group()

        self.textures = TextureHandler()
        self.font = TextGUI.initFont()
        self.background = BackgroundManager(self)
        self.GUI = GUIHandler(self)

        self.tilemap: TileMapHandler = TileMapHandler(self)

        self.particles = ParticleHandler(self)
        self.particles.add(Vector2(20, 20), "balls")

        self.raycaster = Raycaster(self)

        self.debugger = Debugger(
            self, self.renderer.render_layers["debug"], True, True, True
        )

        self.renderer.add_group_to_layer(self.background, "background")
        self.renderer.add_group_to_layer(self.tilemap, "background")
        self.renderer.add_group_to_layer(self.allObjects, "foreground")
        self.renderer.add_group_to_layer(self.allSprites, "foreground")
        self.renderer.add_group_to_layer(self.wallColliders, "foreground")
        self.renderer.add_group_to_layer(self.floorColliders, "foreground")

        self.renderer.add_group_to_layer(self.allSprites, "particles")

        self.renderer.add_group_to_layer(self.particles, "particles")
        self.renderer.add_group_to_layer(self.GUI, "GUI")
        self.renderer.add_group_to_layer(self.debugger, "debug")

    def update(self):
        events = pygame.event.get()
        self.input.update(events)

        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.stop()
                case Program.pause_start_event_id:
                    print("Pause Start")
                    print("*" * 100)

        self.allObjects.update(self.dt, self.tick)
        self.allSprites.update(self.dt, self.tick)
        self.raycaster.update()

        [script.update(self, self.dt, self.tick) for script in self.scripts]

        self.camera.update(self.dt, self.tick)
        self.GUI.update(self)

        self.dt = (self.clock.tick(self.renderer.framerate) / 1000) * self.TimeMult
        if self.dt < (1 / self.renderer.framerate):
            time.sleep((1 / self.renderer.framerate) - self.dt)
        self.tick += 1

    def draw(self):
        self.renderer.draw()
        return
        self.screen.fill("gray")
        for i, layer in self.renderLayers.items():
            layer.fill((0, 0, 0))

        self.background.draw(self.renderLayers["Background"])

        self.drawGroup(self.allObjects, self.renderLayers["Foreground"])
        # draw all Sprites to Foreground
        self.drawGroup(self.allSprites, self.renderLayers["Foreground"])

        self.tileMap.draw(
            self.renderLayers["Foreground"],
        )
        self.particles.draw(self.renderLayers["Particles"])
        self.GUI.draw(self.renderLayers["GUI"])

        # Draw the layers in order
        self.screen.blit(self.renderLayers["Background"], (0, 0))
        self.screen.blit(self.renderLayers["Foreground"], (0, 0))
        self.screen.blit(self.renderLayers["Particles"], (0, 0))
        self.screen.blit(self.renderLayers["GUI"], (0, 0))

        frame = pygame.transform.scale(
            self.screen, self.output_resolution
        )  # output to frame and draw to screen
        self.screenOutput.blit(frame, frame.get_rect())
        self.debugger.draw("1")

        pygame.display.flip()

        # self.renderer.draw()

    def setMap(self, tileMap: TileMapHandler):
        self.tileMap = tileMap

    def stop(self):
        self.running = False

        # save settings

        # exit window and close pygame
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()

    def drawGroup(self, group, surface):
        for spr in group.sprites():
            if hasattr(spr, "draw"):
                spr.draw(surface)
