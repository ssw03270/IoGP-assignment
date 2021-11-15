import pygame
import math
from . import Object

class Player(Object.Object):
    def __init__(self, x, y):
        # object information
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.delta_time = 0
        self.real_x = self.x + 35
        self.health = 5
        self.attack_damage = 1

        # player image
        self.spr_idle = pygame.image.load("../sprites/player/idle.png").convert_alpha()         # 0
        self.spr_move = pygame.image.load("../sprites/player/move.png").convert_alpha()         # 1
        self.spr_attack1 = pygame.image.load("../sprites/player/attack1.png").convert_alpha()   # 2
        self.spr_attack2 = pygame.image.load("../sprites/player/attack2.png").convert_alpha()   # 3
        self.spr_attack3 = pygame.image.load("../sprites/player/attack3.png").convert_alpha()   # 4
        self.spr_hit = pygame.image.load("../sprites/player/hit.png").convert_alpha()           # 5
        self.spr_death = pygame.image.load("../sprites/player/death.png").convert_alpha()       # 6

        # player sound
        self.sound_walk = pygame.mixer.Sound("../sounds/player/walk.mp3")
        self.sound_attack1 = pygame.mixer.Sound("../sounds/player/attack1.mp3")
        self.sound_attack2 = pygame.mixer.Sound("../sounds/player/attack2.mp3")
        self.sound_attack3 = pygame.mixer.Sound("../sounds/player/attack3.mp3")

        # set sound volume
        self.sound_walk.set_volume(0.5)
        self.sound_attack1.set_volume(0.4)
        self.sound_attack2.set_volume(0.2)
        self.sound_attack3.set_volume(0.1)

        # playing background music
        pygame.mixer.music.load("../sounds/player/bgm.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05)

        # about sound
        self.is_move_sound_play = False

        # player move
        self.direction = False
        self.move_speed = 0.2
        self.is_move_able = True

        # player attack
        self.attack_range = 120
        self.attack_combo = 0
        self.attack_delay = 0
        self.attack_max_delay = 1000
        self.is_attack_able = True
        self.is_attacking = False

        # player hit
        self.hit_delay = 0
        self.hit_max_delay = 1000
        self.is_hit_able = True

        # player dash
        self.dash_point = 10
        self.dash_range = 0
        self.dash_max_range = 100
        self.dash_delay = 0
        self.dash_max_delay = 1000
        self.is_dash_able = True

        # player invincibility
        self.is_invincibility_able = False
        self.is_invincibility = False

        # player death
        self.is_player_death = False

        # player state
        self.state_index = 0

        # sprite information
        self.spr_width = 88
        self.spr_height = 30
        self.spr_speed = 80
        self.spr_index = 0
        self.spr_size = 3
        self.spr_list = []
        self.spr_x = self.x + self.spr_width / 2 * self.spr_size
        self.spr_y = self.x + self.spr_height / 2 * self.spr_size

        self.set_sprite()

    def update(self):
        if self.is_invincibility:
            print(self.is_invincibility)
        # attack delay counting
        self.attack_delay += self.delta_time
        # hit delay counting
        if not self.is_hit_able:
            self.hit_delay += self.delta_time
        if not self.is_dash_able:
            self.dash_delay += self.delta_time
        # if player doesn't death
        if not self.is_player_death:
            # player move
            self.move()
            self.dash()
        else:
            self.sound_walk.stop()

    def set_sprite(self):
        lis = []
        # state is idle
        for i in range(0, 6):
            lis.append(self.spr_idle.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move
        for i in range(0, 8):
            lis.append(self.spr_move.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack1
        for i in range(0, 10):
            lis.append(self.spr_attack1.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack2
        for i in range(0, 8):
            lis.append(self.spr_attack2.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack3
        for i in range(0, 9):
            lis.append(self.spr_attack3.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is hit
        for i in range(0, 6):
            lis.append(self.spr_hit.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death
        for i in range(0, 5):
            lis.append(self.spr_death.subsurface(0, i * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])

    def draw_image(self):
        # if player live, playing animation
        if not self.is_player_death:
            # if current index over than max index
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                # if player attack
                if 2 <= self.state_index and self.state_index <= 4:
                    self.state_index = 0
                    self.is_attack_able = True
                    self.is_move_able = True
                    self.is_attacking = False
                # if player hit
                elif self.state_index == 5:
                    self.state_index = 0
                    self.is_move_able = True
                self.spr_index = 0
            # update sprite
            sprite = pygame.transform.scale(
                pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction,
                                      False),
                (self.spr_width * self.spr_size, self.spr_height * self.spr_size))
            self.spr_index += 1 / self.spr_speed * self.delta_time

            return sprite

        # if player death
        else:
            # animation not finished
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

    def move(self):
        # if player doesn't death
        if not self.is_player_death:
            # player move
            keys = pygame.key.get_pressed()

            # if player move
            if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and self.is_move_able and not self.is_invincibility_able:
                self.state_index = 1

                # play foot step sound
                if not self.is_move_sound_play:
                    self.sound_walk.play(-1, 0, 1000)
                    self.is_move_sound_play = True

                if keys[pygame.K_RIGHT]:
                    self.x += self.move_speed * self.delta_time

                    if self.direction:
                        self.x = self.x + self.spr_width
                        self.direction = False
                        self.attack_range *= -1
                if keys[pygame.K_LEFT]:
                    self.x -= self.move_speed * self.delta_time
                    if not self.direction:
                        self.x = self.x - self.spr_width
                        self.direction = True
                        self.attack_range *= -1
            else:
                # set footstep sound
                self.sound_walk.fadeout(500)
                self.is_move_sound_play = False

                # set sprite idle
                if self.state_index == 1:
                    self.state_index = 0
                    self.is_attack_able = True

            # set spr x
            self.spr_x = self.x - 32
            self.spr_y = self.x

            if self.direction:
                self.spr_x += 88

    def attack(self):
        # if player doesn't death
        if not self.is_player_death:
            # check combo
            if self.attack_delay >= self.attack_max_delay:
                self.attack_delay = 0
                self.attack_combo = 0

            # player attack
            if self.is_attack_able:
                self.spr_index = 0

                if self.attack_combo == 0:
                    self.state_index = 2
                    self.attack_combo = 1
                    pygame.mixer.Sound.play(self.sound_attack1)

                elif self.attack_combo == 1:
                    self.state_index = 3
                    self.attack_combo = 2
                    pygame.mixer.Sound.play(self.sound_attack2)

                elif self.attack_combo == 2:
                    self.state_index = 4
                    self.attack_combo = 0
                    pygame.mixer.Sound.play(self.sound_attack3)

                self.is_move_able = False
                self.is_attack_able = False
                self.is_attacking = True
                self.attack_delay = 0

    def hit(self, damage):
        if not self.is_player_death and not self.is_invincibility:
            # check hit able
            if self.hit_delay >= self.hit_max_delay:
                self.hit_delay = 0
                self.is_hit_able = True

            if self.is_hit_able:
                self.state_index = 5
                self.spr_index = 0
                self.health -= damage
                self.is_hit_able = False
                self.is_move_able = False

            if self.health <= 0:
                self.state_index = 6
                self.spr_index = 0
                self.is_player_death = True

    def dash(self):
        if not self.is_player_death:
            # check dash able
            if self.dash_delay >= self.dash_max_delay:
                self.dash_delay = 0
                self.is_dash_able = True

            # if player dash
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LSHIFT]) and self.is_dash_able:
                self.is_dash_able = False
                self.is_invincibility = True
                self.is_invincibility_able = True
                self.dash_range = 0

            # invincibility time
            if self.is_invincibility_able:
                if not self.direction:
                    self.x += self.dash_point
                else:
                    self.x -= self.dash_point
                self.dash_range += self.dash_point

                # if dash range is over than max range
                if self.dash_range > self.dash_max_range:
                    self.is_invincibility_able = False
                    self.is_invincibility = False
