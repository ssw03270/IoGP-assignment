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
        self.delta_time = 0

        # player image
        self.spr_idle = pygame.image.load("../sprites/player/idle.png").convert_alpha()     # 0
        self.spr_move = pygame.image.load("../sprites/player/move.png").convert_alpha()     # 1
        self.spr_attack1 = pygame.image.load("../sprites/player/attack1.png").convert_alpha() # 2
        self.spr_attack2 = pygame.image.load("../sprites/player/attack2.png").convert_alpha() # 3
        self.spr_attack3 = pygame.image.load("../sprites/player/attack3.png").convert_alpha() # 4

        # player move
        self.direction = False
        self.move_speed = 0.2
        self.is_move_able = True

        # player attack
        self.attack_combo = 0
        self.attack_delay = 0
        self.attack_max_delay = 1000
        self.is_attack_able = True

        # player state
        self.state_index = 0

        # sprite information
        self.spr_width = 88
        self.spr_height = 30
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 3
        self.spr_list = []

        self.set_sprite()

    def update(self):
        self.attack_delay += self.delta_time

        # player move
        self.move()

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

        # state is attack1
        for i in range(0, 10):
            lis.append(self.spr_attack1.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack2
        for i in range(0, 8):
            lis.append(self.spr_attack2.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack3
        for i in range(0, 9):
            lis.append(self.spr_attack3.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        # if current index over than max index
        if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
            # if player attack
            if 2 <= self.state_index and self.state_index <= 4:
                self.state_index = 0
                self.is_attack_able = True
                self.is_move_able = True
            self.spr_index = 0

        sprite = pygame.transform.scale(pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction, False), (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        self.spr_index += 1 / self.spr_speed * self.delta_time
        return sprite

    def move(self):
        # player move
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and self.is_move_able:
            self.state_index = 1
            if keys[pygame.K_RIGHT]:
                self.x += self.move_speed * self.delta_time

                if self.direction:
                    self.x = self.x + self.spr_width
                    self.direction = False
            if keys[pygame.K_LEFT]:
                self.x -= self.move_speed * self.delta_time
                if not self.direction:
                    self.x = self.x - self.spr_width
                    self.direction = True
        else:
            if self.state_index == 1:
                self.state_index = 0
                self.is_attack_able = True

    def attack(self):
        # check combo
        if self.attack_delay >= self.attack_max_delay:
            self.attack_delay = 0
            self.attack_combo = 0

        # player attack
        if self.is_attack_able:
            if self.attack_combo == 0:
                self.state_index = 2
                self.attack_combo = 1

            elif self.attack_combo == 1:
                self.state_index = 3
                self.attack_combo = 2

            elif self.attack_combo == 2:
                self.state_index = 4
                self.attack_combo = 0

            self.is_move_able = False
            self.is_attack_able = False
            self.attack_delay = 0

