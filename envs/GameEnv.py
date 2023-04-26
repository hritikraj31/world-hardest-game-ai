import time

import gym
import random
import numpy as np
from gym import spaces

import pygame

from envs.Board import Board
from envs.Engine import Engine
from envs.Player import Player
from functools import cmp_to_key


class GameEnv(gym.Env):

    def __init__(self, render_mode):
        self.generation = 0
        self.GL = 100

        self.board = Board()
        self.players = [Player(self.board.pos_size[0], self.board.pos_size[1], self.GL) for i in range(100)]
        self.surf = None
        self.screen = None
        self.clock = None
        self.engine = Engine(self.board)

        self.count_alive = 100

        self.render_mode = render_mode
        self.max_steps = 50
        self.sorted_list = []

        self.best_fitness = 0

    def step(self):
        self.engine.move()
        for player in self.players:
            orig_x, orig_y = player.pos
            player.move()
            goal_reached, ball_hit, wall_hit, [new_x, new_y] = self.engine.check_collisions(orig_x, orig_y, player.pos[0], player.pos[1], player.size[0], player.size[1])
            player.pos = [new_x, new_y]
            # g, b, w, p = self.engine.check_collisions(orig_x, orig_y, new_pos[0], new_pos[1], player.size[0], player.size[1])
            # if w:
            #     print(player.pos)
            #     print(orig_x, orig_y)
            #     assert False
            if goal_reached:
                player.goal_reached = True
            if (goal_reached or ball_hit) and not player.dead:
                self.count_alive -= 1
                player.dead = True
            if player.genes.index >= self.max_steps and not player.dead:
                player.dead = True
                self.count_alive -= 1

    def reset(self):
        self.board = Board()
        self.engine = Engine(self.board)

    def render(self, render_mode):
        pygame.init()
        if self.screen is None and render_mode == 'human':
            pygame.display.init()
            pygame.display.set_caption('World\'s Hardest Game')
            self.screen = pygame.display.set_mode(self.board.get_dimension())
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.surf = pygame.Surface(self.board.get_dimension())
        self.surf.fill((255, 255, 255))

        self.board.draw(self.surf)
        for player in self.players:
            player.draw(self.surf)

        font = pygame.font.SysFont('Times New Roman', 15)
        img = font.render('Gen: {}, Max Steps: {}, GL: {}'.format(self.generation, self.max_steps, self.GL), True, (255, 255, 255))
        self.surf.blit(img, (10, 2))
        if render_mode == 'human':
            self.screen.blit(self.surf, (0, 0))
            pygame.event.pump()
            self.clock.tick(50)
            pygame.display.flip()
        elif render_mode == 'surface':
            return self.surf
        else:
            gym.error("Invalid render_mode, can only be 'human' and 'surface'.")

    def close(self):
        self.board.close()

    def natural_selection(self):
        self.generation += 1
        m_steps = 0
        for player in self.players:
            if abs(self.best_fitness - player.fitness) > 100.0:
                continue
            m_steps = max(m_steps, player.genes.index+1)
        if self.generation % 5 == 0 and (not (abs(m_steps - self.max_steps - 5) > 50)):
            self.max_steps += 10
        if self.max_steps == self.GL:
            self.GL += 50
        self.reset()
        new_population = [Player([0, 0], [0, 0], self.GL) for i in range(len(self.players))]
        self.count_alive = 100
        self.sorted_list = []
        for player in self.players:
            self.sorted_list.append([player.fitness, player])
        self.sorted_list = sorted(self.sorted_list, key=cmp_to_key(lambda item1, item2: item2[0] - item1[0]))
        # print('Worst player fitness {}'.format(self.sorted_list[-1][0]))
        best_player = self.find_best_player()
        self.best_fitness = best_player.fitness
        print(self.sorted_list[0][0], best_player.fitness)
        new_population[len(self.players) - 1] = best_player.clone([self.board.pos_size[0][0], self.board.pos_size[0][1]], [self.board.pos_size[1][0], self.board.pos_size[1][1]], self.GL)
        new_population[len(self.players) - 1].is_best = True
        mn = best_player.fitness
        for i in range(0, len(self.players)-1):
            parent = self.select_parent()
            mn = min(mn, parent.fitness)
            new_population[i] = parent.clone([self.board.pos_size[0][0], self.board.pos_size[0][1]], [self.board.pos_size[1][0], self.board.pos_size[1][1]], self.GL)
        assert best_player.fitness - mn < 100.1
        self.players = new_population

    def select_parent(self):
        current_sum = 0
        total_fitness = 0
        # for i in range(0, 100):
        #     self.sorted_list[i][0] *= (100-i)//10
        mx = self.sorted_list[0][0]
        for i in range(0, 100):
            if mx - self.sorted_list[i][0] > 100.0:
                break
            total_fitness += self.sorted_list[i][0]
        pointer = random.uniform(0, total_fitness)
        for fitness, player in self.sorted_list:
            current_sum += fitness
            if current_sum > pointer:
                assert mx - player.fitness < 100.1
                return player

    def calculate_fitness(self):
        for player in self.players:
            self.engine.calculate_fitness(player)

    def find_best_player(self):
        best = 0
        best_player = None
        for player in self.players:
            if best < player.fitness:
                best = player.fitness
                best_player = player
        best_player.is_best = True
        return best_player

    def mutate(self):
        for i in range(0, len(self.players)-1):
            self.players[i].mutate()
