import pygame


class Renderer2D(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self._image = image

    def _flip(self):
        self._image = pygame.transform.flip(self._image, True, False)

    def set_image(self, image, facing_right):
        self._image = image
        if not facing_right:
            self._flip()

    def draw(self, canvas, pos):
        canvas.blit(self._image, pos)
