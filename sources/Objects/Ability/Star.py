import pygame
import math, random
from sources.Objects import Object, Player
from sources.Objects.Enemy import MartialHero

class Star(Object.Object):
    def __init__(self, x, y, direction, player = Player.Player, martial_hero = MartialHero):
        self.x = x
        self.y = y
        self.speed = 0.3
        self.direction = direction
        self.delta_time = 0
        self.max_distance = 50
        self.damage = 3

        # flower enemy image
        self.spr_star = pygame.image.load("../sprites/MartialHero/Star.png").convert_alpha()        # 0
        self.spr_rotation = 0

        # flower enemy sound
        self.sound_star = pygame.mixer.Sound("../sounds/Skeleton/Attack.mp3")

        # set sound volume
        self.sound_star.set_volume(0.2)

        # check player detect
        self.player = player
        self.martial_hero = martial_hero

        self.spr_width = 50
        self.spr_height = 50
        self.spr_size = 2

    def update(self):
        if not self.direction:
            self.x += self.speed * self.delta_time
        else:
            self.x -= self.speed * self.delta_time

        self.detected_player()

    def draw_image(self):
        sprite = pygame.transform.rotate(self.spr_star, self.spr_rotation)
        self.spr_rotation += self.delta_time
        if self.spr_rotation > 360:
            self.spr_rotation = 0
        return sprite

    def detected_player(self):
        distance_x = math.fabs(self.player.x - self.x)
        distance_y = math.fabs(self.player.y - self.y)
        if distance_x < self.max_distance and distance_y < self.max_distance:
            self.player.hit(self.damage)
            self.martial_hero.ability.remove(self)
