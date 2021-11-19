import pygame

class Tileset:
    def __init__(self):
        # set tileset size
        self.ground_max_size = self.ground_max_x, self.ground_max_y = (304, 224)
        self.env_object_max_size = self.env_object_max_x, self.env_object_max_y = (512, 512)
        self.environment_max_size = self.environment_max_x, self.environment_max_y = (368, 480)
        self.wall_max_size = self.wall_max_x, self.wall_max_y = (512, 512)

        self.size = self.x, self.y = (16, 16)

        # map tileset
        self.spr_ground_set = pygame.image.load("../sprites/Castle/ground.png").convert_alpha()
        self.spr_env_object_set = pygame.image.load("../sprites/Castle/env_objects.png").convert_alpha()
        self.spr_environment_set = pygame.image.load("../sprites/Castle/environment.png").convert_alpha()
        self.spr_wall_set = pygame.image.load("../sprites/Castle/walls.png").convert_alpha()

        # map list
        self.ground_list = []
        self.env_object_list = []
        self.environment_list = []
        self.wall_list = []

        self.set_map_list()

    def set_map_list(self):
        for x in range(int(self.ground_max_x / self.x)):
            lis = []
            for y in range(int(self.ground_max_y / self.y)):
                lis.append(self.spr_ground_set.subsurface(x * self.x, y * self.y, self.x, self.y))
            self.ground_list.append(lis)

        for x in range(int(self.env_object_max_x / self.x)):
            lis = []
            for y in range(int(self.env_object_max_y / self.y)):
                lis.append(self.spr_env_object_set.subsurface(x * self.x, y * self.y, self.x, self.y))
            self.env_object_list.append(lis)

        for x in range(int(self.environment_max_x / self.x)):
            lis = []
            for y in range(int(self.environment_max_y / self.y)):
                lis.append(self.spr_environment_set.subsurface(x * self.x, y * self.y, self.x, self.y))
            self.environment_list.append(lis)

        for x in range(int(self.wall_max_x / self.x)):
            lis = []
            for y in range(int(self.wall_max_y / self.y)):
                lis.append(self.spr_wall_set.subsurface(x * self.x, y * self.y, self.x, self.y))
            self.wall_list.append(lis)

    def draw_ground(self, x, y):
        return pygame.transform.scale(self.ground_list[x][y], (self.x * 2, self.y * 2))

    def draw_env_object(self, x, y):
        return pygame.transform.scale(self.env_object_list[x][y], (self.x * 2, self.y * 2))

    def draw_environment(self, x, y):
        return pygame.transform.scale(self.environment_list[x][y], (self.x * 3, self.y * 3))

    def draw_wall(self, x, y):
        return pygame.transform.scale(self.wall_list[x][y], (self.x * 3, self.y * 3))