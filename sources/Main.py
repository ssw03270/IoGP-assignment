"""
메인 코드
"""

import pygame, sys
from sources.Objects import Object, Player

clock = pygame.time.Clock()

# pygame start
pygame.init()

# pygame color
black = (0,  0,  0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# pygame display
window_size = [640, 480]
screen = pygame.display.set_mode(window_size)
game_title = 'DarkestCave'
pygame.display.set_caption(game_title)
screen.fill(white)

#####

def draw(object = Object):
    x = object.x
    y = object.y

    sprite = object.draw_image()
    screen.blit(sprite, (x, y))

def main():
    # player character
    player = Player.Player(0, 0)

    while True:
        clock.tick(60)
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        player.move()
        draw(player)
        pygame.display.update()

if __name__ == "__main__":
    main()