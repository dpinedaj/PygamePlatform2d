import os
import pygame


def chop_animation(animation_image, sub_images):
    surface = animation_image.convert_alpha()
    width = surface.get_width()
    height = surface.get_height()
    sub_height = height / sub_images
    animation_images = {1: [surface.subsurface((0, x * sub_height, width, sub_height))
                            for x in range(sub_images)]}
    animation_images[0] = \
        [pygame.transform.flip(img, True, False)
         for img in animation_images[1]]


def load_image(path, scale=0):
    img = pygame.image.load(path)
    if scale != 0:
        h = img.get_height()
        w = img.get_width()
        img = pygame.transform.scale(img, (w * scale, h * scale))
    return img


def load_image_folder(path, scale=0):
    image_paths = [os.path.join(path, p) for p in sorted(os.listdir(path))]
    images = {1: [load_image(p, scale) for p in image_paths]}
    images[0] = [pygame.transform.flip(img, True, False)
                 for img in images[1]]
    return images
