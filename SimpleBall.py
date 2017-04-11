import sys, pygame
pygame.init()

size    = width, height = 256, 244
size_ws = width, height = 340, 244
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size_ws)

ball = pygame.image.load(r"C:\Users\Underwood\Documents\sandbox\art\platformerArt_v4\png\coin_gold.png").convert()
ballrect = ball.get_rect()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.__dict__['unicode'] == 'j' : speed[0] = -speed[0]
            if event.__dict__['unicode'] == 'k' : speed[1] = -speed[1]
            if event.__dict__['unicode'] == 'q' : sys.exit()
            print(event)
            

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.time.delay(100)
    pygame.display.flip()
