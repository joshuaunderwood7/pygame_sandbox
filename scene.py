import sys, pygame
import random
import math
import physics

### PyGame Environment ###
pygame.init()
clock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

### Load Screen Style ###
size_ws =  340 * 3, 244 * 3
display = pygame.display.set_mode(size_ws)
resolution = width, height = display.get_size()

### Load Font Style ###
font = pygame.font.SysFont("mono", 12)

### Load Graphics Assets ###

### Set Graphics Pallet ###
black  = (0x00, 0x00, 0x00)
white  = (0xb4, 0xb8, 0xab)
red    = (0xd8, 0x31, 0x5b)

### Load Sound Assets ###

### Set Sprite Classes ###
class Actor(pygame.sprite.Sprite, physics.Physical):
    def __init__(self, posX, posY):
        super(Actor, self).__init__()
        self.physical_init()
        
        self.color  = white
        self.image = pygame.Surface((5,5))
        self.image.fill(self.color)

        self.rect   = self.image.get_rect()
        self.set_position(posX, posY)
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]


    def update(self):
        if self.position[0] < 0: 
            self.position[0] = 0
            self.bounce(pygame.math.Vector2(1,0), reflectivity=0.3)
        if self.position[0] > width:  
            self.position[0] = width
            self.bounce(pygame.math.Vector2(-1,0), reflectivity=0.3)

        if self.position[1] < 0: 
            self.position[1] = 0
            self.bounce(pygame.math.Vector2(0,1), reflectivity=0.3)
        if self.position[1] > height: 
            self.position[1] = height
            self.bounce(pygame.math.Vector2(0,-1), reflectivity=0.3)

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def set_color(self, color):
        self.color = color
        self.image.fill(self.color)


### Game Function ###
def runGame():

    ### Environment Creation ###
    env = physics.PhysicsEnvironment(global_clock=clock)
    env.activate_gravity()

    ### Sprite Containers ###
    all_sprites_list = pygame.sprite.Group()
    gravity_list = pygame.sprite.Group()

    ### Actor Creation ###
    center = Actor(width / 2, height / 2)
    center.set_color(red)
    center.mass = 10
    gravity_list.add(center)
    env.add_object(center)

    for _ in range(200):
        x = random.randrange(width)
        y = random.randrange(height)
        block = Actor(x, y)
        env.add_object(block)
        gravity_list.add(block)

    ### Set Draw Order ###
    for block in gravity_list:
        all_sprites_list.add(block)
    all_sprites_list.add(center)

    ### Initilize Game Elements ###
    done = False

    ### Game Loop ###
    while not done:

        ### Handle Events ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT : done = True
            if event.type == pygame.KEYDOWN :
                if event.__dict__['unicode'] == 'q':
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                env.explosion(pygame.math.Vector2(pygame.mouse.get_pos()), 1000, 1)


        #=== Game Logic ===#
        #env.run()
        env.span_time(1)

        #==================#

        ### Update Display ###
        display.fill(black)
        all_sprites_list.update()
        all_sprites_list.draw(display)


        ### Manage Refresh Rate ###
        clock.tick(32)
        pygame.display.flip()

    ### Clean up when done playing ###
    pygame.quit()


### Allows Modulization ###
if __name__=="__main__": runGame()

