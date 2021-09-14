import pygame
import math
from . import Object, Player

class Skeleton(Object.Object):
    def __init__(self, x, y, player = Player.Player):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.delta_time = 0
        self.real_x = self.x
        self.direction = False
        self.health = 10

        # flower enemy image
        self.spr_idle = pygame.image.load("../sprites/Skeleton/Idle.png").convert_alpha()        # 0
        self.spr_walk = pygame.image.load("../sprites/Skeleton/Walk.png").convert_alpha()        # 1
        self.spr_attack = pygame.image.load("../sprites/Skeleton/Attack.png").convert_alpha()    # 2
        self.spr_death = pygame.image.load("../sprites/Skeleton/Death.png").convert_alpha()      # 3
        self.spr_hit = pygame.image.load("../sprites/Skeleton/Hit.png").convert_alpha()          # 4

        # flower enemy sound
        self.sound_attack = pygame.mixer.Sound("../sounds/Skeleton/Attack.mp3")
        self.sound_death = pygame.mixer.Sound("../sounds/Skeleton/Death.mp3")
        self.sound_hit = pygame.mixer.Sound("../sounds/Skeleton/Hit.mp3")
        self.sound_walk = pygame.mixer.Sound("../sounds/Skeleton/Walk.mp3")

        # set sound volume
        self.sound_attack.set_volume(0.2)
        self.sound_death.set_volume(0.2)
        self.sound_hit.set_volume(0.2)
        self.sound_walk.set_volume(0.2)

        # check player detect
        self.player = player
        self.is_detected_player = False
        self.max_distance = 60

        # about move
        self.is_move_sound_play = False
        self.is_move = False
        self.is_move_able = True
        self.move_speed = 0.1
        self.move_delay = 0
        self.move_max_delay = 1000

        # flower enemy attack
        self.attack_delay = 0
        self.attack_max_delay = 1000
        self.is_attack_able = True
        self.damage = 2

        # flower enemy hit
        self.hit_delay = 0
        self.hit_max_delay = 1000
        self.is_hit_able = True

        # palyer death
        self.is_enemy_die = False

        # flower enemy state
        self.state_index = 0

        # sprite information
        self.spr_width = 150
        self.spr_height = 150
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 2
        self.spr_list = []
        self.spr_x = self.x
        self.spr_y = self.x

        self.set_sprite()

    def update(self):
        # hit delay counting
        if not self.is_hit_able:
            self.hit_delay += self.delta_time
        if not self.is_attack_able:
            self.attack_delay += self.delta_time
        if not self.is_move_able:
            self.move_delay += self.delta_time
        # if flower enemy doesn't death
        if not self.is_enemy_die:
            self.detected_player()
            self.move()

    def set_sprite(self):
        lis = []
        # state is idle
        for i in range(0, 4):
            lis.append(self.spr_idle.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is walk
        for i in range(0, 4):
            lis.append(self.spr_walk.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack
        for i in range(0, 8):
            lis.append(self.spr_attack.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death
        for i in range(0, 4):
            lis.append(self.spr_death.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is hit
        for i in range(0, 4):
            lis.append(self.spr_hit.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

    def draw_image(self):
        # if player live, playing animation
        if not self.is_enemy_die:
            # if current index over than max index
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                # if flower enemy attack
                if self.state_index == 2:
                    self.state_index = 0
                # if flower enemy hit
                elif self.state_index == 4:
                    self.state_index = 0
                self.spr_index = 0
            sprite = pygame.transform.scale(
                pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction,
                                      False),
                (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
            self.spr_index += 1 / self.spr_speed * self.delta_time
            return sprite

        # if flower enemy death
        else:
            if math.floor(self.spr_index) <= len(self.spr_list[self.state_index]) - 1:
                self.spr_index += 1 / self.spr_speed * self.delta_time
            # animation finished
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                self.spr_index = len(self.spr_list[self.state_index]) - 1
            # update sprite
            sprite = pygame.transform.scale(
                pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction,
                                      False),
                (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
            return sprite

    def attack(self):
        # if enemy flower doesn't death
        if not self.is_enemy_die:
            # check attack able
            if self.attack_delay >= self.attack_max_delay:
                self.attack_delay = 0
                self.is_attack_able = True

            # player attack
            if self.is_attack_able:
                self.state_index = 2
                pygame.mixer.Sound.play(self.sound_attack)
                self.is_attack_able = False
                self.player.hit(self.damage)

    def hit(self, damage):
        if not self.is_enemy_die:
            # check hit able
            if self.hit_delay >= self.hit_max_delay:
                self.hit_delay = 0
                self.is_hit_able = True
                self.is_move_able = True

            if self.is_hit_able:
                self.state_index = 4
                self.health -= damage
                self.is_hit_able = False
                self.sound_hit.play()
                self.move_delay = 0
                self.is_move_able = False
                self.attack_delay = 0
                self.is_attack_able = False

            if self.health <= 0:
                self.state_index = 3
                self.is_enemy_die = True
                self.sound_death.play()

    def detected_player(self):
        self.direction = self.player.spr_x < self.spr_x

        distance = math.fabs(self.player.spr_x - self.spr_x)
        self.is_detected_player = distance < self.max_distance

        if self.is_detected_player:
            self.is_move = False
            self.attack()
        else:
            self.is_move = True

        if self.player.is_attacking:
            if min(self.player.spr_x, self.player.spr_x + self.player.attack_range) < self.spr_x and self.spr_x < max(
                    self.player.spr_x, self.player.spr_x + self.player.attack_range):
                self.hit(self.player.attack_damage)

    def move(self):
        # move delay
        if self.move_delay >= self.move_max_delay:
            self.move_delay = 0
            self.is_move_able = True

        # if enemy is not attacking
        if self.is_move and self.is_move_able:
            # enemy move
            self.state_index = 1

            # enemy foot step sound
            if not self.is_move_sound_play:
                self.sound_walk.play(-1, 0, 1000)
                self.is_move_sound_play = True

            # player position is right
            if not self.direction:
                self.x += self.move_speed * self.delta_time
            # player position is left
            else:
                self.x -= self.move_speed * self.delta_time

            self.spr_x = self.x
        else:
            # set footstep sound
            self.sound_walk.fadeout(500)
            self.is_move_sound_play = False

            # set sprite idle
            if self.state_index == 1:
                self.state_index = 0