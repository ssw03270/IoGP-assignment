import pygame
import math
from sources.Objects import Object, Player

class Paper(Object.Object):
    def __init__(self, x, y, title, content):
        self.x = x
        self.y = y
        self.title = title
        self.content = content
        self.contents = []
        self.line_length = 41

        # sprite information
        self.spr_width = 465
        self.spr_height = 273
        self.spr_size = 1.5

        # ui image
        self.spr_button = pygame.image.load("../sprites/ui/Paper.png").convert_alpha()    # 0

        self.set_content()

    def draw_image(self):
        sprite = self.spr_button.subsurface(0, 0, self.spr_width, self.spr_height)
        sprite = pygame.transform.scale(
            pygame.transform.flip(sprite, False, False),
            (int(self.spr_width * self.spr_size), int(self.spr_height * self.spr_size)))
        return sprite

    def check_click(self, x, y):
        click_x = x
        click_y = y

        if self.x - self.spr_width / 2 * self.spr_size < click_x and click_x < self.x + self.spr_width / 2 * self.spr_size:
            if self.y - self.spr_height / 2 * self.spr_size < click_y and click_y < self.y + self.spr_height / 2 * self.spr_size:
                return self.title

    def set_content(self):
        lis = []
        text_count = 0
        for i in range(len(self.content)):
            lis.append(self.content[i])
            if text_count % self.line_length == 0 and not text_count == 0:
                self.contents.append(lis[:])
                lis.clear()
                text_count = 0
            if self.content[i] == "\n":
                text_count = 0
            text_count += 1
        if not lis == []:
            self.contents.append(lis[:])

    def position(self):
        return (self.x - self.spr_width * self.spr_size / 2 + 60, self.y - self.spr_height * self.spr_size / 2 + 60)