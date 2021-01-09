import pygame
from pygame.locals import *
import os
import json

# TODO THINK A BETTER WAY TO MANAGE THE JSON LEVEL DATA
# TODO SAVE INFORMATION IN THE JSON
# TODO READ CORRECTLY A JSON


# CONSTANTS
TILES_PATH = os.path.join("assets", "tiles")
MENU_COLOR = (111, 111, 111)
MAP_COLOR = (0, 0, 0)
DEFAULT_IN_MAP_NAME = os.path.join("levels", "in.json")
DEFAULT_EX_MAP_NAME = os.path.join("levels", "export.json")
LETTER_STYLE = 'Comic Sans MS'
FONT_SIZE = 15


class LevelEditor:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_width = 960
        self.window_height = 580
        self.menu_width = 40
        self.screen = None
        self.display = None
        self.font = None
        self.running = True

        # Functional Variables
        self.clicking = False
        self.removing = False
        self.current_tile = None
        self.click = False
        self.mouseR = None
        self.mx = 0
        self.my = 0

        # Scroll
        self.up = False
        self.down = False
        self.right = False
        self.left = False

        # Location and references
        self.scroll_x = 0
        self.scroll_y = 0

        # Containers
        self.tile_list = []
        self.tile_database = {}
        self.map_data = {}

    def load_tiles(self):
        self.tile_list = os.listdir(TILES_PATH)
        for tile in self.tile_list:
            img = pygame.image.load(os.path.join(TILES_PATH, tile)).convert()
            img.set_colorkey(MENU_COLOR)
            self.tile_database[tile] = {"image": img.copy(), "w": img.get_width(), "h": img.get_height()}

    def import_data(self):
        if os.path.isfile(DEFAULT_IN_MAP_NAME) and os.access(DEFAULT_IN_MAP_NAME, os.R_OK):
            with open(DEFAULT_IN_MAP_NAME, "r") as json_file:
                self.map_data = json.load(json_file)

    def export_data(self):
        with open(DEFAULT_EX_MAP_NAME, "w") as json_file:
            json_file.write(json.dumps(self.map_data, indent=4))

    def clear_map(self):
        self.map_data = {}

    def scroll_map(self):
        if self.right:
            self.scroll_x += 4
        if self.left and self.scroll_x > 0:
            self.scroll_x -= 4
        if self.up and self.scroll_y > 0:
            self.scroll_y -= 4
        if self.down:
            self.scroll_y += 4

    def draw_map(self):
        for tile in self.map_data:
            for img in self.map_data[tile]["tiles"]:
                width = img["w"]
                height = img["h"]
                self.display.blit(self.tile_database[img["tile"]]["image"],
                                  (self.map_data[tile]["x"] * width - self.scroll_x,
                                   self.map_data[tile]["y"] * height - self.scroll_y))

    def handle_mouse(self):
        # Mouse
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = int(self.mx / 2)
        self.my = int(self.my / 2)
        cur_mx = self.mx
        self.mouseR = pygame.Rect(self.mx, self.my, 2, 2)

        if self.current_tile is not None:
            width = self.tile_database[self.current_tile]["w"]
            height = self.tile_database[self.current_tile]["h"]

            self.mx = int(round((self.scroll_x + self.mx - 10) / width, 0))
            self.my = int(round((self.scroll_y + self.my - 10) / height, 0))

            if self.clicking and cur_mx > self.menu_width:
                loc = str(self.mx) + ';' + str(self.my)
                tile_data = {"tile": self.current_tile, "w": width, "h": height}
                if loc not in self.map_data:
                    self.map_data[loc] = {"tiles": [tile_data], "x": self.mx, "y": self.my}
                elif self.current_tile not in [tile["tile"] for tile in self.map_data[loc]["tiles"]]:
                    self.map_data[loc]["tiles"].append(tile_data)
            if self.removing:
                loc = str(self.mx) + ';' + str(self.my)
                if loc in self.map_data:
                    del self.map_data[loc]
            else:
                self.display.blit(self.tile_database[self.current_tile]["image"],
                                  (self.mx * width - self.scroll_x, self.my * height - self.scroll_y))

    def draw_tiles_menu(self):
        width = height = 20
        x = y = 0
        for img in self.tile_list:
            # width = self.tile_database[img]["w"] * scale_factor
            # height = self.tile_database[img]["h"] * scale_factor
            self.display.blit(
                pygame.transform.scale(self.tile_database[img]["image"], (width, height)),
                (x * width, y * height))
            tileR = pygame.Rect(x * width, y * height, width, height)
            if self.click:
                if self.mouseR.colliderect(tileR):
                    self.current_tile = img
                    self.clicking = False
            x += 1
            if x > 2:
                x = 0
                y += 1

    def print_scroll_position(self):
        curr_position = "({},{})".format(self.scroll_x, self.scroll_y)
        text = self.font.render(curr_position, False, (255, 255, 255))
        self.display.blit(text, (self.window_width / 4, 0))

    def handle_events(self):
        # Buttons ------------------------------------------------ #
        self.click = False

        for event in pygame.event.get():
            # Mouse behavior
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                    self.click = True
                if event.button == 3:
                    self.removing = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                if event.button == 3:
                    self.removing = False

            # Keyboard Behavior
            # TODO check movement with keyboard
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == ord('a'):
                    self.left = True
                if event.key == ord('d'):
                    self.right = True
                if event.key == ord('w'):
                    self.up = True
                if event.key == ord('s'):
                    self.down = True
                if event.key == ord('e'):
                    self.export_data()
                if event.key == ord('i'):
                    self.import_data()
                if event.key == ord('c'):
                    self.clear_map()
            if event.type == KEYUP:
                if event.key == ord('a'):
                    self.left = False
                if event.key == ord('d'):
                    self.right = False
                if event.key == ord('w'):
                    self.up = False
                if event.key == ord('s'):
                    self.down = False

    def start(self):
        pygame.init()
        pygame.mixer.quit()
        pygame.display.set_caption("Level Editor")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)
        self.display = pygame.Surface((self.window_width / 2, self.window_height / 2))
        self.font = pygame.font.SysFont(LETTER_STYLE, FONT_SIZE)
        self.load_tiles()

    def update(self):
        while self.running:
            # Draw the map
            self.display.fill(MAP_COLOR, (self.menu_width, 0, self.window_width - self.menu_width, self.window_height))
            self.draw_map()
            # Handle user behavior
            self.scroll_map()
            self.handle_mouse()
            self.handle_events()
            # Display menu
            self.display.fill(MENU_COLOR, (0, 0, self.menu_width, self.window_height))
            self.draw_tiles_menu()
            # Print position of the scroll
            self.print_scroll_position()
            # Blit everything in screen and update
            self.screen.blit(pygame.transform.scale(self.display, (self.window_width, self.window_height)), (0, 0))
            pygame.display.update()
            self.clock.tick(40)

    def main(self):
        self.start()
        self.update()


if __name__ == "__main__":
    LevelEditor().main()
