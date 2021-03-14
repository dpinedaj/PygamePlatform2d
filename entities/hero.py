import os
from pygame import Vector2
from .utils import Animator2D, Collider2D, RigidBody2D, Renderer2D
from modules.utils import load_image_folder

CHARACTER_PATH = os.path.join("assets", "hero")
HERO_SCALE = 3
HERO_WIDTH = 45
HERO_HEIGHT = 90
HERO_INITIAL_SPEED = 15
HERO_JUMP_POWER = 50
GRAVITY = 5


def load_hero_animation_database():
    idle_images = load_image_folder(os.path.join(CHARACTER_PATH, 'idle'), scale=HERO_SCALE)
    base_img = idle_images[0]
    attack_images = [load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '1'), scale=HERO_SCALE),
                     load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '2'), scale=HERO_SCALE),
                     load_image_folder(os.path.join(CHARACTER_PATH, 'attack', '3'), scale=HERO_SCALE)]
    run_images = load_image_folder(os.path.join(CHARACTER_PATH, 'run'), scale=HERO_SCALE)
    jump_images = load_image_folder(os.path.join(CHARACTER_PATH, 'jump'), scale=HERO_SCALE)
    fall_images = load_image_folder(os.path.join(CHARACTER_PATH, 'fall'), scale=HERO_SCALE)

    return {'idle': idle_images,
            'base': base_img,
            'attack': attack_images,
            'run': run_images,
            'jump': jump_images,
            'fall': fall_images}


class Hero:
    def __init__(self, position):
        self.animation_database = load_hero_animation_database()
        self.base_image = self.animation_database["base"]
        self.position = position - self.get_offset()
        self.anim = Animator2D(self.animation_database)
        self.render = Renderer2D(self.base_image)
        self.collider = Collider2D(self.position, HERO_WIDTH, HERO_HEIGHT)
        self.rigidBody = RigidBody2D(self.position, HERO_INITIAL_SPEED, HERO_JUMP_POWER, GRAVITY)

        self.facingRight = True
        self.canJump = False

    def get_offset(self):
        image_width = self.base_image.get_width()
        image_height = self.base_image.get_height()
        offset_width = (image_width - HERO_WIDTH) / 2
        offset_height = (image_height - HERO_HEIGHT)
        return Vector2(offset_width, offset_height)

    def move(self, right=True):
        self.rigidBody.move(right)
        self.anim.set_animation("run")
        self.facingRight = right

    def stop_moving(self):
        self.rigidBody.stop()
        if self.collider.onGround:
            self.anim.set_animation("idle")

    def stop_falling(self):
        self.rigidBody.velocity[1] = 0

    def jump(self):
        if self.canJump:
            self.rigidBody.jump()
            self.anim.set_animation("jump")

    def attack(self):
        self.anim.set_animation("attack")

    def handleGround(self):
        if self.collider.onGround:
            self.canJump = True
            self.stop_falling()

    def update(self, canvas, blocks):
        self.rigidBody.update()
        self.collider.rect.center = self.rigidBody.position
        self.collider.detect_blocks(blocks)
        self.handleGround()
        self.render.set_image(self.anim.next_frame(), self.facingRight)
        self.render.draw(canvas, self.collider.rect)
