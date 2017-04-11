import sys, pygame
import random
import math

### Global Constants ###
G = 1e-4 # Gravity in this world


### PyGame Environment ###
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

### Load Screen Style ###
size_ws = width, height = 340, 244
screen  = pygame.Surface(size_ws)
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
resolution = display.get_size()

### Load Font Style ###
font = pygame.font.SysFont("mono", 80)

### Load Graphics Assets ###
sprite_size = (16, 16)
colorkey    = (157,157,157)
spritesheet = pygame.image.load(r"art\arcadArne_sheet.png").convert()
block_spriteList = [ (132, ii * 40 + 8 , 16, 16) for ii in range(17)]
player_sprite = (392,848, 16, 16)
bullet_sprite = (412,848, 16, 16)

number_size        = (90, 151)
number_colorkey    = (255, 255, 255)
number_spritesheet = pygame.image.load(r"art\Number collection.png").convert()
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

### Set Graphics Pallet ###
blue   = (0xa5, 0xd8, 0xff)
green  = (0x06, 0xa7, 0x7d)
yellow = (0xf8, 0xf3, 0x2b)
red    = (0xd8, 0x31, 0x5b)
grey   = (0x88, 0xa0, 0xa8)
black  = (0x1e, 0x1b, 0x18)
white  = (0xb4, 0xb8, 0xab)

### Load Sound Assets ###
shoot_sound = pygame.mixer.Sound(r"art\silencer.wav")
bg_music    = pygame.mixer.music.load(r"art\Orbital Colossus.mp3")



### Set Sprite Classes ###
class Actor(pygame.sprite.Sprite):
    def __init__(self, posX, posY, vel=(0.0, 0.0), acc=(0.0, 0.0)):
        super().__init__()
        self.image = pygame.Surface(sprite_size)
        self.image.set_colorkey(colorkey)

        self.image.blit(spritesheet, (0,0), random.choice(block_spriteList))

        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.vel = pygame.math.Vector2(vel)
        self.acc = pygame.math.Vector2(acc)


class FallingBlock(Actor):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.acc[1] = G

    def update(self):
        time = clock.get_time()
        self.vel    += self.acc    * time
        self.rect.x += self.vel[0] * time
        self.rect.y += self.vel[1] * time
        if self.rect.y > height:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, width)
            self.vel = pygame.math.Vector2((0.0, 0.0))
            self.image.blit(spritesheet, (0,0), random.choice(block_spriteList))


class Player(Actor):
    def __init__(self):
        super().__init__(width/2, 240)
        self.image.blit(spritesheet, (0,0), player_sprite)

    def update(self):
        self.rect.x , _ = pygame.mouse.get_pos()


class Bullet(Actor):
    def __init__(self):
        super().__init__(pygame.mouse.get_pos()[0], 240)
        self.image.blit(spritesheet, (0,0), bullet_sprite)

    def fire(self):
        self.rect.x, _ = pygame.mouse.get_pos()
        self.rect.y    = 240

    def update(self):
        time = clock.get_time()
        self.rect.y -= 5


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


### Game Function ###
def runGame():

    ### Sprite Containers ###
    block_list       = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    bullet_list      = pygame.sprite.Group()
    dead_bullets     = pygame.sprite.Group()

    ### Actor Creation ###
    player = Player()
    dispScore = Number()
    for _ in range(50):
        block = FallingBlock(random.randrange(width), 0-random.randrange(height))
        block_list.add(block)

    ### Environment Creation ###
    bullet_stop = FallingBlock(0,-20)
    bullet_stop.rect.width = width

    ### Set Draw Order ###
    all_sprites_list.add(dispScore)
    for block in block_list : all_sprites_list.add(block)
    all_sprites_list.add(player)


    ### Initilize Game Elements ###
    score = 0
    dispScore.update_image(score)
    done = False
    #pygame.mixer.music.play(-1)


    ### Game Loop ###
    while not done:

        ### Handle Events ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT : done = True
            if event.type == pygame.KEYDOWN :
                if event.__dict__['unicode'] == 'q':
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot_sound.play()
                if not dead_bullets.sprites():
                    newBullet = Bullet()
                else:
                    newBullet = dead_bullets.sprites()[0]
                    dead_bullets.remove(newBullet)
                newBullet.fire()
                all_sprites_list.add(newBullet)
                bullet_list.add(newBullet)

        #=== Game Logic ===#
        for dead_bullet in pygame.sprite.spritecollide(bullet_stop, bullet_list, True):
            dead_bullets.add(dead_bullet)

        for bullet in bullet_list:
            blocks_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
            if blocks_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                dead_bullets.add(bullet)
            for block in blocks_hit_list:
                score += 1
                dispScore.update_image(score)
        #==================#

        ### Update Screen ###
        screen.fill(red)
        all_sprites_list.update()
        all_sprites_list.draw(screen)


        ### Bullshit style testing ###
        active = len(bullet_list)
        dead   = len(dead_bullets)
        text = font.render(f"{active} : {dead}", True, yellow)
        text = pygame.transform.scale(text, screen.get_size())

        screen.blit(text, (0,0))
        pygame.transform.scale(screen, resolution, display)

        ### Manage Refresh Rate ###
        clock.tick(32)
        pygame.display.flip()

    ### Clean up when done playing ###
    pygame.quit()


### Allows Modulization ###
if __name__=="__main__": runGame()

