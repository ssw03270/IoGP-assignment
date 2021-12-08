"""
메인 코드
왕의 점심은 얼마나 맛있을지 궁금했던 기사는
성으로 찾아가 그의 점심을 먹어보기로 결심했다
"""

import pygame, sys
import time
from sources.Objects import Object, Player
from sources.Objects.UI import UiDied, UiHealth, UiEnemyHealth, Button, Paper
from sources.Objects.Enemy import MedievalWarrior, MartialHero, EvilWizard, King
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

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

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
        content = " 아주 먼 옛날, 배고픈 기사 하나가 길을 가고 있었다. 명예나 권력을 좋아하던 보통의 기사들과는 달리, 그는 오직 먹는 것만 좋아할 뿐이었다.\n\n" \
                  " 어느날 문득, 그는 왕의 점심은 얼마나 맛있을지에 대한 생각을 했다. 실행력이 좋았던 기사는 그 길로 곧장, 왕의 성으로 쳐들어가고자 했다. \n\n" \
                  " 하지만 성문에는 문지기가 있었다. 아무래도 기사는 그를 뚫고 가야 할 듯 했다. \n\n\n\n" \
                  " (방향키 : 이동, Shift : 대시, Alt : 방어,\n Ctrl : 공격, Space : 점프)"
        paper = Paper.Paper(360, 270, "Paper", content)
        button_list.append(paper)
        draw(paper)

        font = pygame.font.SysFont("휴먼편지체", 20)
        new_content = ""
        for content in paper.contents:
            new_content += ''.join(content) + "\n"

        blit_text(screen, new_content, paper.position(), font)

    elif level == 2:
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

    elif level == 3:
        content = " 고작 문지기로는 온갖 산해진미를 먹으며 근육을 단련한 기사를 막을 수 없었다. 하지만 약간의 상처를 입는 건 어쩔 수 없었다. \n\n" \
                  " 다행이 문지기의 뒷주머니에는 먹다 만 빵조각이 있었고, 기사는 참지 못하고 먹어버리고 말았다. \n\n" \
                  " 양은 적었지만 기사가 회복하기에는 충분한 양이었다. 만반의 준비를 갖춘 기사는 이내 성 안으로 발걸음을 옮겼다 \n\n" \
                  " 넓은 성안, 그곳에는 사무라이 하나가 뜬금없이 복도에 서있었다. 개발자의 예산 부족인지 뭔지는 모르겠지만 사무라이는 먼 나라에서 온 손님인 듯 했다. \n\n" \
                  " 기사의 목표는 왕의 점심. 기사는 곧장 사무라이에게 달려들었다."
        paper = Paper.Paper(360, 270, "Paper", content)
        button_list.append(paper)
        draw(paper)

        font = pygame.font.SysFont("휴먼편지체", 20)
        new_content = ""
        for content in paper.contents:
            new_content += ''.join(content) + "\n"

        blit_text(screen, new_content, paper.position(), font)

    elif level == 4:
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

    elif level == 5:
        content = " 사무라이는 꽤나 버거운 상대였지만 역시나 이번에도 기사가 승리했다. 사무라이의 품안에는 말린 다랑어가 하나 있었다. \n\n" \
                  " 때마침 기사는 배가 고팠기에 그것을 먹고 기운을 차렸다. 성은 넓었지만 아마 넓은 복도를 따라 걸으면 왕의 식당이 나올 듯 했다. \n\n" \
                  " 기사는 상처가 회복되기를 기다렸다가 다시 앞으로 나아갔다. 그리고 또 다시 누군가가 기사의 앞길을 막아세웠다. \n\n" \
                  " 후드를 뒤집어 쓴, 심상치 않은 느낌의 마법사였다."
        paper = Paper.Paper(360, 270, "Paper", content)
        button_list.append(paper)
        draw(paper)

        font = pygame.font.SysFont("휴먼편지체", 20)
        new_content = ""
        for content in paper.contents:
            new_content += ''.join(content) + "\n"

        blit_text(screen, new_content, paper.position(), font)

    elif level == 6:
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

    elif level == 7:
        content = " 마법사가 소환하는 해골 탓에 꽤나 성가셨지만 기사는 어찌어찌 쳐치하는데 성공했다. 역시나 기사는 배고픔을 해결하기 위해 마법사의 옷을 뒤적였다.\n\n" \
                  " 그러나 마법사가 가진 것이라고는 정체불명의 핏덩어리 뿐이었다. 아무리 기사가 대식가라고는 하지만 이건 무리였다. \n\n" \
                  " 이후 기사는 다시 앞으로 나아갔다. 곧, 그는 쌍둥이를 만날 수 있었다. 그녀들은 똑 닮았으며, 날카라운 창을 들고 있었다. \n\n" \
                  " 그리고 이번에도 기사는 왕의 점심을 먹기 위해 앞으로 나아갔다."
        paper = Paper.Paper(360, 270, "Paper", content)
        button_list.append(paper)
        draw(paper)

        font = pygame.font.SysFont("휴먼편지체", 20)
        new_content = ""
        for content in paper.contents:
            new_content += ''.join(content) + "\n"

        blit_text(screen, new_content, paper.position(), font)

    elif level == 8:
        for i in range(0, 18, 4):
            draw_sprite(tileset.draw_wall_far(20, 12, 25, 15), tileset, 0, i * tileset.real_size, 32, 96, 96, 64 + 192)
            draw_sprite(tileset.draw_wall_far(20, 12, 25, 15), tileset, 6 * tileset.real_size, i * tileset.real_size, 32 + 6 * 32, 96, 96 + 6 * 32, 64 + 192)
            draw_sprite(tileset.draw_wall_far(20, 12, 25, 15), tileset, 12 * tileset.real_size, i * tileset.real_size, 32 + 12 * 32, 96, 96 + 12 * 32, 64 + 192)
            draw_sprite(tileset.draw_wall_far(20, 12, 25, 15), tileset, 18 * tileset.real_size, i * tileset.real_size, 32 + 18 * 32, 96, 96 + 18 * 32, 64 + 192)

        for i in range(0, 24, 6):
            draw_sprite(tileset.draw_wall_far(20, 12, 22, 12), tileset, 32 + i * 32, 96)
            draw_sprite(tileset.draw_wall_far(20, 13, 20, 13), tileset, 32 + i * 32, 128)
            draw_sprite(tileset.draw_wall_far(20, 13, 20, 13), tileset, 96 + i * 32, 128)
            draw_sprite(tileset.draw_env_object_far(0, 16, 2, 21), tileset, 32 + i * 32, 96)

        for i in range(0, 24, 2):
            draw_sprite(tileset.draw_env_object(14, 18, 15, 18), tileset, i * tileset.real_size, 400)

        for i in range(0, 24, 3):
            draw_sprite(tileset.draw_ground(1, 0, 3, 2), tileset, i * tileset.real_size, 400)

        for i in range(0, 24):
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 2)
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 3)
            draw_sprite(tileset.draw_ground(0, 4, 0, 4), tileset, i * tileset.real_size, 400 + tileset.real_size * 4)

        for i in range(0, 24, 2):
            draw_sprite(tileset.draw_env_object_far(14, 18, 15, 18), tileset, i * tileset.real_size, 0)
            draw_sprite(tileset.draw_env_object_far(14, 16, 15, 16), tileset, i * tileset.real_size, 32)

