import pygame
import os
import json

from entities import Block
from .utils import load_image

ASSETS_PATH = "assets"
TILES_PATH = os.path.join(ASSETS_PATH, 'tiles')
LEVELS_PATH = "levels"
SCALE_REFERENCE = {
    "block.png": 2,
    "character.png": 3
}
OBJECT_REFERENCE = {
    "block.png": Block
}


class Level:

    def __init__(self, level):
        self.current_level = level
        self.hero_position = pygame.Vector2()

        self.tiles_groups = {}
        self.tiles_images = {}

    def new_level(self, level):
        self.current_level = level

    def load_level(self):
        # Load Map TODO will change when the levels are ready
        tiles_list = [p for p in os.listdir(TILES_PATH) if p != "character.png"]
        self.tiles_images = {tile: load_image(os.path.join(TILES_PATH, tile), scale=SCALE_REFERENCE[tile])
                             for tile in tiles_list}
        self.tiles_groups = {tile: pygame.sprite.Group() for tile in tiles_list}

        with open(os.path.join(LEVELS_PATH, f"{self.current_level}.json"), "r") as json_file:
            level_data = json.load(json_file)

        for pos in level_data:
            for tile in level_data[pos]["tiles"]:
                if tile["tile"] == "character.png":
                    self.hero_position = pygame.Vector2(level_data[pos]["x"] * 32, level_data[pos]["y"] * 32)
                    continue
                pos_vec = pygame.Vector2(level_data[pos]["x"] * 32, level_data[pos]["y"] * 32)
                self.tiles_groups[tile["tile"]].add(OBJECT_REFERENCE[tile["tile"]](pos_vec,
                                                                                   self.tiles_images[tile["tile"]]))

    def get_hero_position(self):
        return self.hero_position

    def get_tiles_groups(self):
        return self.tiles_groups
