import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

from pygame import mixer

mixer.init()
mixer.music.load('D:/flappygamegit/assets/music.wav')
mixer.music.play()

pygame.init()

#screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
bg = pygame.image.load("D:/flappygamegit/assets/bg.png")
screen_shake = 0
once = True

WINDOW_SIZE = (600,800)
display = pygame.Surface((600,800))
#clock
clock = pygame.time.Clock()

#helpers
done = True

#creating a custom event for adding a new obstascle

ADDOBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDOBSTACLE, 1800, loops=5)
ADDBIGBOY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBIGBOY, 10000, loops=1)
ADDGUN = pygame.USEREVENT + 3
pygame.time.set_timer(ADDGUN,10000, loops=1)
ADDHITBOX = pygame.USEREVENT + 4
pygame.time.set_timer(ADDHITBOX,10000, loops=1)
ADDENEMYPROJECTILE = pygame.USEREVENT + 5
pygame.time.set_timer(ADDENEMYPROJECTILE, 1250)
ADDGUNCONTINUOUS = pygame.USEREVENT + 6
pygame.time.set_timer(ADDGUNCONTINUOUS,12000)
BIGBOYENTRANCE = pygame.USEREVENT + 7
pygame.time.set_timer(BIGBOYENTRANCE,7000, loops = 1)
# WEAPONOFF = pygame.USEREVENT + 6
# pygame.time.set_timer(WEAPONOFF,5000, loops=1)

#CLASSES
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird,self).__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("D:/flappygamegit/assets/yellowbird-upflap.png"))
        self.sprites.append(pygame.image.load("D:/flappygamegit/assets/yellowbird-midflap.png"))
        self.sprites.append(pygame.image.load("D:/flappygamegit/assets/yellowbird-downflap.png"))
        self.current_sprite = 0
        self.surf = self.sprites[self.current_sprite]
        # self.surf = pygame.image.load("flappy.png").convert_alpha()
        # self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0]*2), int(self.size[1]*2)))
        self.rect = self.surf.get_rect(
            center=(
                75,
                SCREEN_HEIGHT/2,
            )
        )
        #for speed
        self.speed = 0

        #for rotation
        self.angle = 0

        #boolean weapon
        self.weaponOn = False

        self.increment = 0

        self.timer = 0

    def gravity(self):
        self.speed += 3
        self.angle -= 4

    def update(self, pressed_keys):

        if pressed_keys[K_UP] and done == True:
            self.speed = -25
            self.angle = 80

        if self.angle >= 50:
            self.angle = 50

        if self.angle <= -70:
            self.angle = -70



        # if self.rect.bottom >= SCREEN_HEIGHT:
        #     self.rect.bottom = SCREEN_HEIGHT - 3
        #     self.speed = -3

        # animation
        if self.weaponOn == False:
            self.current_sprite += 0.3
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.surf = self.sprites[int(self.current_sprite)]
            self.size = self.surf.get_size()
            self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
            self.surf = pygame.transform.rotate(self.surf, self.angle)

        elif self.weaponOn == True and self.timer < 150:
            self.surf = pygame.image.load("D:/flappygamegit/assets/gunbird.png").convert_alpha()
            self.size = self.surf.get_size()
            self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
            if pressed_keys[K_SPACE] and ((self.increment % 2) == 0):
                bullets = Bullets(self.rect.centery)
                projectiles.add(bullets)

            self.increment += 1
            self.timer += 1

        if self.timer >= 150:
            self.timer = 0
            self.weaponOn = False

        self.gravity()
        self.rect.move_ip(0,self.speed)




#Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle,self).__init__()
        self.surf1 = pygame.image.load("D:/flappygamegit/assets/pipe-greendown.png")
        self.size1 = self.surf1.get_size()
        self.surf1 = pygame.transform.scale(self.surf1, (int(self.size1[0] * 2), int(self.size1[1] * 2)))
        self.surf2 = pygame.image.load("D:/flappygamegit/assets/pipe-greenup.png")
        self.size2 = self.surf2.get_size()
        self.surf2 = pygame.transform.scale(self.surf2, (int(self.size2[0] * 2), int(self.size2[1] * 2)))
        self.shake = False
        self.gap = 400
        xpos = 700
        ypos = random.randint(600,900)

        #bottom
        self.rect1 = self.surf1.get_rect(
            center=(
                xpos,
                ypos,
            )
        )
        #top
        self.rect2 = self.surf2.get_rect(
            center=(
                xpos,
                ypos-500-self.gap,
            )
        )
        self.speed = -4

    def updatebool(self):
        self.shake = True

    def update(self):
        if pygame.time.get_ticks() < 9000:
            self.rect1.move_ip(-5, 0)
            self.rect2.move_ip(-5, 0)
            if self.rect1.right < 0:
                self.kill()
            if self.rect2.right < 0:
                self.kill()


        if pygame.time.get_ticks() > 9000:
            self.speed += 2
            self.rect1.move_ip(self.speed,0)
            self.rect2.move_ip(self.speed, 0)


