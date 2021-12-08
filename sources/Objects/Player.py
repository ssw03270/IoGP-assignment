import pygame
import math
from . import Object
from .Ability import GuardEffect

class Player(Object.Object):
    def __init__(self, x, y):
        # object information
        self.x = x
        self.y = y
        self.width = 44
        self.height = 10
        self.delta_time = 0
        self.real_x = self.x

        self.max_health = 20
        self.health = self.max_health
        self.max_energy = 200
        self.energy = self.max_energy
        self.attack_damage = 1

        # player image
        self.spr_idle = pygame.image.load("../sprites/HeroKnight/Idle.png").convert_alpha()         # 0
        self.spr_move = pygame.image.load("../sprites/HeroKnight/Run.png").convert_alpha()          # 1
        self.spr_dash = pygame.image.load("../sprites/HeroKnight/Dash.png").convert_alpha()         # 2
        self.spr_attack = pygame.image.load("../sprites/HeroKnight/Attack.png").convert_alpha()     # 3
        self.spr_attack = pygame.image.load("../sprites/HeroKnight/Attack.png").convert_alpha()     # 4
        self.spr_attack = pygame.image.load("../sprites/HeroKnight/Attack.png").convert_alpha()     # 5
        self.spr_hit = pygame.image.load("../sprites/HeroKnight/Hit.png").convert_alpha()           # 6
        self.spr_death = pygame.image.load("../sprites/HeroKnight/Death.png").convert_alpha()       # 7
        self.spr_jump = pygame.image.load("../sprites/HeroKnight/Jump.png").convert_alpha()         # 8
        self.spr_fall = pygame.image.load("../sprites/HeroKnight/Fall.png").convert_alpha()         # 9
        self.spr_guard = pygame.image.load("../sprites/HeroKnight/Guard.png").convert_alpha()         # 10

        self.spr_player_sprite_sheet = pygame.image.load("../sprites/player/PlayerSpriteSheet.png").convert_alpha() # 8

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
        self.attack_range = 100

        self.attack_combo = 0
        self.attack_max_combo = 2
        self.attack_delay = 450
        self.attack_max_delay = 450
        self.attack_normal_max_delay = 450
        self.attack_combo_max_delay = 2000

        self.punch_combo = 0
        self.punch_max_combo = 1000
        self.punch_delay = 10000
        self.punch_max_delay = 10000
        self.punch_energy = 0.2

        self.kick_combo = 0
        self.kick_max_combo = 1
        self.kick_delay = 450
        self.kick_max_delay = 450
        self.kick_normal_max_delay = 450
        self.kick_combo_max_delay = 2000

        self.is_attack_able = True
        self.is_attacking = False
        self.attack_energy = 1

        # player hit
        self.hit_delay = 0
        self.hit_max_delay = 500
        self.is_hit_able = True

        # player dash
        self.dash_point = 15
        self.dash_range = 0
        self.dash_max_range = 200
        self.dash_delay = 0
        self.dash_max_delay = 1000
        self.is_dash_able = True
        self.dash_energy = 5

        # player jump
        self.is_jump_able = True
        self.jump_speed = 100
        self.jump_point = 0
        self.jump_start_point = self.y
        self.jump_max_range = math.sin(math.pi) * self.jump_speed
        self.jump_energy = 3

        # player invincibility
        self.is_invincibility_able = False
        self.is_invincibility = False

        # player death
        self.is_player_death = False

        # player guard
        self.is_guard_on = False
        self.guard_energy = 2
        self.guard_effect = []

        # player state
        self.state_index = 0

        # sprite information
        self.spr_width = 50
        self.spr_height = 37
        self.spr_speed = 80
        self.spr_index = 0
        self.spr_size = 3
        self.spr_list = []
        self.spr_x = self.x + self.spr_width / 2 * self.spr_size
        self.spr_y = self.x + self.spr_height / 2 * self.spr_size

        self.set_sprite()

        self.is_attacking_state = False

    def update(self):
        # attack delay counting
        self.attack_delay += self.delta_time
        self.punch_delay += self.delta_time
        self.kick_delay += self.delta_time
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
            self.punch()
        else:
            self.sound_walk.stop()
        # energy
        self.energy += 1 / self.delta_time * 2
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        elif self.energy < 0:
            self.energy = 0

        if self.is_guard_on:
            self.energy -= self.guard_energy / self.delta_time
            if self.energy < self.guard_energy / self.delta_time:
                self.guard_off()

        for guard_effect in self.guard_effect:
            guard_effect.update()

        self.is_attacking_state = (3 <= self.state_index and self.state_index <= 5) or (11 == self.state_index) or (12 <= self.state_index and self.state_index <= 13)
    def set_sprite(self):
        lis = []

        # state is idle 0
        for i in range(0, 4):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 0 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is move 1
        for i in range(0, 6):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 2 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is dash 2
        for i in range(0, 2):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 6 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack1 3
        for i in range(0, 5):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 11 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack2 4
        for i in range(0, 6):
            lis.append(
                self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 12 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is attack3 5
        for i in range(0, 6):
            lis.append(
                self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 13 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is hit 6
        for i in range(0, 3):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 14 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is death 7
        for i in range(0, 7):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 15 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is jump 8
        for i in range(0, 4):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 3 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is fall 9
        for i in range(0, 2):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 5 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is guard 10
        for i in range(0, 4):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 0 * self.spr_height, self.spr_width, self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is punch 11
        for i in range(0, 12):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 29 * self.spr_height, self.spr_width,
                                                               self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is kick 12
        for i in range(0, 4):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 31 * self.spr_height, self.spr_width,
                                                               self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

        # state is kick 13
        for i in range(4, 8):
            lis.append(self.spr_player_sprite_sheet.subsurface(i * self.spr_width, 31 * self.spr_height, self.spr_width,
                                                               self.spr_height))
        self.spr_list.append(lis[:])
        lis.clear()

    def draw_image(self):
        # if player live, playing animation
        if not self.is_player_death:
            # if current index over than max index
            if math.floor(self.spr_index) > len(self.spr_list[self.state_index]) - 1:
                # if player attack
                if self.is_attacking_state:
                    self.state_index = 0
                    self.is_move_able = True
                    self.is_attacking = False
                # if player hit
                elif self.state_index == 6:
                    self.state_index = 0
                    self.is_move_able = True
                elif self.state_index == 0:
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
            self.state_index = 7
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

            # player jump
            if not self.is_jump_able and not self.is_guard_on:
                self.y = self.jump_start_point + -1 * math.sin(self.jump_point) * self.jump_speed
                self.jump_point += math.pi / self.delta_time * 2

                if self.jump_point < math.pi / 2:
                    if not self.state_index == 2 and not self.is_attacking_state and not self.state_index == 6:
                        self.state_index = 8
                elif self.jump_point > math.pi / 2:
                    if not self.state_index == 2 and not self.is_attacking_state and not self.state_index == 6:
                        self.state_index = 9

            if self.jump_point >= math.pi:
                print(self.y)
                self.is_jump_able = True
                self.jump_point = 0
                self.y = self.jump_start_point
                print(self.jump_start_point)
                if self.state_index == 8 or self.state_index == 9:
                    self.state_index = 0

            # player move
            keys = pygame.key.get_pressed()

            # if player move
            if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and self.is_move_able and not self.is_invincibility_able and not self.is_guard_on:
                if not self.state_index == 8 and not self.state_index == 9:
                    self.state_index = 1

                # play foot step sound
                if not self.is_move_sound_play:
                    self.sound_walk.play(-1, 0, 1000)
                    self.is_move_sound_play = True

                if keys[pygame.K_RIGHT]:
                    if self.x <= 720:
                        self.x += self.move_speed * self.delta_time
                    if self.direction:
                        self.direction = False
                        self.attack_range *= -1
                if keys[pygame.K_LEFT]:
                    if self.x >= 0:
                        self.x -= self.move_speed * self.delta_time
                    if not self.direction:
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

            if self.attack_delay >= self.attack_max_delay:
                self.attack_delay = 0
                self.is_attack_able = True

            # player attack
            if self.is_attack_able and not self.is_guard_on and self.energy >= self.attack_energy:
                self.spr_index = 0
                self.state_index = 3 + self.attack_combo
                self.attack_combo += 1
                self.attack_max_delay = self.attack_normal_max_delay
                if self.attack_combo > self.attack_max_combo:
                    self.attack_combo = 0
                    self.attack_max_delay = self.attack_combo_max_delay

                pygame.mixer.Sound.play(self.sound_attack1)
                self.energy -= self.attack_energy

                self.is_move_able = False
                self.is_attack_able = False
                self.is_attacking = True
                self.attack_delay = 0

    def punch(self):
        # if player doesn't death
        if not self.is_player_death:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:

                if self.punch_delay >= self.punch_max_delay:
                    self.punch_delay = 0
                    self.is_attack_able = True
                    self.spr_index = 0
                    self.state_index = 11

                # player attack
                if self.is_attack_able and not self.is_guard_on and self.energy >= self.attack_energy:
                    self.punch_combo += self.delta_time

                    self.is_move_able = False
                    self.is_attacking = True

                    if self.punch_combo > self.punch_max_combo:
                        self.punch_combo = 0
                        self.punch_delay = 0
                        self.is_attack_able = False


                    pygame.mixer.Sound.play(self.sound_attack1)
                    self.energy -= self.punch_energy

    def punch_end(self):
        if self.punch_delay >= self.punch_max_delay and self.punch_combo <= self.punch_max_combo:
            self.punch_combo = 0

            self.is_move_able = False
            self.is_attack_able = False
            self.is_attacking = True
            self.punch_delay = 0

    def kick(self):
        # if player doesn't death
        if not self.is_player_death:

            if self.kick_delay >= self.kick_max_delay:
                self.kick_delay = 0
                self.is_attack_able = True

            # player attack
            if self.is_attack_able and not self.is_guard_on and self.energy >= self.attack_energy:
                self.spr_index = 0
                self.state_index = 12 + self.kick_combo
                self.kick_combo += 1
                self.kick_max_delay = self.kick_normal_max_delay
                if self.kick_combo > self.kick_max_combo:
                    self.kick_combo = 0
                    self.kick_max_delay = self.kick_combo_max_delay

                pygame.mixer.Sound.play(self.sound_attack1)
                self.energy -= self.attack_energy

                self.is_move_able = False
                self.is_attack_able = False
                self.is_attacking = True

    def hit(self, damage):
        if not self.is_player_death and not self.is_invincibility:
            # check hit able
            if self.hit_delay >= self.hit_max_delay:
                self.hit_delay = 0
                self.is_hit_able = True

            if self.is_hit_able and not self.is_guard_on:
                self.state_index = 6
                self.spr_index = 0
                self.health -= damage
                self.is_hit_able = False
                self.is_move_able = False

            if self.is_hit_able and self.is_guard_on:
                self.is_move_able = True
                if len(self.guard_effect) < 1:
                    self.guard_effect.append(GuardEffect.GuardEffect(self.x, self.y, self))

            if self.health <= 0:
                self.state_index = 7
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
            if (keys[pygame.K_LSHIFT]) and self.is_dash_able and not self.is_guard_on and self.energy >= self.dash_energy:
                self.is_dash_able = False
                self.is_invincibility = True
                self.is_invincibility_able = True
                self.dash_range = 0
                if not self.is_attacking_state:
                    self.state_index = 2
                    self.energy -= self.dash_energy

            # invincibility time
            if self.is_invincibility_able:
                if not self.direction and self.x <= 720:
                    self.x += self.dash_point
                elif self.direction and self.x >= 0:
                    self.x -= self.dash_point
                self.dash_range += self.dash_point

                # if dash range is over than max range
                if self.dash_range > self.dash_max_range:
                    self.is_invincibility_able = False
                    self.is_invincibility = False

                    if self.state_index == 2:
                        self.state_index = 0

    def jump(self):
        if not self.is_player_death:
            if self.is_jump_able and self.energy >= self.jump_energy:
                self.is_jump_able = False
                self.energy -= self.jump_energy

    def guard_on(self):
        if not self.is_player_death:
            self.state_index = 10
            self.spr_index = 0
            self.is_guard_on = True

    def guard_off(self):
        if not self.is_player_death:
            self.state_index = 0
            self.spr_index = 0
            self.is_guard_on = False