def draw_sprite(sprite, tileset, start_x, start_y, not_x1 = -1, not_y1 = -1, not_x2 = -1, not_y2 = -1):
    for x in range(len(sprite)):
        for y in range(len(sprite[x])):
            if not (start_x + x * tileset.real_size >= not_x1 and start_x + x * tileset.real_size <= not_x2 \
                    and start_y + y * tileset.real_size >= not_y1 and start_y + y * tileset.real_size <= not_y2):
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

    pygame.draw.rect(screen, red, [150, 50, 425 * (enemy_health / enemy_max_health) - 5, 20])
    pygame.draw.rect(screen, red, [148, 52, 425 * (enemy_health / enemy_max_health), 16])

def draw_player_ui(player):
    player_max_health = player.max_health
    player_health = player.health
    player_max_energy = player.max_energy
    player_energy = player.energy

    pygame.draw.rect(screen, black, [48, 473, 123, 24])
    pygame.draw.rect(screen, black, [47, 475, 128, 20])

    pygame.draw.rect(screen, gray, [45, 476, 126, 18])

    pygame.draw.rect(screen, red, [50, 475, 125 * (player_health / player_max_health) - 5, 20])
    pygame.draw.rect(screen, red, [46, 477, 125 * (player_health / player_max_health), 16])

    pygame.draw.rect(screen, black, [48, 498, 123, 24])
    pygame.draw.rect(screen, black, [47, 500, 128, 20])

    pygame.draw.rect(screen, gray, [45, 501, 126, 18])

    pygame.draw.rect(screen, blue, [50, 500, 125 * (player_energy / player_max_energy) - 5, 20])
    pygame.draw.rect(screen, blue, [46, 502, 125 * (player_energy / player_max_energy), 16])

    spr_attack = pygame.image.load("../sprites/ui/Attack.png").convert_alpha()
    spr_punch = pygame.image.load("../sprites/ui/Punch.png").convert_alpha()
    spr_kick = pygame.image.load("../sprites/ui/Kick.png").convert_alpha()

    screen.blit(spr_attack, (550, 475))
    screen.blit(spr_punch, (600, 475))
    screen.blit(spr_kick, (650, 475))

    attack_height = player.attack_delay / player.attack_max_delay * 40
    punch_height = player.punch_delay / player.punch_max_delay * 40
    kick_height = player.kick_delay / player.kick_max_delay * 40

    if attack_height > 40:
        attack_height = 40
    if punch_height > 40:
        punch_height = 40
    if kick_height > 40:
        kick_height = 40

    attack_transparent = pygame.Surface((40, 40 - attack_height))  # the size of your rect
    punch_transparent = pygame.Surface((40, 40 - punch_height))  # the size of your rect
    kick_transparent = pygame.Surface((40, 40 - kick_height))  # the size of your rect

    attack_transparent.set_alpha(200)  # alpha level
    punch_transparent.set_alpha(200)  # alpha level
    kick_transparent.set_alpha(200)  # alpha level

    attack_transparent.fill(gray)
    punch_transparent.fill(gray)
    kick_transparent.fill(gray)

    screen.blit(attack_transparent, (550, 475))
    screen.blit(punch_transparent, (600, 475))
    screen.blit(kick_transparent, (650, 475))

