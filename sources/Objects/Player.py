import pygame
from . import Object

class Player(Object.Object):
    def __init__(self, x, y):
        # object position
        self.x = x
        self.y = y

        # player image
        self.spr_idle = pygame.image.load("../sprites/player/idle.png").convert_alpha()     # 0
        self.spr_move = pygame.image.load("../sprites/player/move.png").convert_alpha()     # 1
        self.spr_attack1 = pygame.image.load("../sprites/player/attack1.png").convert_alpha() # 2
        self.spr_attack2 = pygame.image.load("../sprites/player/attack2.png").convert_alpha() # 3
        self.spr_attack3 = pygame.image.load("../sprites/player/attack3.png").convert_alpha() # 4

        # player state
        self.state_index = 0

        # sprite information
        self.spr_width = 88
        self.spr_height = 30
        self.spr_speed = 5
        self.spr_index = 0
        self.spr_size = 3
        self.spr_list = []

        self.set_sprite()

    def set_sprite(self):
        # if state is idle
        if self.state_index == 0:
            for i in range(0, 6):
                self.spr_list.append(self.spr_idle.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))

        # if state is move
        elif self.state_index == 1:
            for i in range(0, 8):
                self.spr_list.append(self.spr_move.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))

        # if state is move
        elif self.state_index == 2:
            for i in range(0, 10):
                self.spr_list.append(self.spr_attack1.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))

        # if state is move
        elif self.state_index == 3:
            for i in range(0, 9):
                self.spr_list.append(self.spr_attack2.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))

        # if state is move
        elif self.state_index == 4:
            for i in range(0, 8):
                self.spr_list.append(self.spr_attack3.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))

    def draw_image(self):
        # return sprite
        sprite = pygame.transform.scale(self.spr_list[self.spr_index], (self.spr_width * self.spr_size, self.spr_height * self.spr_size))

        self.spr_index += 1
        if self.spr_index > len(self.spr_list) - 1:
            self.spr_index = 0

        return sprite