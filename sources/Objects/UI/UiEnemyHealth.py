import pygame
import math
from sources.Objects import Object, Player

class UiEnemyHealth(Object.Object):
    def __init__(self, x, y, player = Player.Player, enemy_max_health = int):
        self.x = x
        self.y = y
        self.delta_time = 0
        self.enemy_max_health = enemy_max_health
        self.enemy_health = enemy_max_health

        # player information
        self.player = player
    def draw_image(self):
        sprite = pygame.draw.rect((255, 0, 0), [150, 10, 50, 20])
        return sprite