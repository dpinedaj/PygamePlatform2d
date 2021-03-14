class Animator2D:

    def __init__(self, animation_database):
        self.__animation_database = animation_database
        self.__current_animation = "idle"

        # Counters
        self.__anim_iter = 0

    def set_animation(self, anim):
        if anim != self.__current_animation:
            self.__current_animation = anim
            self.restart_iter()

    def restart_iter(self):
        self.__anim_iter = 0

    def next_frame(self):
        if self.__anim_iter == len(self.__animation_database[self.__current_animation]) - 1:
            self.restart_iter()
        else:
            self.__anim_iter += 1
        return self.__animation_database[self.__current_animation][self.__anim_iter]
