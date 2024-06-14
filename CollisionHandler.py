import pygame


angleSurfaceHeights = {
    0 : (0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5),  #12 degree
    1 : (0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7), #22 degree
    2 : (0,1,2,3,4,5,6,7,9,10,11,12,13,14,15), #45 degree
    3 : (1,3,5,7,9,11,13,15,15,15,15,15,15,15,15,15) #75 degree


}

def slopeResolve(spr,rect,obj,slope):
    spr.collisions["down"] = True
    spr.onGround = True

    if spr.velocity.y >= 0:
        spr.velocity.y = 0

    leftCenter = obj.rect.collidepoint(pygame.Vector2(rect.centerx+2,rect.centery))
    rightCenter = obj.rect.collidepoint(pygame.Vector2(rect.centerx-2,rect.centery))
    if leftCenter and rightCenter:
        
        #get just subpixel of tile user is on
        digitConvert = ((spr.position.x + spr.rect.width/2) % 16)
        
        spr.position.y = obj.rect.bottom - slope[int(digitConvert)]-1 - spr.rect.height
    else:
        if spr.rect.left < obj.rect.left:
            spr.position.y = obj.rect.bottom - slope[0] - spr.rect.height
        elif spr.rect.right > obj.rect.right:
            spr.position.y = obj.rect.bottom - slope[-1] - spr.rect.height  


def objectCollideResolve(spr,rect,obj):
    colPoint = obj.rect.collidepoint
    isSlope = False
    if obj.angle == 12:
        slope = angleSurfaceHeights[0]
        isSlope = True
    elif obj.angle == 22:
        slope = angleSurfaceHeights[1]
        isSlope = True
    elif obj.angle == 45:
        slope = angleSurfaceHeights[2]
        isSlope = True
    if isSlope:
        if obj.flip:
            slope = tuple(reversed(slope))
        slopeResolve(spr,rect,obj,slope)
        return
    
    collideResolve(spr,rect,obj.rect)
        

def collideResolve(spr,sprRect,objRect):
    colPoint = objRect.collidepoint

    if colPoint(sprRect.midbottom) or colPoint((sprRect.left + 1, sprRect.bottom)) or colPoint((sprRect.right - 1, sprRect.bottom)):
        spr.collisions["down"] = True
        spr.onGround = True
        spr.position.y = objRect.top - spr.rect.height
        if spr.velocity.y > 0:
            spr.velocity.y = 0
    
    elif colPoint(sprRect.midtop) or colPoint((sprRect.left + 1, sprRect.top)) or colPoint((sprRect.right - 1, sprRect.top)):
        spr.collisions["up"] = True
        spr.position.y = objRect.bottom  # Adjust the position to be exactly below the collider
        spr.velocity.y = 0  # Stop vertical velocity
    
    # Check horizontal collisions (left and right)
    elif colPoint(sprRect.midleft) or colPoint((sprRect.left, sprRect.top + 2)) or colPoint((sprRect.left, sprRect.bottom - 4)):
        spr.collisions["left"] = True
        spr.position.x = objRect.right
        if spr.velocity.x < 0:
            spr.velocity.x = 0
        
    elif colPoint(sprRect.midright) or colPoint((sprRect.right, sprRect.top + 2)) or colPoint((sprRect.right, sprRect.bottom - 4)):
        spr.collisions["right"] = True
        spr.position.x = objRect.left - spr.rect.width
        if spr.velocity.x > 0:
            spr.velocity.x = 0



def collideTest(rect,objs):
    objectCollisions=[]
    #rect is x,y,width,height
    #objs is list of objects (or groups)
    #colliderect tests for intersection between rect and each obj rect in group
    for obj in objs:
        if rect.colliderect(obj.rect):
            objectCollisions.append(obj)
    
    

    return objectCollisions

def collideUpdate(spr,collideGroup,tileMap):
    # Check for collisions between the two groups on next movement
    #collisions = pygame.sprite.groupcollide(self.game.PhysSprites, self.game.floorColliders, False, False)
    futureRect = spr.rect.copy()
    futureRect.update(spr.position.x+round(spr.velocity.x,2),spr.position.y+round(spr.velocity.y*1.1,2),spr.rect[2], spr.rect[3])
    #get collisions
    

    tileCollisions = tileMap.getTileAround(futureRect)
    if tileCollisions:
        for tile in tileCollisions:
            collideResolve(spr,futureRect,tile)

    #objectCollisions = collideTest(futureRect,collideGroup)
    #if their are collisions
    #if objectCollisions:
    #    for obj in objectCollisions:
    #        objectCollideResolve(spr,futureRect,obj)

            
            
            
            