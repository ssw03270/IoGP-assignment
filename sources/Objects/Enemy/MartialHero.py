import pygame
import math, random
from sources.Objects import Object, Player
from sources.Objects.Ability import Star

class MartialHero(Object.Object):
    def __init__(self, x, y, player = Player.Player):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.delta_time = 0
        self.real_x = self.x
        self.direction = False
        self.max_health = 10
        self.health = self.max_health
        self.name = "Martial Hero"
        self.ability = []

        # flower enemy image
        self.spr_idle = pygame.image.load("../sprites/MartialHero/Idle.png").convert_alpha()        # 0
        self.spr_walk = pygame.image.load("../sprites/MartialHero/Run.png").convert_alpha()         # 1
        self.spr_attack1 = pygame.image.load("../sprites/MartialHero/Attack1.png").convert_alpha()  # 2
        self.spr_attack2 = pygame.image.load("../sprites/MartialHero/Attack2.png").convert_alpha()  # 3
        self.spr_attack3 = pygame.image.load("../sprites/MartialHero/Attack3.png").convert_alpha()  # 4
        self.spr_death = pygame.image.load("../sprites/MartialHero/Death.png").convert_alpha()      # 5
        self.spr_hit = pygame.image.load("../sprites/MartialHero/Hit.png").convert_alpha()          # 6

        # flower enemy sound
        self.sound_attack = pygame.mixer.Sound("../sounds/Skeleton/Attack.mp3")
        self.sound_death = pygame.mixer.Sound("../sounds/Skeleton/Death.mp3")
        self.sound_hit = pygame.mixer.Sound("../sounds/Skeleton/Hit.mp3")
        self.sound_walk = pygame.mixer.Sound("../sounds/Skeleton/Walk.mp3")

        # set sound volume
        self.sound_attack.set_volume(0.2)
        self.sound_death.set_volume(0.2)
        self.sound_hit.set_volume(0.1)
        self.sound_walk.set_volume(0.2)

        # check player detect
        self.player = player
        self.is_detected_near_player = False
        self.is_detected_far_player = False
        self.max_near_distance = 100
        self.min_far_distance = 200
        self.max_far_distance = 400

        # about move
        self.is_move_sound_play = False
        self.is_move = False
        self.is_move_able = True
        self.move_speed = 0.3
        self.move_delay = 0
        self.move_max_delay = 1000

        # dash
        self.dash_point = 15
        self.dash_range = 0
        self.dash_max_range = 200
        self.dash_delay = 0
        self.dash_max_delay = 10000
        self.is_dash_able = True

        # flower enemy attack
        self.attack_delay = 0
        self.attack_max_delay = 2000
        self.is_attack_able = False
        self.damage = 1

        # flower enemy hit
        self.hit_delay = 0
        self.hit_max_delay = 500
        self.is_hit_able = True

        # palyer death
        self.is_enemy_die = False

        # flower enemy state
        self.state_index = 0

        # sprite information
        self.spr_width = 200
        self.spr_height = 200
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
        if not self.is_dash_able:
            self.dash_delay += self.delta_time
        # if flower enemy doesn't death
        if not self.is_enemy_die:
            self.detected_player()
            self.move()
            self.dash()
        for star in self.ability:
            star.update()

    def set_sprite(self):
        lis = []
        # state is idle
        for i in range(0, 8):
            lis.append(self.spr_idle.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is walk
        for i in range(0, 8):
            lis.append(self.spr_walk.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack1
        for i in range(0, 6):
            lis.append(self.spr_attack1.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack2
        for i in range(0, 6):
            lis.append(self.spr_attack2.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack3
        for i in range(0, 6):
            lis.append(self.spr_attack3.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death
        for i in range(0, 6):
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
            if self.state_index >= 2 and self.state_index <= 4:
                if math.floor(self.spr_index) > (len(self.spr_list[self.state_index]) - 1) / 2:
                    if self.state_index <= 3:
                        self.player.hit(self.damage)
                    else:
                        if len(self.ability) < 1:
                            self.ability.append(Star.Star(self.x, self.y, self.direction, self.player, self))
            # if current index over than max index
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                # if flower enemy attack
                if self.state_index >= 2 or self.state_index <= 4:
                    self.state_index = 0
                # if flower enemy hit
                elif self.state_index == 6:
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

    def attack(self, is_far, is_near):
        # if enemy flower doesn't death
        if not self.is_enemy_die:
            # check attack able
            if self.attack_delay >= self.attack_max_delay:
                self.attack_delay = 0
                self.is_attack_able = True
                self.is_move_able = True

            # player attack
            if self.is_attack_able:
                if is_near:
                    self.state_index = random.randrange(2, 4)
                elif is_far:
                    self.state_index = 4
                self.spr_index = 0
                pygame.mixer.Sound.play(self.sound_attack)
                self.is_attack_able = False
                self.is_move_able = False

    def hit(self, damage):
        if not self.is_enemy_die:
            # check hit able
            if self.hit_delay >= self.hit_max_delay:
                self.hit_delay = 0
                self.is_hit_able = True
                self.is_move_able = True

            if self.is_hit_able:
                self.state_index = 6
                self.spr_index = 0
                self.health -= damage
                self.is_hit_able = False
                self.sound_hit.play()
                self.move_delay = 0
                self.is_move_able = False
                self.is_attack_able = False

            if self.health <= 0:
                self.state_index = 5
                self.spr_index = 0
                self.is_enemy_die = True
                self.sound_death.play()

    def detected_player(self):
        if self.is_move_able:
            self.direction = self.player.x < self.x

        distance = math.fabs(self.player.x - self.x)
        self.is_detected_far_player = distance < self.max_far_distance and self.min_far_distance < distance
        self.is_detected_near_player = distance < self.max_near_distance

        if self.is_detected_far_player or self.is_detected_near_player:
            self.is_move = False
            self.attack(self.is_detected_far_player, self.is_detected_near_player)
        else:
            self.is_move = True

        if self.player.is_attacking:
            if min(self.player.x, self.player.x + self.player.attack_range) < self.x and self.x < max(
                    self.player.x, self.player.x + self.player.attack_range):
                self.hit(self.player.attack_damage)
                self.player.is_attacking = False

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

    def dash(self):
        if not self.is_enemy_die:
            # check dash able
            if self.dash_delay >= self.dash_max_delay:
                self.dash_delay = 0
                self.is_dash_able = True

            # if dash
            if self.is_dash_able:
                self.is_dash_able = False
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