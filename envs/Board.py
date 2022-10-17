from envs.Engine import Engine
import pygame
from pygame import gfxdraw
from enum import Enum
from typing import Tuple


class Board:
    def __init__(self):
        self.height = 200
        self.width = 200
        self.cell_size = 20
        self.ballSpeed = 4
        self.playerSpeed = 3
        self.balls = []
        self.walls = []
        self.player = [0, 0, 0, 0]
        self.goal = [0, 0, 0, 0]
        self.read_map()
        self.screen = None
        self.surf = None
        self.clock = None
        self.engine = Engine(self)

    def draw(self):
        class Colors(Enum):
            RED = (1, (255, 0, 0))
            GREEN = (2, (50, 255, 50))
            BLUE = (3, (0, 0, 255))
            GRAY = (4, (191, 191, 191))
            BLACK = (5, (0, 0, 0))
            WHITE = (6, (255, 255, 255))

            def __str__(self) -> str:
                return self.name.lower()

            def num(self) -> int:
                return self.value[0]

            def rgb(self) -> Tuple:
                return self.value[1]
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        for i in range(self.width // self.cell_size):
            for j in range(self.height // self.cell_size):
                if i % 2 == j % 2:
                    pygame.gfxdraw.box(self.surf, (i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size), Colors.GRAY.rgb())
        for wall in self.walls:
            pygame.gfxdraw.box(self.surf, (wall[0], wall[1], wall[2], wall[3]), Colors.BLACK.rgb())
        pygame.gfxdraw.box(self.surf, (self.goal[0], self.goal[1], self.goal[2], self.goal[3]), Colors.GREEN.rgb())
        for ball in self.balls:
            pygame.gfxdraw.filled_circle(self.surf, ball[0], ball[1], ball[2], Colors.RED.rgb())
        pygame.gfxdraw.box(self.surf, (self.player[0], self.player[1], self.player[2], self.player[3]), Colors.BLUE.rgb())
        self.screen.blit(self.surf, (0, 0))
        pygame.event.pump()
        self.clock.tick(50)
        pygame.display.flip()

    def read_map(self):
        filename = 'envs/GameMap'
        file = open(filename, 'r')
        for line in file:
            data = line.split(' ')
            if data[0] == 'P':
                self.player = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]
            elif data[0] == 'W':
                self.walls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
            elif data[0] == 'G':
                self.goal = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]
            elif data[0] == 'B':
                self.balls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
            else:
                self.width = int(data[0])
                self.height = int(data[1])

    def close(self):
        pygame.display.quit()
        pygame.quit()
