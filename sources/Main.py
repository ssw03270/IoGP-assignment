"""
메인 코드
왕의 점심은 얼마나 맛있을지 궁금했던 기사는
성으로 찾아가 그의 점심을 먹어보기로 결심했다
"""

import pygame, sys
import time
from sources.Objects import Object, Player
from sources.Objects.UI import UiDied, UiHealth, UiEnemyHealth, Button
from sources.Objects.Enemy import MedievalWarrior, MartialHero
from sources import Tileset

clock = pygame.time.Clock()

# pygame start
pygame.init()

# pygame color
black = (0,  0,  0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (200, 0, 0)
gray = (59, 59, 59)

# pygame display
window_size = [720, 540]
screen = pygame.display.set_mode(window_size)
game_title = 'King\'s Lunch '
pygame.display.set_caption(game_title)
screen.fill(white)


anim_light_level_2_index = 0
anim_light_level_2_max_index = 4

button_list = []

# level design


#####

def draw(object = Object.Object):
    x = object.x
    y = object.y

    sprite = object.draw_image()
    screen.blit(sprite, (x - object.spr_width / 2 * object.spr_size, y - object.spr_height / 2 * object.spr_size))

def draw_level(tileset = Tileset.Tileset, level = int, delta_time = int):
    if level == 0:
        spr_title = pygame.image.load("../sprites/ui/Title.png").convert_alpha()
        screen.blit(spr_title, (360 - 257, 100))

        button1 = Button.Button(360, 340, "Start")
        draw(button1)
        font = pygame.font.SysFont(None, 30)
        title = font.render(button1.title, True, white)
        title_rect = title.get_rect()
        title_rect.centerx = button1.x
        title_rect.y = button1.y - 10
        screen.blit(title, title_rect)
        button_list.append(button1)

        button2 = Button.Button(360, 400, "Exit")
        draw(button2)
        font = pygame.font.SysFont(None, 30)
        title = font.render(button2.title, True, white)
        title_rect = title.get_rect()
        title_rect.centerx = button2.x
        title_rect.y = button2.y - 10
        screen.blit(title, title_rect)
        button_list.append(button2)

    elif level == 1:
        for i in range(0, 18, 6):
            draw_sprite(tileset.draw_wall(20, 1, 27, 6), tileset, 496, i * tileset.real_size)

        draw_sprite(tileset.draw_ground(12, 0, 15, 2), tileset, 0, 400)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 0, 400 + tileset.real_size * 3)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 0, 400 + tileset.real_size * 4)

        draw_sprite(tileset.draw_ground(12, 0, 15, 2), tileset, 16 * tileset.real_size, 400)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 16 * tileset.real_size, 400 + tileset.real_size * 3)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 16 * tileset.real_size, 400 + tileset.real_size * 4)

        draw_sprite(tileset.draw_ground(12, 0, 15, 2), tileset, 20 * tileset.real_size, 400)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 20 * tileset.real_size, 400 + tileset.real_size * 3)
        draw_sprite(tileset.draw_ground(12, 2, 15, 2), tileset, 20 * tileset.real_size, 400 + tileset.real_size * 4)

        for i in range(4, 16, 6):
            draw_sprite(tileset.draw_wood_env(4, 12, 9, 13), tileset, i * tileset.real_size, 400)

        draw_sprite(tileset.draw_env_object(17, 0, 19, 3), tileset, 544, 300)

    elif level == 2:
        for i in range(0, 18, 4):
            draw_sprite(tileset.draw_wall(20, 12, 25, 15), tileset, 0, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(20, 12, 25, 15), tileset, 6 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(20, 12, 25, 15), tileset, 12 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(20, 12, 25, 15), tileset, 18 * tileset.real_size, i * tileset.real_size)

        for i in range(0, 24, 3):
            draw_sprite(tileset.draw_ground(1, 0, 3, 2), tileset, i * tileset.real_size, 400)
        for i in range(0, 24):
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 2)
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 3)
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 4)

        for i in range(0, 4):
            draw_sprite(tileset.draw_env_object(10, 0, 12, 1), tileset, i * 224 - 50, 96)
            draw_sprite(tileset.draw_env_object(11, 2, 12, 5), tileset, i * 224 - 18, 136)
            draw_sprite(tileset.draw_env_object(11, 2, 12, 5), tileset, i * 224 - 18, 136 + 32 * 3)
            draw_sprite(tileset.draw_env_object(10, 6, 12, 7), tileset, i * 224 - 50, 136 + 32 * 7)

        for i in range(0, 24, 7):
            draw_sprite(tileset.draw_env_object(7, 9, 11, 11), tileset, 32 + i * tileset.real_size, 0)
            draw_sprite(tileset.draw_env_object(7, 12, 9, 14), tileset, 0 + i * tileset.real_size, 0)
            draw_sprite(tileset.draw_env_object(10, 12, 12, 14), tileset, 128 + i * tileset.real_size, 0)

        global anim_light_level_2_index

        for i in range(0, 3):
            draw_sprite(tileset.draw_environment(13, 12, 13, 15), tileset, i * 224 + 96, 300)
            draw_sprite(tileset.draw_anim_light(int(anim_light_level_2_index), 5, int(anim_light_level_2_index), 5), tileset, i * 224 + 96, 300)

        # level anim update
        anim_light_level_2_index += delta_time / 1000 * 10

        if anim_light_level_2_index >= anim_light_level_2_max_index:
            anim_light_level_2_index = 0


    elif level == 3:
        for i in range(0, 18, 5):
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 0, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 4 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 8 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 12 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 16 * tileset.real_size, i * tileset.real_size)
            draw_sprite(tileset.draw_wall(14, 8, 17, 12), tileset, 20 * tileset.real_size, i * tileset.real_size)
        for i in range(0, 24, 5):
            draw_sprite(tileset.draw_ground(0, 12, 5, 13), tileset, i * tileset.real_size, 400)
        for i in range(0, 24):
            draw_sprite(tileset.draw_ground(12, 2, 12, 2), tileset, i * tileset.real_size, 464)
            draw_sprite(tileset.draw_ground(12, 2, 12, 2), tileset, i * tileset.real_size, 496)
            draw_sprite(tileset.draw_ground(12, 2, 12, 2), tileset, i * tileset.real_size, 528)
        for i in range(0, 24, 3):
            draw_sprite(tileset.draw_env_object(13, 18, 16, 18), tileset, i * tileset.real_size, 0)
        for i in range(0, 4):
            draw_sprite(tileset.draw_env_object(22, 25, 24, 25), tileset, i * 224 - 50, 32)
            draw_sprite(tileset.draw_env_object(23, 26, 23, 30), tileset, i * 224 - 18, 64)
            draw_sprite(tileset.draw_env_object(23, 27, 23, 30), tileset, i * 224 - 18, 64 + 32 * 3)
            draw_sprite(tileset.draw_env_object(23, 27, 23, 30), tileset, i * 224 - 18, 64 + 32 * 6)
            draw_sprite(tileset.draw_env_object(22, 31, 24, 31), tileset, i * 224 - 50, 64 + 32 * 10)

