import pygame



def defaultCalc(particle,particlemodifiers):
    
    print("default calc")


def scaleDecayCalc(particle,particlemodifiers):
    if particlemodifiers["scaleDecay"]:
        particle[0] = pygame.transform.scale_by(particle[0],particlemodifiers["scaleDecay"])
