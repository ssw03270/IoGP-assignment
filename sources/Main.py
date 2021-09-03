"""
메인 코드
"""

import pygame, sys
from sources.Objects import Object, Player, FlowerEnemy
from sources import Tileset

clock = pygame.time.Clock()

# pygame start
pygame.init()

# pygame color
black = (0,  0,  0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (59, 59, 59)

# pygame display
window_size = [720, 540]
screen = pygame.display.set_mode(window_size)
game_title = 'DarkestCave'
pygame.display.set_caption(game_title)
screen.fill(white)

# level design


#####

def draw(object = Object.Object):
    x = object.x
    y = object.y

    sprite = object.draw_image()
    screen.blit(sprite, (x, y))

def draw_level(tileset = Tileset.Tileset):
    tile_x = 2
    tlie_y = 0

    # draw border line
    for x in range(0, 15):
        sprite = tileset.draw_image(2, 10)
        screen.blit(sprite, (x * 48, 0))
        screen.blit(sprite, (x * 48, 492))

    # for y in range(1, 13):
    #     sprite = tileset.draw_image(2, 10)
    #     screen.blit(sprite, (0, y * 48))
    #     screen.blit(sprite, (672, y * 48))

    # draw up
    for x in range (1, 14):
        if tile_x > 6 and tlie_y == 0:
            tlie_y = 2
        if tile_x > 13:
            tile_x = 2
            tlie_y = 0

        sprite = tileset.draw_image(tile_x, tlie_y)
        screen.blit(sprite, (x * 48, 48))
        tile_x += 1

    # draw down
    for x in range(1, 14):
        sprite = tileset.draw_image(2, 10)
        screen.blit(sprite, (x * 48, 444))

    # draw side
    # sprite = tileset.draw_image(3, 10)
    # for y in range(2, 10):
    #     screen.blit(sprite, (48, y * 48))
    #     screen.blit(pygame.transform.flip(sprite, True, False), (624, y * 48))

    # draw vertex
    sprite = tileset.draw_image(2, 10)
    screen.blit(sprite, (0, 48))
    screen.blit(sprite, (672, 48))
    screen.blit(sprite, (0, 444))
    screen.blit(sprite, (672, 444))

def main():
    # object
    player = Player.Player(100, 350)
    flower_enemy = FlowerEnemy.FlowerEnemy(400, 350, player)

    # tileset
    tileset = Tileset.Tileset()

    while True:
        # set fps
        delta_time = clock.tick(60)

        # set delta time of each object
        player.delta_time = delta_time
        flower_enemy.delta_time = delta_time

        # update each object
        player.update()
        flower_enemy.update()

        # set screen white for update display
        background = pygame.image.load("../sprites/map/background.png")
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.attack()


        draw(player)
        draw(flower_enemy)
        draw_level(tileset)

        pygame.display.update()

if __name__ == "__main__":
    main()