def main():
    # object
    player_x = 100
    player_y = 390
    player = Player.Player(player_x, player_y)

    died = UiDied.UiDied(360, 270, player)

    # level
    levels = [[],
              [],
              [MedievalWarrior.MedievalWarrior(800, 400, player)],
              [],
              [MartialHero.MartialHero(800, 400, player)],
              [],
              [EvilWizard.EvilWizard(800, 375, player)],
              [],
              [King.King(800, 340, player)]]

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
        if is_all_enemy_die and level_index + 1 < max_level_index and not level_index == 0 and not level_index % 2 == 1:
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

                player.health = player.max_health
                player.energy = player.max_energy

        # set delta time of each object
        player.delta_time = delta_time
        for guard_effect in player.guard_effect:
            guard_effect.delta_time = delta_time
        for obj in levels[level_index]:
            obj.delta_time = delta_time
            for ability in obj.ability:
                ability.delta_time = delta_time

        # update each object
        if not level_index == 0 and not level_index % 2 == 1:
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
                    if value == "Start" and level_index == 0:
                        level_index = 1
                        player.x = player_x
                        player.y = player_y

                    elif value == "Exit" and level_index == 0:
                        sys.exit()

                    elif value == "Paper" and level_index % 2 == 1:
                        level_index += level_index % 2
                        player.x = player_x
                        player.y = player_y

            if event.type == pygame.KEYUP and not level_index == 0 and not level_index % 2 == 1:
                if event.key == pygame.K_x:
                    player.punch_end()

            if event.type == pygame.KEYDOWN and not level_index == 0 and not level_index % 2 == 1:
                if event.key == pygame.K_z:
                    player.attack()
                if event.key == pygame.K_c:
                    player.kick()
                if event.key == pygame.K_SPACE:
                    player.jump()
                # if event.key == pygame.K_x:
                #     player.guard_on()
                if event.key == pygame.K_r and player.is_player_death:
                    player_x = 100
                    player_y = 390
                    player = Player.Player(player_x, player_y)

                    died = UiDied.UiDied(360, 270, player)

                    # level
                    levels = [[],
                              [],
                              [MedievalWarrior.MedievalWarrior(800, 400, player)],
                              [],
                              [MartialHero.MartialHero(800, 400, player)],
                              [],
                              [EvilWizard.EvilWizard(800, 375, player)],
                              [],
                              [King.King(800, 340, player)]]

                    level_index = 0
            if event.type == pygame.KEYUP and not level_index == 0 and not level_index % 2 == 1:
                if event.key == pygame.K_x:
                    player.guard_off()
        # draw object
        for obj in levels[level_index]:
            draw(obj)
            for ability in obj.ability:
                draw(ability)

        if not level_index == 0 and not level_index % 2 == 1:
            draw(player)
            draw_player_ui(player)
            for guard_effect in player.guard_effect:
                draw(guard_effect)

        if player.is_player_death:
            draw(died)
        for obj in levels[level_index]:
            draw_enemy_health(obj)

        pygame.display.update()

if __name__ == "__main__":
    main()