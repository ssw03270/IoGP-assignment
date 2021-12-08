import pygame
import math, random
from sources.Objects import Object, Player
from sources.Objects.Enemy import King

class Sword(Object.Object):
    def __init__(self, x, y, direction, player = Player.Player, king = King):
        self.x = random.randrange(0, 720)
        self.y = 100
        self.speed = 0.6
        self.direction = (player.x - self.x, player.y - self.y)
        self.unit = math.sqrt(self.direction[0] * self.direction[0] + self.direction[1] * self.direction[1])
        self.direction_vector = (self.direction[0] / self.unit, self.direction[1] / self.unit)
        self.delta_time = 0
        self.max_distance = 32
        self.damage = 3

        # flower enemy image
        self.spr_star = pygame.image.load("../sprites/King/sword.png").convert_alpha()        # 0
        self.spr_rotation = math.atan2(self.direction[0], self.direction[1])*180/math.pi

        # flower enemy sound
        self.sound_star = pygame.mixer.Sound("../sounds/Skeleton/Attack.mp3")

        # set sound volume
        self.sound_star.set_volume(0.2)

        # check player detect
        self.player = player
        self.king = king

        self.spr_width = 32
        self.spr_height = 32
        self.spr_size = 3

        self.start_delay = 0
        self.start_max_delay = 1000

    def update(self):

        self.detected_player()

        self.start_delay += self.delta_time
        if self.start_delay >= self.start_max_delay:
            self.x += self.direction_vector[0] * self.speed * self.delta_time
            self.y += self.direction_vector[1] * self.speed * self.delta_time
        else:
            self.direction = (self.player.x - self.x, self.player.y - self.y)
            self.unit = math.sqrt(self.direction[0] * self.direction[0] + self.direction[1] * self.direction[1])
            self.direction_vector = (self.direction[0] / self.unit, self.direction[1] / self.unit)
            self.spr_rotation = math.atan2(self.direction_vector[0], self.direction_vector[1])*180/math.pi

    def draw_image(self):
        sprite = pygame.transform.scale(pygame.transform.rotate(self.spr_star, self.spr_rotation + 135), (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        return sprite

    def detected_player(self):
        distance_x = math.fabs(self.player.x - self.x)
        distance_y = math.fabs(self.player.y - self.y)
        if distance_x < self.max_distance and distance_y < self.max_distance:
            self.player.hit(self.damage)
            self.king.ability.remove(self)
