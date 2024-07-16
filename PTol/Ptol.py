import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    def update(self,game):
        pass


class PhysObject(Object):
    def __init__(self,position,texture,):
        pass

    def update(self,game):
        self._physupdate(game)

        super().update(game)

    
    def draw(self,surface):
        pass

    def _physupdate(self,game):
        pass

class PortalObject(Object):
    def __init__(self):
        super().__init__()
    

    def update(self,game):
        pass

    def _portalTeleport(self,Object):
        pass

    def collideCheck(self,object):
        pass