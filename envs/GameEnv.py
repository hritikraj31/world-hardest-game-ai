import time

import gym
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
        self.action_space = spaces.Discrete(5)
        # self.observation_space = spaces.Box()
        self.render_mode = render_mode

    def step(self, action):
        result = self.engine.move(action)
        if result == -1 or result == 1:
            if self.render_mode == 'human':
                self.render(self.render_mode)
                time.sleep(0.5)
            return 1
        if self.render_mode == 'human':
            self.render(self.render_mode)
        return 0

    def reset(self):
        self.board = Board()
        self.engine = Engine(self.board)
        self.render()

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
