import pygame
import math, random
from sources.Objects import Object, Player
from sources.Objects.Enemy import Skeleton

class EvilWizard(Object.Object):
    def __init__(self, x, y, player = Player.Player):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20
        self.delta_time = 0
        self.real_x = self.x
        self.direction = False
        self.max_health = 20
        self.health = self.max_health
        self.name = "Evil Wizard"
        self.ability = []

        # flower enemy image
        self.spr_idle = pygame.image.load("../sprites/EvilWizard/Idle.png").convert_alpha()        # 0
        self.spr_walk = pygame.image.load("../sprites/EvilWizard/Run.png").convert_alpha()         # 1
        self.spr_attack1 = pygame.image.load("../sprites/EvilWizard/Attack1.png").convert_alpha()  # 2
        self.spr_attack2 = pygame.image.load("../sprites/EvilWizard/Attack2.png").convert_alpha()  # 3
        self.spr_death = pygame.image.load("../sprites/EvilWizard/Death.png").convert_alpha()      # 4
        self.spr_hit = pygame.image.load("../sprites/EvilWizard/Hit.png").convert_alpha()          # 5

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
        self.max_near_distance = 100

        # about move
        self.is_move_sound_play = False
        self.is_move = False
        self.is_move_able = True
        self.move_speed = 0.2
        self.move_delay = 0
        self.move_max_delay = 1000

        # flower enemy attack
        self.attack_delay = 0
        self.attack_max_delay = 3000
        self.attack_combo = 0
        self.attack_max_combo = 1
        self.is_attack_able = True
        self.damage = 1

        # flower enemy hit
        self.hit_delay = 0
        self.hit_max_delay = 500
        self.is_hit_able = True

        # ability
        self.ability_delay = 0
        self.ability_max_delay = 10000

        # palyer death
        self.is_enemy_die = False

        # flower enemy state
        self.state_index = 0

        # sprite information
        self.spr_width = 250
        self.spr_height = 250
        self.spr_speed = 100
        self.spr_index = 0
        self.spr_size = 1.5
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
        self.ability_delay += self.delta_time
        # if flower enemy doesn't death
        if not self.is_enemy_die:
            self.detected_player()
            self.move()
            self.use_ability()
        for skeleton in self.ability:
            skeleton.update()

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
        for i in range(0, 8):
            lis.append(self.spr_attack1.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack2
        for i in range(0, 8):
            lis.append(self.spr_attack2.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death
        for i in range(0, 7):
            lis.append(self.spr_death.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is hit
        for i in range(0, 3):
            lis.append(self.spr_hit.subsurface(i * self.spr_width, 0, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

    def draw_image(self):
        # if player live, playing animation
        if not self.is_enemy_die:
            if self.state_index >= 2 and self.state_index <= 3:
                if math.floor(self.spr_index) > (len(self.spr_list[self.state_index]) - 1) / 2:
                    self.player.hit(self.damage)

            # if current index over than max index
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                # if flower enemy attack
                if self.state_index >= 2 and self.state_index <= 3:
                    self.state_index = 0
                # if flower enemy hit
                elif self.state_index == 5:
                    self.state_index = 0
                self.spr_index = 0
            sprite = pygame.transform.scale(
                pygame.transform.flip(self.spr_list[self.state_index][math.floor(self.spr_index)], self.direction,
                                      False),
                (int(self.spr_width * self.spr_size), int(self.spr_height * self.spr_size)))
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
                (int(self.spr_width * self.spr_size), int(self.spr_height * self.spr_size)))
            return sprite

    def attack(self, is_near):
        # if enemy flower doesn't death
        if not self.is_enemy_die:
            # check attack able
            if self.attack_delay >= self.attack_max_delay:
                self.attack_delay = 0
                self.is_attack_able = True
                self.is_move_able = True

            # player attack
            if self.is_attack_able:
                if self.attack_combo < self.attack_max_combo:
                    self.attack_max_delay = 750
                elif self.attack_combo == self.attack_max_combo:
                    self.attack_max_delay = 3000

                self.state_index = self.attack_combo + 2
                self.attack_combo += 1
                if self.attack_combo > self.attack_max_combo:
                    self.attack_combo = 0

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
                self.state_index = 5
                self.spr_index = 0
                self.health -= damage
                self.is_hit_able = False
                self.sound_hit.play()
                self.move_delay = 0
                self.is_move_able = False
                self.is_attack_able = False
                self.attack_delay = 0

            if self.health <= 0:
                self.state_index = 4
                self.spr_index = 0
                self.is_enemy_die = True
                self.sound_death.play()

                for skeleton in self.ability:
                    skeleton.hit(10000)

    def detected_player(self):
        if self.is_move_able:
            self.direction = self.player.x < self.x

        distance = math.fabs(self.player.x - self.x)
        self.is_detected_near_player = distance < self.max_near_distance

        if self.is_detected_near_player:
            self.is_move = False
            self.attack(self.is_detected_near_player)
        else:
            self.is_move = True
            self.attack_combo = 0

        if self.player.is_attacking:
            if min(self.player.x, self.player.x + self.player.attack_range) < self.x and self.x < max(
                    self.player.x, self.player.x + self.player.attack_range):

                if self.player.is_attacking_state:
                    if math.floor(self.player.spr_index) > (len(self.player.spr_list[self.player.state_index]) - 1) / 2:
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

    def use_ability(self):
        if not self.is_enemy_die:
            if not self.state_index == 2 and not self.state_index == 3:
                if self.ability_delay > self.ability_max_delay:
                    if not self.direction:
                        self.ability.append(Skeleton.Skeleton(800, 385, self.player))
                    else:
                        self.ability.append(Skeleton.Skeleton(-50, 385, self.player))
                    self.ability_delay = 0