def draw_sprite(sprite, tileset, start_x, start_y):
    for x in range(len(sprite)):
        for y in range(len(sprite[x])):
            screen.blit(sprite[x][y], (start_x + x * tileset.real_size, start_y + y * tileset.real_size))

def draw_enemy_health(enemy):
    enemy_max_health = enemy.max_health
    enemy_health = enemy.health

    font = pygame.font.SysFont(None, 30)
    title = font.render(enemy.name, True, white)
    title_rect = title.get_rect()
    title_rect.centerx = 360
    title_rect.y = 25
    screen.blit(title, title_rect)

    pygame.draw.rect(screen, black, [148, 48, 423, 24])
    pygame.draw.rect(screen, black, [146, 50, 428, 20])

    pygame.draw.rect(screen, gray, [145, 51, 426, 18])

    pygame.draw.rect(screen, red, [150, 50, 420 * (enemy_health / enemy_max_health), 20])
    pygame.draw.rect(screen, red, [148, 52, 420 * (enemy_health / enemy_max_health) + 4, 16])

def draw_player_ui(player):
    player_max_health = player.max_health
    player_health = player.health
    player_max_energy = player.max_energy
    player_energy = player.energy

    pygame.draw.rect(screen, black, [48, 473, 123, 24])
    pygame.draw.rect(screen, black, [47, 475, 128, 20])

    pygame.draw.rect(screen, gray, [45, 476, 126, 18])

    pygame.draw.rect(screen, red, [50, 475, 120 * (player_health / player_max_health), 20])
    pygame.draw.rect(screen, red, [46, 477, 120 * (player_health / player_max_health) + 6, 16])

    pygame.draw.rect(screen, black, [48, 498, 123, 24])
    pygame.draw.rect(screen, black, [47, 500, 128, 20])

    pygame.draw.rect(screen, gray, [45, 501, 126, 18])

    pygame.draw.rect(screen, blue, [50, 500, 120 * (player_energy / player_max_energy), 20])
    pygame.draw.rect(screen, blue, [46, 502, 120 * (player_energy / player_max_energy) + 6, 16])

