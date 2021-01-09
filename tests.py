import pygame
from pygame.locals import *
from collections import namedtuple

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))

max_gravity = 100


class Block(object):
    sprite = pygame.image.load(r"assets\tiles\block.png").convert_alpha()

    def __init__(self, x, y):
        self.rect = self.sprite.get_rect(centery=y, centerx=x)


class Player(object):
    sprite = pygame.image.load(r"assets\tiles\character.png").convert()
    sprite.set_colorkey((0, 255, 0))

    def __init__(self, x, y):
        self.rect = self.sprite.get_rect(centery=y, centerx=x)
        # indicates that we are standing on the ground
        # and thus are "allowed" to jump
        self.on_ground = True
        self.xvel = 0
        self.yvel = 0
        self.jump_speed = 10
        self.move_speed = 8

    def update(self, move, blocks):

        # check if we can jump
        if move.up and self.on_ground:
            self.yvel -= self.jump_speed

        # simple left/right movement
        if move.left: self.xvel = -self.move_speed
        if move.right: self.xvel = self.move_speed

        # if in the air, fall down
        if not self.on_ground:
            self.yvel += 0.3
            # but not too fast
            if self.yvel > max_gravity: self.yvel = max_gravity

        # if no left/right movement, x speed is 0, of course
        if not (move.left or move.right):
            self.xvel = 0

        # move horizontal, and check for horizontal collisions
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, blocks)

        # move vertically, and check for vertical collisions
        self.rect.top += self.yvel
        self.on_ground = False;
        self.collide(0, self.yvel, blocks)

    def collide(self, xvel, yvel, blocks):
        # all blocks that we collide with
        for block in [blocks[i] for i in self.rect.collidelistall(blocks)]:

            # if xvel is > 0, we know our right side bumped
            # into the left side of a block etc.
            if xvel > 0: self.rect.right = block.rect.left
            if xvel < 0: self.rect.left = block.rect.right

            # if yvel > 0, we are falling, so if a collision happpens
            # we know we hit the ground (remember, we seperated checking for
            # horizontal and vertical collision, so if yvel != 0, xvel is 0)
            if yvel > 0:
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.yvel = 0
            # if yvel < 0 and a collision occurs, we bumped our head
            # on a block above us
            if yvel < 0: self.rect.top = block.rect.bottom


blocklist = []
player = []
colliding = False
Move = namedtuple('Move', ['up', 'left', 'right'])
while True:
    screen.fill((25, 30, 90))
    mse = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT: exit()

        if key[K_LSHIFT]:
            if event.type == MOUSEMOTION:
                if not any(block.rect.collidepoint(mse) for block in blocklist):
                    x = (int(mse[0]) / 32) * 32
                    y = (int(mse[1]) / 32) * 32
                    blocklist.append(Block(x + 16, y + 16))
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    to_remove = [b for b in blocklist if b.rect.collidepoint(mse)]
                    for b in to_remove:
                        blocklist.remove(b)

                    if not to_remove:
                        x = (int(mse[0]) / 32) * 32
                        y = (int(mse[1]) / 32) * 32
                        blocklist.append(Block(x + 16, y + 16))

                elif event.button == 3:
                    x = (int(mse[0]) / 32) * 32
                    y = (int(mse[1]) / 32) * 32
                    player = []
                    player.append(Player(x + 16, y + 16))

    move = Move(key[K_UP], key[K_LEFT], key[K_RIGHT])
    for b in blocklist:
        screen.blit(b.sprite, b.rect)
    for p in player:
        p.update(move, blocklist)
        screen.blit(p.sprite, p.rect)
    clock.tick(60)
    pygame.display.flip()
