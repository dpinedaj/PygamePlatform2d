import pygame
from pygame.locals import *
from pygame import Vector2
from entities import Hero, Block
from modules import Level, utils


class Game:
    def __init__(self):
        self.canvas = pygame.display.set_mode((960, 580))
        self.camera = None
        self.hero = None
        self.level = None
        self.clock = None
        self.running = False

        self.blocks = []
        self.current_level = 0
        self.tiles_groups = {}

    def start(self):
        pygame.init()
        # clock - FPS
        self.clock = pygame.time.Clock()
        # mainloop
        self.running = True
        # load main menu

        # TODO LOAD LEVEL
        self.level = Level(self.current_level)
        self.tiles_groups = self.level.get_tiles_groups()
        hero_position = self.level.get_hero_position()

        block_image = utils.load_image(r'assets\tiles\block.png', 4)

        block_width = 64
        block_position = 30
        for i in range(10):
            block = Block(Vector2(block_position, 300), block_image)
            self.blocks.append(block)
            block_position += block_width
        self.hero = Hero(pygame.Vector2(30, 30))

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
                self.hero.move(right=False)
            elif pressed[K_RIGHT]:
                self.hero.move()
            else:
                self.hero.stop_moving()

            self.canvas.fill((0, 0, 0))
            for block in self.blocks:
                self.canvas.blit(block.image, block.rect)
                utils.draw_line_limit(self.canvas, block.rect, (255, 0, 0))
            self.hero.update(self.canvas, self.blocks)
            utils.draw_line_limit(self.canvas, self.hero.collider.rect, (0, 255, 255))
            pygame.display.flip()

            self.clock.tick(15)

        pygame.quit()

    def main(self):
        self.start()
        self.update()


if __name__ == '__main__':
    Game().main()
