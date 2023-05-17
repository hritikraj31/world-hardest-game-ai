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
        self.pos_size = [0, 0, 0, 0]
        self.goal = [0, 0, 0, 0]
        self.checkpoints = []  # should be given in the order in which to be visited
        self.read_map()
        self.engine = Engine(self)

    def draw(self, surf):
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

        for i in range(self.width // self.cell_size):
            for j in range(self.height // self.cell_size):
                if i % 2 == j % 2:
                    pygame.gfxdraw.box(surf, (i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size), Colors.GRAY.rgb())
        for wall in self.walls:
            pygame.gfxdraw.box(surf, (wall[0], wall[1], wall[2], wall[3]), Colors.BLACK.rgb())
        pygame.gfxdraw.box(surf, (self.goal[0], self.goal[1], self.goal[2], self.goal[3]), Colors.GREEN.rgb())
        for ball in self.balls:
            pygame.gfxdraw.filled_circle(surf, ball[0], ball[1], ball[2], Colors.RED.rgb())

    def read_map(self):
        filename = 'envs/GameMap'
        file = open(filename, 'r')
        for line in file:
            data = line.split(' ')
            if data[0] == 'P':
                self.pos_size = [[int(data[1]), int(data[2])], [int(data[3]), int(data[4])]]
                # take entry for player before balls
            elif data[0] == 'W':
                self.walls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
            elif data[0] == 'G':
                self.goal = [int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])]
            elif data[0] == 'B':
                self.balls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
            elif data[0] == 'C':
                self.checkpoints.append((int(data[1]), int(data[2]), int(data[3]), int(data[4])))
                # consists of coordinate, type of checkpoint(0: line right, 1: line up
                # ,2: line left, 3: line down, 4: point right, 5: point up, 6: point left, 7: point down), reward
            else:
                self.width = int(data[0])
                self.height = int(data[1])

    @staticmethod
    def close():
        pygame.display.quit()
        pygame.quit()

    def get_dimension(self):
        return self.width, self.height
