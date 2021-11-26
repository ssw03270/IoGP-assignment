import pygame
import math
from sources.Objects import Object, Player

class Button(Object.Object):
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title

        # sprite information
        self.spr_width = 34
        self.spr_height = 10
        self.spr_size = 5

        # ui image
        self.spr_button = pygame.image.load("../sprites/ui/Button.png").convert_alpha()    # 0

    def draw_image(self):
        sprite = self.spr_button.subsurface(0, 0, self.spr_width, self.spr_height)
        sprite = pygame.transform.scale(
            pygame.transform.flip(sprite, False, False),
            (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        return sprite