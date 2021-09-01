import pygame
from . import Object

class Player(Object.Object):
    def __init__(self):
        super().__init__()

        # player image
        self.spr_idle = pygame.image.load("../sprites/player/idle.png").convert()
        self.spr_move = pygame.image.load("../sprites/player/move.png").convert()

        # player state
        # 0 : idle
        # 1 : move
        self.state = 0

    def draw_image(self, index):
        if self.state == 0:
            return self.spr_idle

        elif self.state == 1:
            return self.spr_move