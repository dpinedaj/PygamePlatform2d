import pygame

CANVAS_WIDTH = 960
CANVAS_HEIGHT = 580


class Collider2D:
    def __init__(self, pos, width, height):
        self.rect = pygame.rect.Rect(pos[0], pos[1], width, height)

        self.__onGround = False

    @property
    def onGround(self):
        return self.__onGround

    def collision(self, other):
        return self.rect.colliderect(other.rect)

    def detect_blocks(self, blocks):
        # Detect blocks
        collision_blocks = [block for block in blocks if self.collision(block)]
        for block in collision_blocks:

            # Horizontal delimiters
            if block.rect.left > self.rect.right:
                self.rect.right = block.rect.left

            elif block.rect.right < self.rect.left:
                self.rect.left = block.rect.right

            # Vertical delimiters

            if block.rect.top < self.rect.bottom:
                self.rect.bottom = block.rect.top
                self.__onGround = True
            else:
                self.__onGround = False
