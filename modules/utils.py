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
    images = [load_image(p, scale) for p in image_paths]
    # images = {1: [load_image(p, scale) for p in image_paths]}
    # images[0] = [pygame.transform.flip(img, True, False)
    #              for img in images[1]]
    return images


def draw_line_limit(canvas, rect, color=(255, 255, 255), ):
    # TODO CHECKING RECT PROBLEMS
    # side lines
    pygame.draw.rect(canvas, color, (rect.right, rect.top, 1, rect.height), 0)
    pygame.draw.rect(canvas, color, (rect.left, rect.top, 1, rect.height), 0)

    # top and bottom lines
    pygame.draw.rect(canvas, color, (rect.left, rect.top, rect.width, 1), 0)
    pygame.draw.rect(canvas, color, (rect.left, rect.bottom, rect.width, 1), 0)