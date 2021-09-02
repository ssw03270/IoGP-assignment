import pygame
import math
from . import Object

class Player(Object.Object):
    def __init__(self, x, y):
        # object information
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.direction = False
        self.move_speed = 2

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
        lis = []
        # state is idle
        for i in range(0, 6):
            lis.append(self.spr_idle.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move
        for i in range(0, 8):
            lis.append(self.spr_move.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move
        for i in range(0, 10):
            lis.append(self.spr_attack1.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move
        for i in range(0, 9):
            lis.append(self.spr_attack2.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move
        for i in range(0, 8):
            lis.append(self.spr_attack3.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        # return sprite
        if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
            self.spr_index = 0
        sprite = pygame.transform.scale(pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction, False), (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        self.spr_index += 1 / self.spr_speed
        return sprite

    def move(self):
        # get key pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.state_index = 1
            if keys[pygame.K_RIGHT]:
                self.x += self.move_speed
                if self.direction:
                    self.x = self.x + self.spr_width
                    self.direction = False
            if keys[pygame.K_LEFT]:
                self.x -= self.move_speed
                if not self.direction:
                    self.x = self.x - self.spr_width
                    self.direction = True
        else:
            self.state_index = 0
