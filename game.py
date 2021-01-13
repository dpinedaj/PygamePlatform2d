import pygame
from pygame.locals import *
import os
import json
from entities.character import Character
from entities.block import Block
from modules.utils import load_image, load_image_folder

# TODO AUTOMATIC LEVEL LOAD
# TODO LOAD DINAMICALLY ALL THE TILES AND OBJECTS IN LEVEL JSON
# TODO CHECK THE GAME SCALE VS LVL EDITOR
# TODO CAMERA FOLLOWS HERO
# TODO BACKGROUND LAYER
# TODO SOUNDS
# TODO ENEMIES
# Constants
ASSETS_PATH = "assets"
CHARACTER_PATH = os.path.join(ASSETS_PATH, "character")
TILES_PATH = os.path.join(ASSETS_PATH, 'tiles')
LEVELS_PATH = "levels"
SCALE_REFERENCE = {
    "block.png": 2,
    "character.png": 3
}
OBJECT_REFERENCE = {
    "block.png": Block
}


class Game:
    def __init__(self):
        self.canvas = pygame.display.set_mode((960, 580))
        self.initial_position = pygame.Vector2(0, 0)
        self.hero = None
        self.current_level = 0
        self.clock = None
        self.blocks = None
        self.enemies = None
        self.running = False

        self.tiles_groups = {}
        self.tiles_images = {}

    def load_hero(self):
        # Load Character
        hero_scale = SCALE_REFERENCE["character.png"]
        idle_imgs = load_image_folder(os.path.join(CHARACTER_PATH, 'idle'), scale=hero_scale)
        base_imgs = load_image(os.path.join(CHARACTER_PATH, 'idle', '0.png'), scale=hero_scale)
        attack_imgs = [load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '1'), scale=hero_scale),
                       load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '2'), scale=hero_scale),
                       load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '3'), scale=hero_scale)]
        run_imgs = load_image_folder(os.path.join(CHARACTER_PATH, 'run'), scale=hero_scale)
        jump_imgs = load_image_folder(os.path.join(CHARACTER_PATH, 'jump'), scale=hero_scale)
        fall_imgs = load_image_folder(os.path.join(CHARACTER_PATH, 'fall'), scale=hero_scale)

        hero_images = {'idle': idle_imgs,
                       'base': base_imgs,
                       'attack': attack_imgs,
                       'run': run_imgs,
                       'jump': jump_imgs,
                       'fall': fall_imgs}

        self.hero = Character(self.initial_position, hero_images)

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
                    self.initial_position = pygame.Vector2(level_data[pos]["x"] *32, level_data[pos]["y"] *32)
                    continue
                pos_vec = pygame.Vector2(level_data[pos]["x"] * 32, level_data[pos]["y"] * 32)
                self.tiles_groups[tile["tile"]].add(OBJECT_REFERENCE[tile["tile"]](pos_vec,
                                                    self.tiles_images[tile["tile"]]))

    def start(self):
        pygame.init()
        # clock - FPS
        self.clock = pygame.time.Clock()
        # mainloop
        self.running = True
        # load main menu
        self.load_level()
        self.load_hero()


    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_x:
                        self.hero.attack()
                    elif event.key == K_UP:
                        self.hero.jump()

            pressed = pygame.key.get_pressed()
            if pressed[K_LEFT]:
                self.hero.move(left=True)
            elif pressed[K_RIGHT]:
                self.hero.move()
            else:
                self.hero.stop_moving()

            self.canvas.fill((0, 0, 0))

            for name, group in self.tiles_groups.items():
                group.draw(self.canvas)
                for b_sprite in group.sprites():
                    b_sprite.draw_line_limit(self.canvas, color=(255, 0, 0))
                self.hero.update(self.canvas, group)
            pygame.display.flip()

            self.clock.tick(15)

        pygame.quit()

    def main(self):
        self.start()
        self.update()


if __name__ == '__main__':
    Game().main()
