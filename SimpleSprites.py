import sys, pygame
import random
import math
pygame.init()

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Load Screen Style
size_ws = width, height = 340, 244
#resolution = (960, 732)
screen  = pygame.Surface(size_ws)
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
resolution = display.get_size()

# Load Graphics
sprite_size = (16, 16)
colorkey    = (157,157,157)
spritesheet = pygame.image.load(r"C:\Users\Underwood\Documents\sandbox\art\arcadArne_sheet.png").convert()
block_spriteList = [ (132, ii * 40 + 8 , 16, 16) for ii in range(17)]
player_sprite = (392,848, 16, 16)

number_size        = (90, 151)
number_colorkey    = (255, 255, 255)
number_spritesheet = pygame.image.load(r"C:\Users\Underwood\Documents\sandbox\art\Number collection.png").convert()
number_spriteList  = [ ( 130, 972, 90, 151) 
                     , ( 250, 972, 90, 151)
                     , ( 369, 972, 90, 151)
                     , ( 488, 972, 90, 151)
                     , ( 607, 972, 90, 151)
                     , ( 726, 972, 90, 151)
                     , ( 845, 972, 90, 151)
                     , ( 964, 972, 90, 151)
                     , (1083, 972, 90, 151)
                     , (1202, 972, 90, 151)
                     ]

blue   = (0xa5, 0xd8, 0xff)
green  = (0x06, 0xa7, 0x7d)
yellow = (0xf8, 0xf3, 0x2b)
red    = (0xd8, 0x31, 0x5b)
grey   = (0x88, 0xa0, 0xa8)
black  = (0x1e, 0x1b, 0x18)
white  = (0xb4, 0xb8, 0xab)

class Block(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.image = pygame.Surface(sprite_size)
        self.image.set_colorkey(colorkey)
        
        self.image.blit(spritesheet, (0,0), random.choice(block_spriteList))
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.acc = pygame.math.Vector2(32, 32)
        
    def update(self):
        self.rect.y += 1
        if self.rect.y > height:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, width)
            self.image.blit(spritesheet, (0,0), random.choice(block_spriteList))
           
class Player(Block):
    def __init__(self):
        super().__init__(width/2, height/2)
        self.image.blit(spritesheet, (0,0), player_sprite)
    
    def update(self):
        self.rect.x , self.rect.y = pygame.mouse.get_pos()
    

class Number(pygame.sprite.Sprite): 
    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.update_image(value)
    
    def update_image(self, value):
        stringSize = len(str(value))
        self.image = pygame.Surface((stringSize + number_size[0] * stringSize, number_size[1]))
        self.image.set_colorkey(number_colorkey)
        self.image.fill(number_colorkey)
        
        for ii, digit in enumerate(str(value)):
            loc = (1 + number_size[0] * ii , 0)
            self.image.blit(number_spritesheet, loc, number_spriteList[int(digit)])
        
        
        self.image = pygame.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
            
    
    
def runGame():

    block_list       = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    
    dispScore = Number()
    all_sprites_list.add(dispScore)
    
    for _ in range(2000):
        block = Block(random.randrange(width), random.randrange(height))
        block_list.add(block)
        all_sprites_list.add(block)
        
    player = Player()
    all_sprites_list.add(player)    
        
    
    score = 0
    dispScore.update_image(score)
    done = False
        

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT : done = True
            if event.type == pygame.KEYDOWN :
                if event.__dict__['unicode'] == 'q':
                    done = True

        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

        for block in blocks_hit_list:
            score += 1
            dispScore.update_image(score)
        
        screen.fill(red)
        all_sprites_list.update()
        all_sprites_list.draw(screen)
        
        clock.tick(60)
        
        pygame.transform.scale(screen, resolution, display)
        pygame.display.flip()
        
    pygame.quit()


if __name__=="__main__": runGame()
