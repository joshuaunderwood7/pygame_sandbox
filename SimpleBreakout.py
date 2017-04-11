import sys, pygame
import random
import math
pygame.init()


C = { 'blue'   : (0xa5, 0xd8, 0xff)
    , 'green'  : (0x06, 0xa7, 0x7d)
    , 'yellow' : (0xf8, 0xf3, 0x2b)
    , 'red'    : (0xd8, 0x31, 0x5b)
    , 'grey'   : (0x88, 0xa0, 0xa8)
    }
black = (0x1e, 0x1b, 0x18)
white = (0xb4, 0xb8, 0xab)

choices = list(C.values())
size_ws = width, height = 340, 244

class Block():
    def __init__(self, posX, posY):
        self.width  = 34
        self.height = 7
        self.rect   = pygame.rect.Rect(posX+1,posY+1,self.width-2, self.height-2)
        self.color  = random.choice(choices)
    
    def get_rect(self):
        return self.rect

        
class Paddle(Block):
    def __init__(self):
        self.width  = 50
        self.height = 10
        self.posY   = 240
        self.posX   = 120
        self.rect   = pygame.rect.Rect(self.posX,self.posY,self.width, self.height)
        self.color  = white
    
    
    def update(self, posX):
        self.posX = posX - round(self.width/2)
        self.rect = pygame.rect.Rect(self.posX,self.posY,self.width, self.height)
        

class Ball(Block):
    def __init__(self):
        self.width  = 5
        self.height = 5
        self.velY   = -2
        self.posY   = 220
        self.velX   = 1
        self.posX   = 120
        self.rect   = pygame.rect.Rect(self.posX,self.posY,self.width, self.height)
        self.color  = white
    
    
    def update(self, paddle, blocks):
        if self.rect.colliderect(paddle):
            self.velY = -self.velY
        index = self.rect.collidelist(blocks)
        if index > -1:
            self.velY = -self.velY
            blocks.remove(blocks[index])
        self.rect = self.rect.move(self.velX, self.velY)
        if self.rect.left < 0 or self.rect.right > width:
            self.velX = -self.velX
        if self.rect.top < 0 or self.rect.bottom > height:
            self.velY = -self.velY
        


def runGame():
    pygame.init()



    screen = pygame.display.set_mode(size_ws)
    blocks = [Block(col * 34, row * 7) for col in range(10) for row in range(10)]
    paddle = Paddle()
    ball   = Ball()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.__dict__['unicode'] == 'q' : sys.exit()
                
        
        paddle.update(pygame.mouse.get_pos()[0])
        ball.update(paddle, blocks)
        
        
        screen.fill(black)

        for block in blocks:
            screen.fill(block.color, block.get_rect())
        screen.fill(paddle.color, paddle.get_rect())
        screen.fill(ball.color, ball.get_rect())

        pygame.display.flip()
        
        pygame.time.delay(10)
        
runGame()