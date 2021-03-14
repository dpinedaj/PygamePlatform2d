import pygame


class Entity2D(pygame.sprite.Sprite):

    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = self.images['base'] if isinstance(self.images, dict) else self.images

        # Define Rect
        self.rect = self.image.get_rect(center=pos)

