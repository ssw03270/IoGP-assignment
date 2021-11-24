"""
메인 코드
왕의 점심은 얼마나 맛있을지 궁금했던 기사는
성으로 찾아가 그의 점심을 먹어보기로 결심했다
"""

import pygame, sys
import time
from sources.Objects import Object, Player
from sources.Objects.UI import UiDied, UiHealth, UiEnemyHealth
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
game_title = 'Last Boss'
pygame.display.set_caption(game_title)
screen.fill(white)

# level design


#####

def draw(object = Object.Object):
    x = object.x
    y = object.y

    sprite = object.draw_image()
    screen.blit(sprite, (x - object.spr_width / 2 * object.spr_size, y - object.spr_height / 2 * object.spr_size))

def draw_level(tileset = Tileset.Tileset, level = int):
    if level == 1:
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



def main():
    # object
    player = Player.Player(300, 415)
    healths = [UiHealth.UiHealth(66, 116, player, 1), UiHealth.UiHealth(106, 116, player, 2),
               UiHealth.UiHealth(146, 116, player, 3), UiHealth.UiHealth(186, 116, player, 4),
               UiHealth.UiHealth(226, 116, player, 5)]
    died = UiDied.UiDied(360, 270, player)

    # level
    levels = [[MedievalWarrior.MedievalWarrior(800, 400, player)],
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
        if is_all_enemy_die and level_index + 1 < max_level_index:
            is_next_level_able += True

        # is time to move next level
        if is_next_level_able:
            next_level_delay += delta_time
            if next_level_delay > next_level_max_delay:
                next_level_delay = 0
                is_next_level_able = False
                level_index += 1

        # set delta time of each object
        player.delta_time = delta_time
        for obj in levels[level_index]:
            obj.delta_time = delta_time
            for ability in obj.ability:
                ability.delta_time = delta_time
        for health in healths:
            health.delta_time = delta_time

        # update each object
        player.update()
        for obj in levels[level_index]:
            obj.update()

        # set screen white for update display
        background = pygame.image.load("../sprites/Castle/background.png")
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.attack()
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_r and player.is_player_death:
                    player = Player.Player(300, 355)
                    healths = [UiHealth.UiHealth(50, 100, player, 1), UiHealth.UiHealth(90, 100, player, 2),
                               UiHealth.UiHealth(130, 100, player, 3), UiHealth.UiHealth(170, 100, player, 4),
                               UiHealth.UiHealth(210, 100, player, 5)]
                    died = UiDied.UiDied(360, 270, player)

                    # level
                    levels = [[FlowerEnemy.FlowerEnemy(500, 400, player), Skeleton.Skeleton(100, 400, player)], []]
                    level_index = 0

        # draw object
        draw_level(tileset, 1)
        draw(player)
        for obj in levels[level_index]:
            draw(obj)
            for ability in obj.ability:
                draw(ability)
        for health in healths:
            draw(health)
        if player.is_player_death:
            draw(died)
        for obj in levels[level_index]:
            draw_enemy_health(obj)

        pygame.display.update()

if __name__ == "__main__":
    main()