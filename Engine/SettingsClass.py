import pygame
import re
import os.path
from Engine.InputHandler import InputHandler
gameInput = InputHandler()


def toInt(var):
    try:
        # Try converting the variable to an integer
        return int(var)
    except (ValueError, TypeError):
        return var



class Settings:
    def __init__(self,filepath='Engine/Settings.txt'):
        self.settings = {}
        
        if not os.path.isfile(filepath):
            file = open(filepath,"w")
        else:
            file = open(filepath,"r")
        
        
        
        category = ""
        for line in file:
            line = line.replace('\n','')
            if line == "[General]":
                
                category = "general"
                print(category + " Settings")
                continue
            if line == "[Keybinds]":
                category = "keybinds"
                print(category + " Settings")
                continue
            
            
            
            parts = re.split(r'[= ]+', line)
            if len(parts) != 2:
                continue
            
            if category == "general":
                settingsName = parts[0]
                settingsValue = parts[1]
                setattr(self,settingsName,toInt(settingsValue))
                    
            if category == "keybinds":
                keyLink = parts[0]
                keyName = parts[1]
                print(parts)
                gameInput.newControl(keyLink,keyName)
        
            

            
            
        file.close()
        
        