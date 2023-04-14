from envs.Engine import Engine
import pygame
from pygame import gfxdraw
from enum import Enum
from typing import Tuple
import numpy as np
from envs.Utils import line_ray_intersection
import math


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
        self.checkpoints = []  # should be given in the order in which to be visited
        self.state = None
        self.read_map()
        self.engine = Engine(self)

        a = math.cos(math.pi/4)
        self.ray_directions = [(1, 0), (a, -a), (0, -1), (-a, -a), (-1, 0), (-a, a), (0, 1), (a, a)]
        self.ray_hit_points = []
        # self.dispreward = 0

    def draw(self, surf):
        class Colors(Enum):
            RED = (1, (255, 0, 0))
            GREEN = (2, (50, 255, 50))
            BLUE = (3, (0, 0, 255))
            GRAY = (4, (191, 191, 191))
            BLACK = (5, (0, 0, 0))
            WHITE = (6, (255, 255, 255))
            YELLOW = (7, (246, 250, 40))
            VIOLET = (8, (166, 40, 250))

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
        pygame.gfxdraw.box(surf, (self.player[0], self.player[1], self.player[2], self.player[3]), Colors.BLUE.rgb())

        checkpoint_idx = self.engine.checkpoint
        point1 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
        point2 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
        if self.checkpoints[checkpoint_idx][2] in [0, 2, 4, 6]:
            point1[1] -= self.checkpoints[checkpoint_idx][4]
            point2[1] += self.checkpoints[checkpoint_idx][4]
        else:
            point1[0] -= self.checkpoints[checkpoint_idx][4]
            point2[0] += self.checkpoints[checkpoint_idx][4]
        pygame.gfxdraw.line(surf, point1[0], point1[1], point2[0], point2[1], Colors.YELLOW.rgb())

        checkpoint_idx = self.engine.checkpoint - 1
        if checkpoint_idx >=0:
            point1 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
            point2 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
            if self.checkpoints[checkpoint_idx][2] in [0, 2, 4, 6]:
                point1[1] -= self.checkpoints[checkpoint_idx][4]
                point2[1] += self.checkpoints[checkpoint_idx][4]
            else:
                point1[0] -= self.checkpoints[checkpoint_idx][4]
                point2[0] += self.checkpoints[checkpoint_idx][4]
            pygame.gfxdraw.line(surf, point1[0], point1[1], point2[0], point2[1], Colors.RED.rgb())
        # self.compute_state()

        for x, y, t in self.ray_hit_points:
            if t == 0 or t == -2:
                pygame.gfxdraw.line(surf, self.player[0] + self.player[2] // 2, self.player[1] + self.player[3] // 2, int(x), int(y), Colors.GREEN.rgb() if t==0 else Colors.RED.rgb())
            else:
                pygame.gfxdraw.line(surf, self.player[0]+ self.player[2]//2, self.player[1] + self.player[3]//2, int(x), int(y), Colors.VIOLET.rgb() if t==1 else Colors.RED.rgb())
        # font = pygame.font.SysFont('Times New Roman', 20)
        # self.dispreward += reward
        # img = font.render(str(self.dispreward), True, Colors.BLACK.rgb())
        # surf.blit(img, (20, 20))

    def read_map(self):
        filename = 'envs/GameMap'
        file = open(filename, 'r')
        self.state = []
        for line in file:
            data = line.split(' ')
            if data[0] == 'P':
                self.player = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]
                self.state.append(self.player[0])
                self.state.append(self.player[1])
                # take entry for player before balls
            elif data[0] == 'W':
                self.walls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
            elif data[0] == 'G':
                self.goal = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]
            elif data[0] == 'B':
                self.balls.append([int(data[1]), int(data[2]), int(data[3]), int(data[4])])
                # self.state.append(self.balls[-1][0])
                # self.state.append(self.balls[-1][1])
                # self.state.append(self.balls[-1][3])
            elif data[0] == 'C':
                self.checkpoints.append((int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])))
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

    def compute_state(self):
        self.state = []
        self.ray_hit_points = []
        ray_origin = [self.player[0] + self.player[2]/2, self.player[1] + self.player[3]/2]
        for ray_direction in self.ray_directions:
            best_t = 1000000000
            best_point = (ray_origin, 1)
            for wall in self.walls:
                point1 = (wall[0], wall[1])
                point2 = (wall[0], wall[1] + wall[3])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, 1)
                point2 = (wall[0] + wall[2], wall[1])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, 1)
                point1 = (wall[0] + wall[2], wall[1] + wall[3])
                point2 = (wall[0] + wall[2], wall[1])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, 1)
                point2 = (wall[0], wall[1] + wall[3])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, 1)
            for ball in self.balls:
                point1 = (ball[0]-ball[2], ball[1]+ball[2])
                point2 = (ball[0]-ball[2], ball[1]-ball[2])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, -1)
                point1 = (ball[0] + ball[2], ball[1] - ball[2])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, -1)
                point1 = (ball[0] - ball[2], ball[1] + ball[2])
                point2 = (ball[0] + ball[2], ball[1] + ball[2])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, -1)
                point1 = (ball[0] + ball[2], ball[1] - ball[2])
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, -1)
            checkpoint_idx = self.engine.checkpoint
            point1 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
            point2 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
            if self.checkpoints[checkpoint_idx][2] in [0, 2, 4, 6]:
                point1[1] -= self.checkpoints[checkpoint_idx][4]
                point2[1] += self.checkpoints[checkpoint_idx][4]
            else:
                point1[0] -= self.checkpoints[checkpoint_idx][4]
                point2[0] += self.checkpoints[checkpoint_idx][4]
            t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
            if t != -1 and t < best_t:
                best_t = t
                best_point = (point, 0)
            checkpoint_idx = self.engine.checkpoint - 1
            if checkpoint_idx >= 0:
                point1 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
                point2 = [self.checkpoints[checkpoint_idx][0], self.checkpoints[checkpoint_idx][1]]
                if self.checkpoints[checkpoint_idx][2] in [0, 2, 4, 6]:
                    point1[1] -= self.checkpoints[checkpoint_idx][4]
                    point2[1] += self.checkpoints[checkpoint_idx][4]
                else:
                    point1[0] -= self.checkpoints[checkpoint_idx][4]
                    point2[0] += self.checkpoints[checkpoint_idx][4]
                t, point = line_ray_intersection(ray_origin, ray_direction, point1, point2)
                if t != -1 and t < best_t:
                    best_t = t
                    best_point = (point, -2)
            self.ray_hit_points.append([best_point[0][0], best_point[0][1], best_point[1]])
            best_t /= 400.0
            if best_point[1] == 1:
                self.state.append([best_t, 0, 0, 0])
            elif best_point[1] == -1:
                self.state.append([0, best_t, 0, 0])
            elif best_point[1] == 0:
                self.state.append([0, 0, best_t, 0])
            else:
                self.state.append([0, 0, 0, best_t])

    def get_state(self):
        self.compute_state()
        return np.array(self.state).flatten()
