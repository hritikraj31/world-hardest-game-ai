from envs.Player import Player
import pygame
from pygame import gfxdraw


class Board:
    def __init__(self):
        self.rows = 15
        self.cols = 20
        self.heightPixel = 20
        self.widthPixel = 20
        # self.height = 200
        # self.width = 200
        self.height = self.rows * self.heightPixel
        self.width = self.cols * self.widthPixel
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.balls = []
        self.read_map()
        self.screen = None
        self.surf = None
        self.clock = None

    def draw(self):
        colors = [(255, 255, 255), (128, 128, 128), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.surf  = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.widthPixel
                y = i * self.heightPixel
                if self.grid[i][j]>3:
                    gfxdraw.filled_circle(self.surf, x + self.widthPixel//2, y + self.heightPixel//2, self.widthPixel//2-1, colors[self.grid[i][j]])
                else:
                    gfxdraw.box(self.surf, (x, y, self.widthPixel, self.heightPixel), colors[self.grid[i][j]])
        self.screen.blit(self.surf, (0, 0))
        pygame.event.pump()
        self.clock.tick(20)
        pygame.display.flip()

    def read_map(self):
        filename = 'envs/GameMap'
        file = open(filename, 'r')
        i = 0
        for line in file:
            j = 0
            for x in line.split(' '):
                x = int(x)
                self.grid[i][j] = x
                if x == 2:
                    self.player = Player(i, j, self)
                elif x > 3:
                    self.balls.append([i, j, x - 3])
                j += 1
            i += 1

    def close(self):
        pygame.display.quit()
        pygame.quit()
