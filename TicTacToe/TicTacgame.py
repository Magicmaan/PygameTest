import pygame


class TicTac:
    def  __init__(self,outputScreen,scale,pos):
        self.screen = outputScreen
        self.scaleFactor = 1
        self.grid = [0,0,0,2,0,1,1,2,1]
        self.gameScreen = pygame.Surface((300,300))
        self.gamePosition = pos

        self.cross = pygame.transform.scale(pygame.image.load("TicTacToe/cross.png"),(self.gameScreen.get_width()//3,self.gameScreen.get_width()//3))
        self.circle = pygame.transform.scale(pygame.image.load("TicTacToe/circle.png"),(self.gameScreen.get_width()//3,self.gameScreen.get_width()//3))

        

    def update(self,gridPos=False,move=1):
        if not gridPos:
            mouse = pygame.mouse.get_pos()
            rect = self.gameScreen.get_rect()
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse):
                #convert mouse pos to grid pos in gamerect

                #TODO: add position offset ez ik but im about to go work
                nm = (mouse[0]*3 // rect.width , mouse[1]*3 // rect.height )
                gridPos = nm[0] + (nm[1]*3)

        if not self.grid[gridPos]:
                self.grid[gridPos] = move
        

    
    def draw(self):
        self.gameScreen.fill((155,155,155))
        
        for i,val in enumerate(self.grid):
            position = ((i%3)*self.cross.get_width(),(i//3)*self.cross.get_height())
            match val:
                case 1: #circle
                    self.gameScreen.blit(self.circle,position)
                case 2: #cross
                    self.gameScreen.blit(self.cross,position)

        #scale and draw
        game = pygame.transform.scale_by(self.gameScreen.copy(), self.scaleFactor)
        self.screen.blit(game,self.gamePosition)
        pygame.display.flip()


class miniMax:
    def __init__(self) -> None:
        pass
        #tree structure
    
    def update(self):
        pass
    
    def getMoves(self):
        pass

    def evalPosition(self):
        #recursive bit 
        pass



pygame.init() #initialise pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TicTacToe')
tictac = TicTac(screen,4,(0,0))
tick = 0
mouse = (0,0)
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break




        tictac.update()
        tictac.draw()
        
        

        
       
        
        
        tick=tick+1