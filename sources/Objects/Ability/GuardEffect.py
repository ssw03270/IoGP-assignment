import pygame
import math, random
from sources.Objects import Object, Player

class GuardEffect(Object.Object):
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.delta_time = 0
        self.player = player

        # flower enemy image
        self.spr_guard_effect = pygame.image.load("../sprites/HeroKnight/GuardEffect.png").convert_alpha()        # 0
        self.spr_rotation = random.randrange(0, 360)

        # flower enemy sound
        self.sound_guard_effect = pygame.mixer.Sound("../sounds/Skeleton/Attack.mp3")

        # set sound volume
        self.sound_guard_effect.set_volume(0.2)

        self.spr_width = 250
        self.spr_height = 250
        self.spr_speed = 50
        self.spr_index = 0
        self.spr_size = 2/3
        self.spr_list = []

        self.set_sprite()

    def set_sprite(self):
        if self.player.direction:
            self.x -= 50
        else:
            self.x += 50
        self.y -= 20
        # state is idle
        for i in range(0, 4):
            self.spr_list.append(self.spr_guard_effect.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))

    def update(self):
        self.spr_index += 1 / self.spr_speed * self.delta_time

        if math.floor(self.spr_index) > len(self.spr_list) - 1:
            self.player.guard_effect.remove(self)

    def draw_image(self):
        sprite = pygame.transform.rotate(self.spr_list[math.floor(self.spr_index)], self.spr_rotation)
        sprite = pygame.transform.scale(sprite, (int(self.spr_width * self.spr_size), int(self.spr_height * self.spr_size)))
        return sprite

