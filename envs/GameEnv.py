import time

import gym
import numpy as np
from gym import spaces

import pygame

from envs.Board import Board
from envs.Engine import Engine

class GameEnv(gym.Env):

    def __init__(self, render_mode):
        self.board = Board()
        self.surf = None
        self.screen = None
        self.clock = None
        self.engine = Engine(self.board)

        self.observation_dim = self.board.get_state().shape
        self.render_mode = render_mode

    def step(self, action):
        terminated, reward = self.engine.move(action)
        self.board.state[0] = self.board.player[0]
        self.board.state[1] = self.board.player[1]
        # for idx, ball in enumerate(self.board.balls):
        #     self.board.state[3 * idx + 2] = ball[0]
        #     self.board.state[3 * idx + 3] = ball[1]
        #     self.board.state[3 * idx + 4] = ball[3]
        if terminated:
            if self.render_mode == 'human':
                self.render(self.render_mode)
                time.sleep(0.5)
            return self.board.get_state(), reward, terminated
        if self.render_mode == 'human':
            self.render(self.render_mode)
        return self.board.get_state(), reward, terminated

    def reset(self):
        self.board = Board()
        self.engine = Engine(self.board)
        return self.board.get_state()

    def render(self, render_mode):
        if self.screen is None and render_mode == 'human':
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('World\'s Hardest Game')
            self.screen = pygame.display.set_mode(self.board.get_dimension())
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.surf = pygame.Surface(self.board.get_dimension())
        self.surf.fill((255, 255, 255))
        self.board.draw(self.surf)

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
