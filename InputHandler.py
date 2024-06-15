import pygame



class InputHandler:
    #creates one unique instance
    _inputInstance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._inputInstance:
            cls._inputInstance = super(InputHandler, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._inputInstance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.keymap = {}
        self.mods = {}
        self.controls = {}
        self.keyTimer = {}

        
    

    def getMouse(self):
        #to be added
        pass
    
    


    def key(self,key):
        #get individual key input
        #takes in pygame consts i.e. "K_CTRL"
        #retrieves attribribute in pygame
        #gets from keymap
        if not self.keymap:
            self.pollInput()
        
        return self.keymap[getattr(pygame, key)]
    
            
    def newControl(self,keyLink,keyName):
        self.controls[keyLink] = keyName
        
        def controlFunction():
            return self.key(self.controls[keyLink])
        
        setattr(self, keyLink, controlFunction)
    
    def pollInput(self):
        #get raw inputs from keyboard
        self.keymap = pygame.key.get_pressed()
        self.mods = pygame.key.get_mods()
        
        
    def L_CTRL(self):
        if self.mods == pygame.KMOD_LCTRL:
            return True
        return False
    
    def L_SHIFT(self):
        if self.mods == pygame.KMOD_LSHIFT:
            return True
        return False
    
    def L_ALT(self):
        if self.mods == pygame.K_LALT:
            return True
        return False
        
    