#class Bigboy
class Bigboy(pygame.sprite.Sprite):
    def __init__(self):
        super(Bigboy,self).__init__()
        self.surf = pygame.image.load("D:/flappygamegit/assets/bigboy.png").convert_alpha()
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 4), int(self.size[1] * 5)))
        # self.size = self.surf.get_size()
        # self.surf = pygame.Surface(self.size)
        # self.rect = pygame.Rect((700, 0, 100, 800))

        self.rect = self.surf.get_rect(
            center=(
                600,
                SCREEN_HEIGHT / 2,
            )
        )
        self.action = 0
        self.counter = 0
        self.hit = False
        self.check = True
        self.counter = 0.5
        self.hitpoints = 200


    def update(self):
        #first movement
        if self.action <= 27:
            self.rect.move_ip(-10,0)
            self.action += 1

        #idle movement
        if self.action > 27:
            if self.check == True:
                self.rect.move_ip(-1,0)
                self.counter += 0.5
                if self.counter % 10 == 0:
                    self.check = False
            if self.check == False:
                self.rect.move_ip(1, 0)
                self.counter -= 0.5
                if self.counter % 10 == 0:
                    self.check = True


        #figure it out

        if self.hit == True:
            self.surf = pygame.image.load("D:/flappygamegit/assets/bigboytransparent.png").convert_alpha()
            self.size = self.surf.get_size()
            self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 4), int(self.size[1] * 5)))
            self.hitpoints -= 1
            self.hit = False
        elif self.hit == False:
            self.surf = pygame.image.load("D:/flappygamegit/assets/bigboy.png").convert_alpha()
            self.size = self.surf.get_size()
            self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 4), int(self.size[1] * 5)))

        if self.hitpoints == 0:
            self.kill()
            pygame.time.wait(100)


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super(Gun,self).__init__()
        self.surf = pygame.image.load("D:/flappygamegit/assets/gunremoved.png").convert_alpha()
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] / 2), int(self.size[1] / 2)))
        self.rect = self.surf.get_rect(
            center=(
                400,
                0,
            )
         )
        self.action = 0

    def update(self):
        self.rect.move_ip(0,5)
        self.action += 1
        self.rect.move_ip(-5,0)

class Bullets(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Bullets, self).__init__()
        self.position = position
        self.sprites = []
        for x in range(1,11):
            self.sprites.append(pygame.image.load("D:/flappygamegit/assets/bullet" + str(x) + ".png"))
        self.current_sprite = 0
        self.surf = self.sprites[self.current_sprite]
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 4), int(self.size[1] * 4)))
        self.rect = self.surf.get_rect(
            center=(
                150,
                self.position + 38
            )
        )
        self.speed = 2

    def update(self):
        self.speed += 2
        self.current_sprite += 0.3
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = len(self.sprites)-1
        self.surf = self.sprites[int(self.current_sprite)]
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 4), int(self.size[1] * 4)))
        self.rect.move_ip(self.speed,0)

class Hitbox(pygame.sprite.Sprite):
    def __init__(self):
        super(Hitbox, self).__init__()
        self.rect = pygame.Rect((820, 0, 100, 800))
        self.surf = pygame.Surface((100,800))
        self.surf = self.surf.convert_alpha()
        self.surf.set_alpha(0)
        self.action = 0

    def update(self):
        #first movement
        if self.action <= 27:
            self.rect.move_ip(-10,0)
            self.action += 1

class Enemyprojectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemyprojectile, self).__init__()
        self.surf = pygame.image.load("D:/flappygamegit/assets/pipeprojectile.png").convert_alpha()
        self.size = self.surf.get_size()
        self.surf1 = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect(
            center=(
                900,
                random.randint(0,SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,30)
    def update(self):
        self.rect.move_ip(-self.speed, 0)

class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        super(Gameover,self).__init__()
        self.surf = pygame.image.load("D:/flappygamegit/assets/gameover.png").convert_alpha()
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2
            )
        )
        self.alpha = 0
        self.surf.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        self.alpha = min(self.alpha+20,255)
        self.surf = pygame.image.load("D:/flappygamegit/assets/gameover.png").convert_alpha().copy()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.surf.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)


def gameover():
    clear = 255
    display.fill((255,255,255))
    rect = display.get_rect()
    screen.blit(display,rect)
    if clear >= 0:
        clear -= 1

    display.set_alpha(round(clear))




#sprite groups
obstacle = Obstacle()
bird = Bird()
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites.add(bird)
obstacles.add(obstacle)
enemies = pygame.sprite.Group()
weapons = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
hitboxes = pygame.sprite.Group()
enemyprojectiles = pygame.sprite.Group()

fakeobstacles = pygame.sprite.Group()

#custom functions
def spritecollideanymod(sprite, group, collided=None):
    default_sprite_collide_func = sprite.rect.colliderect

    if collided is not None:
        for group_sprite in group:
            if collided(sprite, group_sprite):
                return group_sprite
    else:
        # Special case old behaviour for speed.
        for group_sprite in group:
            if default_sprite_collide_func(group_sprite.rect1):
                return group_sprite
            elif default_sprite_collide_func(group_sprite.rect2):
                return group_sprite
    return None

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect

timer = 0

#GAME LOOP
running = True

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False
        if event.type == ADDOBSTACLE and done == True:
            new_obstacle = Obstacle()
            obstacles.add(new_obstacle)

        if event.type == ADDBIGBOY:
            newhitbox = Hitbox()
            hitboxes.add(newhitbox)
            all_sprites.add(newhitbox)
            newbigboy = Bigboy()
            enemies.add(newbigboy)
            all_sprites.add(newbigboy)
        if event.type == ADDGUN:
            newgun = Gun()
            all_sprites.add(newgun)
            weapons.add(newgun)
        if pygame.time.get_ticks() > 11000 and done == True:
            if event.type == ADDENEMYPROJECTILE:
                enproj = Enemyprojectile()
                enemyprojectiles.add(enproj)
                enemies.add(enproj)
                all_sprites.add(enproj)
        if pygame.time.get_ticks() > 16000:
            if event.type == ADDGUNCONTINUOUS:
                newgun = Gun()
                all_sprites.add(newgun)
                weapons.add(newgun)

        if pygame.time.get_ticks() > 9000 and once == True:
            screen_shake = 70
            once = False

        # elif event.type == WEAPONOFF:
        #     print("firing")
        #     bird.weaponOn = False

    if screen_shake > 0:
        screen_shake -= 1

    #updating positions
    pressed_keys = pygame.key.get_pressed()
    bird.update(pressed_keys)
    obstacles.update()
    enemies.update()
    weapons.update()
    projectiles.update()
    hitboxes.update()
    screen.blit(bg,(0,0))

    #rendering all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for entity in obstacles:
        screen.blit(entity.surf1, entity.rect1)
        screen.blit(entity.surf2, entity.rect2)
    for entity in projectiles:
        screen.blit(entity.surf,entity.rect)

    #collisionFFFFFFFFFFFFFFFFFFFFFFFhELLO Hello my name
    if spritecollideanymod(bird,obstacles) and done == True:
        gameover()
        gameoverr = Gameover()
        all_sprites.add(gameoverr)
        done = False

    if done == False:
        gameoverr.update()
        timer += 1
        if timer > 100:
            running = False

    if pygame.sprite.spritecollideany(bird,weapons):
        bird.weaponOn = True
        newgun.kill()

    if pygame.sprite.groupcollide(projectiles,hitboxes,True,False):
        newbigboy.hit = True

    if pygame.sprite.spritecollideany(bird,enemyprojectiles) and done == True:
        bird.kill()
        bird.weaponOn = False
        gameoverr = Gameover()
        all_sprites.add(gameoverr)
        done = False
        gameover()

    render_offset = [0,0]
    if screen_shake:
        render_offset[0] = random.randint(0,8) - 4
        render_offset[1] = random.randint(0, 8) - 4

    screen.blit(pygame.transform.scale(screen,WINDOW_SIZE),render_offset)
    pygame.display.update()
    pygame.display.flip()

    clock.tick(30)