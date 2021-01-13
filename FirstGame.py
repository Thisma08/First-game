import pygame
import sys
import os

'''
Variables
'''
# Enter variables here
worldX = 960
worldY = 720
fps = 40
anim = 3
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
main = True
ALPHA = WHITE
forwardX = 600
backwardX = 230
'''
Objects
'''
# Enter Python classes and functions here


class platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Images', img)).convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.moveX = 0
        self.moveY = 0
        self.frame = 0
        self.health = 10
        self.score = 0
        self.isJump = True
        self.isFalling = False
        self.images = []
        for i in range(1, 4):
            img = pygame.image.load(os.path.join('Images', 'W' + str(i) + '.png')).convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        Control player movement
        """

        self.moveX += x
        self.moveY += y

    def update(self):
        """
        Update sprite position
        """
        self.rect.x = self.rect.x + self.moveX
        self.rect.y = self.rect.y + self.moveY

        if self.moveX < 0:
            self.isJump = True
            pygame.time.wait(100)
            self.frame += 1
            if self.frame > 3 * anim:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame % anim], True, False)

        if self.moveX > 0:
            self.isJump = True
            pygame.time.wait(100)
            self.frame += 1
            if self.frame > 3 * anim:
                self.frame = 0
            self.image = self.images[self.frame % anim]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            print(self.health)

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.moveY = 0
            self.rect.bottom = g.rect.top
            self.isJump = False

        if self.rect.y > worldY:
            self.health -= 1
            print(self.health)
            self.rect.x = 200
            self.rect.y = worldY - 300

        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1
        print(self.score)

        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
        for p in plat_hit_list:
            self.isJump = False
            self.moveY = 0
            if self.rect.bottom <= p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.moveY += 3.2

        if self.isJump and self.isFalling is False:
            self.isFalling = True
            self.moveY -= 33

    def gravity(self):
        if self.isJump:
            self.moveY += 3.2

        if self.rect.y > worldY and self.moveY >= 0:
            self.moveY = 0
            self.rect.y = worldY - 300

    def jump(self):
        if self.isJump is False:
            self.isFalling = False
            self.isJump = True


class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Images', img)).convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def move(self):
        """
        enemy movement
        """
        distance = 60
        speed = 4

        if 0 <= self.counter <= distance:
            self.rect.x += speed
        elif distance <= self.counter <= distance*2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1


class level:
    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1], 'enemy.png')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            print('Level' + str(lvl))

        return enemy_list

    def ground(lvl, x, y, w, h):
        ground_list = pygame.sprite.Group()
        if lvl == 1:
            ground = platform(x, y, w, h, 'ground.png')
            ground_list.add(ground)

        if lvl == 2:
            print('Level' + str(lvl))

        return ground_list

    def platform(lvl):
        plat_list = pygame.sprite.Group()
        if lvl == 1:
            plat = platform(200, worldY-97-128, 285, 67, 'platform.png')
            plat_list.add(plat)
            plat = platform(600, worldY-97-320, 197, 54, 'platform.png')
            plat_list.add(plat)
        if lvl == 2:
            print('level' + str(lvl))

        return plat_list

    def loot(lvl):
        loot_list = pygame.sprite.Group()
        if lvl == 1:
            loot = platform(350, worldY-97-200, 50, 50, 'loot.png')
            loot_list.add(loot)
            loot = platform(750, worldY-97-392, 50, 50, 'loot.png')
            loot_list.add(loot)

        if lvl == 2:
            print(lvl)

        return loot_list


'''
Setup
'''
# Enter the run-once code here
clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldX, worldY])
player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 20
pygame.display.set_caption('FirstGame')
eloc = []
eloc = [300, 0]
enemy_list = level.bad(1, eloc)
ground_list = level.ground(1, 0, worldY-97, 1080, 97)
plat_list = level.platform(1)
loot_list = level.loot(1)


'''
Main Loop
'''
# Enter game loop here
while main:
    world.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_SPACE or event.key == ord('w'):
                player.jump()
                print('Jump')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
    if player.rect.x >= forwardX:
        scroll = player.rect.x - forwardX
        player.rect.x = forwardX
        for p in plat_list:
            p.rect.x += scroll
        for e in enemy_list:
            e.rect.x -= scroll

    if player.rect.x <= forwardX:
        scroll = backwardX - player.rect.x
        player.rect.x = backwardX
        for p in plat_list:
            p.rect.x += scroll
        for e in enemy_list:
            e.rect.x += scroll
        for l in loot_list:
            l.rect.x += scroll

    for e in enemy_list:
        e.move()
    player.gravity()
    player.update()
    player_list.draw(world)
    enemy_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)
    loot_list.draw(world)
    pygame.display.flip()
    pygame.time.Clock().tick(fps)
