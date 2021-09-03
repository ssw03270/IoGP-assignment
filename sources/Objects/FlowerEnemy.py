import pygame
import math
from . import Object, Player

class FlowerEnemy(Object.Object):
    def __init__(self, x, y, player = Player.Player):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.delta_time = 0
        self.real_x = self.x
        self.direction = False

        # flower enemy image
        self.spr_attack = pygame.image.load("../sprites/flowerEnemy/attack.png").convert_alpha()    # 0
        self.spr_death = pygame.image.load("../sprites/flowerEnemy/death.png").convert_alpha()      # 1
        self.spr_hit = pygame.image.load("../sprites/flowerEnemy/hit.png").convert_alpha()          # 2
        self.spr_idle = pygame.image.load("../sprites/flowerEnemy/idle.png").convert_alpha()        # 3

        # flower enemy sound
        self.sound_attack = pygame.mixer.Sound("../sounds/flowerEnemy/attack.mp3")

        # set sound volume
        self.sound_attack.set_volume(0.5)

        # check player detect
        self.player = player
        self.is_detected_player = False
        self.max_distance = 30

        # flower enemy attack
        self.attack_delay = 0
        self.attack_max_delay = 5000
        self.is_attack_able = True
        self.damage = 2

        # flower enemy state
        self.state_index = 3

        # sprite information
        self.spr_width = 32
        self.spr_height = 32
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 3
        self.spr_list = []

        self.set_sprite()

    def update(self):
        if not self.is_attack_able:
            self.attack_delay += self.delta_time
        self.detected_player()

    def set_sprite(self):
        lis = []
        # state is attack
        for i in range(0, 12):
            lis.append(self.spr_attack.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death
        for i in range(0, 4):
            lis.append(self.spr_death.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is hit
        for i in range(0, 2):
            lis.append(self.spr_hit.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is idle
        for i in range(0, 5):
            lis.append(self.spr_idle.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        # if current index over than max index
        if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
            # if player attack
            if 0 == self.state_index:
                self.state_index = 3
            self.spr_index = 0

        sprite = pygame.transform.scale(pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction, False), (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
        self.spr_index += 1 / self.spr_speed * self.delta_time
        return sprite

    def attack(self):
        # check attack able
        if self.attack_delay >= self.attack_max_delay:
            self.attack_delay = 0
            self.is_attack_able = True

        # player attack
        if self.is_attack_able:
            self.state_index = 0
            pygame.mixer.Sound.play(self.sound_attack)
            self.is_attack_able = False
            self.player.hit(self.damage)

    def detected_player(self):
        self.direction = self.player.real_x < self.real_x

        distance = math.fabs(self.player.real_x - self.real_x)
        self.is_detected_player = distance < self.max_distance

        if self.is_detected_player:
            self.attack()