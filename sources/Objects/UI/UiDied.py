import pygame
import math
from sources.Objects import Object, Player

class UiDied(Object.Object):
    def __init__(self, x, y, player = Player.Player):
        self.x = x
        self.y = y
        self.width = 720
        self.height = 540
        self.delta_time = 0

        # ui image
        self.spr_died = pygame.image.load("../sprites/ui/died.png").convert_alpha()    # 0

        # ui sound
        self.sound_died = pygame.mixer.Sound("../sounds/flowerEnemy/attack.mp3")

        # set sound volume
        self.sound_died.set_volume(0.5)

        # player information
        self.player = player

        # ui state
        self.state_index = 0

        # sprite information
        self.spr_width = 720
        self.spr_height = 540
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 1
        self.spr_list = []

        self.set_sprite()

    def set_sprite(self):
        lis = []
        # state is attack
        for i in range(0, 1):
            lis.append(self.spr_died.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        sprite = pygame.transform.scale(
            pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], False, False),
            (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        return sprite