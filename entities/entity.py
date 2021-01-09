import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = self.images['base'] if isinstance(self.images, dict) else self.images

        # Define Rect
        self.rect = self.image.get_rect(center=pos)

        # Velocity
        self.vy = 0
        self.vx = 0

    def draw_line_limit(self, canvas, color=(255, 255, 255), rect=None):
        # TODO CHECKING RECT PROBLEMS
        # side lines
        rect = self.rect if rect is None else rect
        pygame.draw.rect(canvas, color, (rect.right, rect.top, 1, rect.height), 0)
        pygame.draw.rect(canvas, color, (rect.left, rect.top, 1, rect.height), 0)

        # top and bottom lines
        pygame.draw.rect(canvas, color, (rect.left, rect.top, rect.width, 1), 0)
        pygame.draw.rect(canvas, color, (rect.left, rect.bottom, rect.width, 1), 0)