def main():
    # object
    player_x = 100
    player_y = 415
    player = Player.Player(player_x, player_y)

    died = UiDied.UiDied(360, 270, player)

    # level
    levels = [[],
              [MedievalWarrior.MedievalWarrior(800, 400, player)],
              [],
              [MartialHero.MartialHero(800, 400, player)],
              []]

    level_index = 0
    max_level_index = len(levels)
    next_level_delay = 0
    next_level_max_delay = 1000
    is_next_level_able = False

    # tileset
    tileset = Tileset.Tileset()

    while True:
        # set fps
        delta_time = clock.tick(30)
        # check level
        is_all_enemy_die = True
        for obj in levels[level_index]:
            if not obj.is_enemy_die:
                is_all_enemy_die = False
        if is_all_enemy_die and level_index + 1 < max_level_index and not level_index == 0:
            is_next_level_able = True

        # is time to move next level
        if is_next_level_able:
            next_level_delay += delta_time
            if next_level_delay > next_level_max_delay:
                next_level_delay = 0
                is_next_level_able = False
                level_index += 1

                player.x = player_x
                player.y = player_y

        # set delta time of each object
        player.delta_time = delta_time
        for obj in levels[level_index]:
            obj.delta_time = delta_time
            for ability in obj.ability:
                ability.delta_time = delta_time

        # update each object
        if not level_index == 0:
            player.update()
        for obj in levels[level_index]:
            obj.update()

        # set screen white for update display
        background = pygame.image.load("../sprites/Castle/background.png")
        screen.blit(background, (0, 0))
        draw_level(tileset, level_index, delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                column_index = event.pos[0]
                row_index = event.pos[1]
                for button in button_list:
                    value = button.check_click(column_index, row_index)
                    if value == "Start":
                        level_index = 1
                        player.x = player_x
                        player.y = player_y
                    elif value == "Exit":
                        sys.exit()

            if event.type == pygame.KEYDOWN and not level_index == 0:
                if event.key == pygame.K_LCTRL:
                    player.attack()
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_LALT:
                    player.guard_on()
                if event.key == pygame.K_r and player.is_player_death:
                    player = Player.Player(300, 355)
                    healths = [UiHealth.UiHealth(50, 100, player, 1), UiHealth.UiHealth(90, 100, player, 2),
                               UiHealth.UiHealth(130, 100, player, 3), UiHealth.UiHealth(170, 100, player, 4),
                               UiHealth.UiHealth(210, 100, player, 5)]
                    died = UiDied.UiDied(360, 270, player)

                    # level
                    levels = levels
                    level_index = 0
            if event.type == pygame.KEYUP and not level_index == 0:
                if event.key == pygame.K_LALT:
                    player.guard_off()
        # draw object
        if not level_index == 0:
            draw(player)
            draw_player_ui(player)
        for obj in levels[level_index]:
            draw(obj)
            for ability in obj.ability:
                draw(ability)
        if player.is_player_death:
            draw(died)
        for obj in levels[level_index]:
            draw_enemy_health(obj)

        pygame.display.update()

if __name__ == "__main__":
    main()