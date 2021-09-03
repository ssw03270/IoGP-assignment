import pygame
import math
from . import Object, Player

class UiHealth(Object.Object):
    def __init__(self, x, y, player = Player.Player, health_index = int):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.delta_time = 0
        self.health_index = health_index

        # ui image
        self.spr_health = pygame.image.load("../sprites/ui/health.png").convert_alpha()    # 0

        # ui sound
        self.sound_health_break = pygame.mixer.Sound("../sounds/flowerEnemy/attack.mp3")

        # set sound volume
        self.sound_health_break.set_volume(0.5)

        # player information
        self.player = player

        # ui state
        self.state_index = 0

        # sprite information
        self.spr_width = 32
        self.spr_height = 32
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 1
        self.spr_list = []

        self.set_sprite()

    def set_sprite(self):
        lis = []
        # state is attack
        for i in range(0, 6):
            lis.append(self.spr_health.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
            self.spr_index = len(self.spr_list[self.state_index]) - 1

        sprite = pygame.transform.scale(pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], False, False), (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        if self.player.health < self.health_index:
            self.spr_index += 1 / self.spr_speed * self.delta_time
        return sprite