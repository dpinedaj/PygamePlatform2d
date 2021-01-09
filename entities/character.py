from .entity import *
from pygame.math import Vector2

# FIXME FIX THE BLOCKS BEHAVIOR; STILL SLIDING FOR WRONG LIMITS

# ANIMATION CONSTANTS
ATTACK_SUB_IMAGES = 6
IDLE_SUB_IMAGES = 4
RUN_SUB_IMAGES = 6
JUMP_SUB_IMAGES = 4
FALL_SUB_IMAGES = 2


class Character(Entity):

    def __init__(self, pos, images):
        super().__init__(pos, images)
        self.player_clock = pygame.time.Clock()

        # Redefine rect
        initial_width = self.rect.width
        initial_height = self.rect.height
        real_width = 45
        real_height = 90
        offset_width = (real_width - initial_width) / 2
        offset_height = (real_height - initial_height)
        self.rect.size = Vector2(real_width, real_height)
        self.offset = Vector2(offset_width, offset_height)

        # Animations
        self.idle_iter = 0
        self.attack_action = 0
        self.attack_iter = 0
        self.run_iter = 0
        self.jump_iter = 0
        self.fall_iter = 0

        # States
        self.facing_right = True
        self.is_attack = False
        self.on_ground = False
        self.is_running = False
        self.is_collided = False  # TODO testing

        # Constants
        self.jump_power = 50
        self.speed = 15

    # Util Functions
    @property
    def collider(self):
        return self.rect.topleft + self.offset

    def stop_moving(self):
        self.vx = 0

    def stop_falling(self):
        self.vy = self.jump_iter = self.fall_iter = 0
        self.on_ground = True

    def stop_jumping(self):
        self.vy = 0

    def apply_gravity(self, gravity):
        if not self.on_ground:
            self.vy += gravity

    # Animations Functions
    def idle_animation(self, canvas):
        self.player_clock.tick(5)
        canvas.blit(self.images['idle'][self.facing_right][self.idle_iter], self.collider)
        self.idle_iter = (self.idle_iter + 1) % IDLE_SUB_IMAGES

    def attack_animation(self, canvas):
        canvas.blit(self.images['attack'][self.attack_action][self.facing_right][self.attack_iter], self.collider)
        self.attack_iter += 1
        if self.attack_iter == ATTACK_SUB_IMAGES - 1:
            self.is_attack = False
            self.attack_action += 1
            self.attack_iter = 0

    def run_animation(self, canvas):
        canvas.blit(self.images['run'][self.facing_right][self.run_iter], self.collider)
        self.run_iter = (self.run_iter + 1) % RUN_SUB_IMAGES

    def jump_animation(self, canvas):
        if self.vy < 0:
            canvas.blit(self.images['jump'][self.facing_right][self.jump_iter], self.collider)
            self.jump_iter = self.jump_iter + 1 if self.jump_iter != JUMP_SUB_IMAGES - 1 else self.jump_iter
        elif self.vy >= 0:
            canvas.blit(self.images['fall'][self.facing_right][self.fall_iter], self.collider)
            self.fall_iter = self.fall_iter + 1 if self.fall_iter != FALL_SUB_IMAGES - 1 else 0

    def set_animation(self, canvas):
        if self.is_collided:
            self.draw_line_limit(canvas, (255, 0, 0))  # TODO testing
        else:
            self.draw_line_limit(canvas)  # TODO testing
        if self.is_attack:
            self.attack_animation(canvas)
        elif self.is_running:
            self.run_animation(canvas)
        elif not self.on_ground:
            self.jump_animation(canvas)
        else:
            self.idle_animation(canvas)

    # Action Functions
    def attack(self):
        self.is_attack = True
        if self.attack_action == len(self.images['attack']):
            self.attack_action = 0

    def jump(self):
        if self.on_ground:
            self.rect.y += 2  # Jump helps to smooth
            self.on_ground = False
            self.is_running = False
            self.vy = -1 * self.jump_power
            self.rect.y -= 2  # Jump helps to smooth

    def move(self, left=False):
        if left:
            self.facing_right = False
            self.vx = -self.speed

        else:
            self.facing_right = True
            self.vx = self.speed

    # Manage blockers and boundaries
    def check_movement(self):
        # Define if is moving horizontally
        if self.vx == 0 or not self.on_ground:
            self.is_running = False
        else:
            self.is_running = True

    def handle_world_boundaries(self, canvas, blocks):

        def detect_blocks():
            # Detect blocks
            block_collision = pygame.sprite.spritecollide(self, blocks, False)
            if len(block_collision) > 0:
                self.is_collided = True  # TODO testing
                for block in block_collision:
                    w_lim = block.rect.width / 2
                    h_lim = block.rect.height / 2
                    block.draw_line_limit(canvas)  # TODO testing

                    # Horizontal blocks
                    if self.rect.right >= block.rect.left \
                            and self.vx > 0 \
                            and self.rect.bottom - block.rect.top > w_lim \
                            and block.rect.bottom - self.rect.top > w_lim:
                        self.rect.right = block.rect.left
                        self.stop_moving()

                    elif self.rect.left <= block.rect.right \
                            and self.vx < 0 \
                            and self.rect.bottom - block.rect.top > w_lim \
                            and block.rect.bottom - self.rect.top > w_lim:
                        self.rect.left = block.rect.right
                        self.stop_moving()

                    # Vertical blocks
                    elif self.vy > 0 and -h_lim <= self.rect.bottom - block.rect.top <= h_lim:
                        self.rect.bottom = block.rect.top + 1  # This +1 is tricky to keep the ground
                        self.stop_falling()
                        self.on_block = True

                    elif self.vy < 0 and -h_lim <= block.rect.bottom - self.rect.top <= h_lim:
                        self.rect.top = block.rect.bottom
                        self.stop_jumping()

            else:
                self.is_collided = False  # TODO testing
                self.on_ground = False

        def detect_canvas_limit():
            if self.rect.right >= canvas.get_width():
                self.rect.right = canvas.get_width()

            elif self.rect.left <= 0:
                self.rect.left = 0
            # Canvas floor limit
            canvas_floor_condition = self.rect.bottom >= canvas.get_height()

            if canvas_floor_condition:
                self.rect.bottom = canvas.get_height()
                self.stop_falling()

        if blocks is not None:
            detect_blocks()
        detect_canvas_limit()

    def handle_movements(self, canvas, blocks):
        self.rect.y += self.vy
        self.rect.x += self.vx

        self.check_movement()
        self.handle_world_boundaries(canvas, blocks)

    # Update frame by frame
    def update(self, canvas, blocks=None):
        self.apply_gravity(5)
        self.handle_movements(canvas, blocks)
        self.set_animation(canvas)
