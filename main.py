from envs.VideoUtility import VideoUtility
import random
import sys
import pygame
from envs.GameEnv import GameEnv

if __name__ == '__main__':

    # video_utility = VideoUtility()
    # env = GameEnv('surface')
    #
    # video_utility.initialize('ep1')
    # for i in range(1, 100):
    #     action = random.randint(0, 4)
    #     end = env.step(action)
    #     video_utility.save_image('img_{}.jpeg'.format(i), env.render('surface'))
    #     if end:
    #         break
    #
    # video_utility.compile_images()
    # env.close()

    end = False
    action = 0

    def get_input():
        global end, action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = 1
                elif event.key == pygame.K_UP:
                    action = 2
                elif event.key == pygame.K_LEFT:
                    action = 3
                elif event.key == pygame.K_DOWN:
                    action = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and action == 1:
                    action = 0
                if event.key == pygame.K_UP and action == 2:
                    action = 0
                if event.key == pygame.K_LEFT and action == 3:
                    action = 0
                if event.key == pygame.K_DOWN and action == 4:
                    action = 0
            elif event.type == pygame.QUIT:
                end = True

    env = GameEnv("human")

    while not end:
        end = env.step(action)
        get_input()

    env.close()

    # b = Board()
    # action = 0
    # print("Game Running ...")
    # while True:
    #     b.draw()
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RIGHT:
    #                 action = 1
    #             elif event.key == pygame.K_UP:
    #                 action = 2
    #             elif event.key == pygame.K_LEFT:
    #                 action = 3
    #             elif event.key == pygame.K_DOWN:
    #                 action = 4
    #         elif event.type == pygame.KEYUP:
    #             if event.key == pygame.K_RIGHT and action == 1:
    #                 action = 0
    #             if event.key == pygame.K_UP and action == 2:
    #                 action = 0
    #             if event.key == pygame.K_LEFT and action == 3:
    #                 action = 0
    #             if event.key == pygame.K_DOWN and action == 4:
    #                 action = 0
    #         elif event.type == pygame.QUIT:
    #             b.close()
    #             sys.exit()
    #     if b.engine.move(action) != 0:
    #         b.close()
    #         break
