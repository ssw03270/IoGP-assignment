import pygame

class Tileset:
    def __init__(self):
        # set tileset size
        self.max_size = self.max_x, self.max_y = (224, 256)
        self.size = self.x, self.y = (16, 16)
        # map tileset
        self.spr_tileset = pygame.image.load("../sprites/map/tileset.png").convert_alpha()
        # map list
        self.map_list = []
        self.set_map_list()

    def set_map_list(self):
        for x in range(int(self.max_x / self.x)):
            lis = []
            for y in range(int(self.max_y / self.y)):
                lis.append(self.spr_tileset.subsurface(x * self.x, y * self.y, self.x, self.y))
            self.map_list.append(lis)

    def draw_image(self, x, y):
        return pygame.transform.scale(self.map_list[x][y], (self.x * 3, self.y * 3))