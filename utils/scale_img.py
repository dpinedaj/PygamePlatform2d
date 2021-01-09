import pygame
import os
import sys

def scale_img(factor, path):
    sep = os.path.sep
    path_list = path.split(sep)
    file_name = path_list[-1]
    base_path = sep.join(path_list[:-1])
    new_path = os.path.join(base_path, file_name[:-4] + "_copy" + file_name[-4:])
    img = pygame.image.load(path)
    h = img.get_height()
    w = img.get_width()
    img = pygame.transform.scale(img, (int(round(w * factor)), int(round(h * factor))))
    pygame.image.save(img, new_path)
    

path = sys.argv[1]
factor = sys.argv[2]
scale_img(float(factor), path)
