"""
메인 코드
"""

import pygame, sys
from sources.Objects import Object, Player

clock = pygame.time.Clock()

# pygame start
pygame.init()

# set display size
window_size = [640, 480]
screen = pygame.display.set_mode(window_size)
game_title = 'DarkestCave'
pygame.display.set_caption(game_title)

#####

def draw(object=Object):
    x = object.x
    y = object.y

    state = object.state

    screen.blit(object.draw_image(state), (x, y))

def main():
    player = Player.Player()
    draw(player)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()