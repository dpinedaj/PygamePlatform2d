from pygame import Vector2


class RigidBody2D:
    def __init__(self, position, speed, jump_power, gravity):
        self.position = position

        self.velocity = Vector2()

        self.__speed = speed
        self.__jump_power = -jump_power
        self.__gravity = gravity

    def move(self, right):
        if right:
            self.velocity[0] = self.speed
        else:
            self.velocity[0] = - self.speed

    def stop(self):
        self.velocity = Vector2()

    def jump(self):
        self.position[1] -= 5  # Jump helps to smooth
        self.velocity[1] = self.__jump_power
        self.position[1] += 5  # Jump helps to smooth

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def jump_power(self):
        return self.__jump_power

    @jump_power.setter
    def jump_power(self, jump_power):
        self.__jump_power = jump_power

    @property
    def gravity(self):
        return self.__gravity

    @gravity.setter
    def gravity(self, gravity):
        self.__gravity = gravity

    def apply_gravity(self):
        self.velocity[1] += self.__gravity

    def update(self):
        self.apply_gravity()
        self.position += self.velocity

