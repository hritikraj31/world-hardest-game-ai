from envs.VideoUtility import VideoUtility
import pygame
from envs.GameEnv import GameEnv


def human_mode():
    terminated = False
    action = 0

    def get_input():
        global terminated, action
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
                terminated = True

    env = GameEnv("human")

    while not terminated:
        reward, terminated = env.step(action)
        get_input()

    env.close()

def test_mode():
    env = GameEnv('surface')
    video_utility = VideoUtility()
    stop = False
    count = 0
    video_utility.initialize('gen0')
    mod = 5
    while not stop:
        env.step()
        count += 1
        if env.count_alive > 0 and env.generation % mod == 0:
            env.render('human')
            if env.generation % mod == 0:
                video_utility.save_image('img_{}.jpeg'.format(count), env.render('surface'))
        if env.count_alive < 1:
            count = 0
            if env.generation % mod == 0:
                video_utility.compile_images()
            env.calculate_fitness()
            env.natural_selection()
            env.mutate()
            if env.generation % mod == 1:
                video_utility.initialize('gen{}'.format(env.generation+mod-1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
    env.close()


if __name__ == '__main__':
    test_mode()