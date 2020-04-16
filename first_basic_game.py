import pygame
import random
# import basic keystroke inputs that you want to use:
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_a,K_s,K_d,K_w,K_ESCAPE,KEYDOWN,KEYUP,QUIT,RLEACCEL
)
FPS = 60
if FPS == 60:
    s = 35
    e_s = 20
elif FPS == 30:
    s = 60
    e_s = 20
# define screen dimensions:
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
# define the user clas (see: https://realpython.com/python-super/ for information on use of super() inheritance)
class User(pygame.sprite.Sprite):
    def __init__(self):
        super(User,self).__init__()
        self.obj = pygame.image.load('Images/doctor copy.jpg')
        self.obj = pygame.transform.scale(self.obj,(100,140)).convert()
        self.obj.set_colorkey((254,254,254),RLEACCEL)
        self.rect = self.obj.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)) #starts at approximately center.
    def update(self, pressed_keys):
        # pressed_keys is a dict:
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -s)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, s)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-s, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(s, 0)
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -s)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, s)
        if pressed_keys[K_a]:
            self.rect.move_ip(-s, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(s, 0)
            # Keep player player on the screen by appearing out of opposite side...
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
# define the enemy class:
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.obj = pygame.image.load('Images/corona_blue.jpg').convert()
        self.obj.set_colorkey((2,2,2), RLEACCEL)
        self.obj = pygame.transform.scale(self.obj,(100,100))
        self.rect = self.obj.get_rect(
            center = (
                SCREEN_WIDTH,
                random.randint(50,SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(e_s,2*e_s)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
# create a clock to manage FPS:
clock = pygame.time.Clock()
# have to initialise pygame to get the library running:
pygame.init()
# create the screen:
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
# initiate the user:
usr = User()
# create event for adding enemies:
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)
# create two Sprite groups: one for all sprites, one for just the enemies.
all_spr = pygame.sprite.Group()
enemy_spr = pygame.sprite.Group()
all_spr.add(usr)
# get the game loop running and create the code to enable the user to quit the game. In this case the 'esc' key.
pygame.display.flip()
running = True
while running == True:
    # loop through the elements in the event queue:
    for event in pygame.event.get():
        # did the user press a key? act on this first...
        if event.type == KEYDOWN:
            # create if statements for esc key press:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT: # this is closing the window.
            running = False
        elif event.type == ADDENEMY:# check to see if any new enemies must be added.
            enemy = Enemy()
            enemy_spr.add(enemy)
            all_spr.add(enemy)
    screen.fill((255,255,255))
    #update user movement:
    pressed_keys = pygame.key.get_pressed()
    usr.update(pressed_keys)
    # update enemy movements:
    for sprite in enemy_spr:
        sprite.update()
    # update the display with all sprite movements:
    for sprite in all_spr:
        screen.blit(sprite.obj,sprite.rect)
    pygame.display.flip()
    if pygame.sprite.spritecollideany(usr,enemy_spr):
        usr.kill()
        running = False
    clock.tick(FPS)
# quit pygame and the python application:
pygame.quit()
quit()