from envs.VideoUtility import VideoUtility
# from agents.DQNAgent import  DQNAgent
import random
import sys
import pygame
import numpy as np
from envs.GameEnv import GameEnv


# def bot_mode():
#     episodes = 20
#
#     video_utility = VideoUtility()
#     env = GameEnv('surface')
#
#     agent = DQNAgent(env.observation_dim, 5)
#     replay_buffer = []
#     max_size = 40960
#
#     for episode in range(1, episodes+1):
#         observation = env.reset()
#         video_utility.initialize('ep{}'.format(episode))
#
#         max_moves = 500
#
#         total_training_reward = 0
#         for move in range(1, max_moves):
#             epsilon = random.random()
#             action = 0
#             if epsilon < 0.2:
#                 action = random.randint(0, 4)
#             else:
#                 fixed_observation = observation
#                 fixed_observation_reshaped = fixed_observation.reshape([1, fixed_observation.shape[0]])
#                 action = np.argmax(agent.qnetwork.predict(fixed_observation_reshaped).flatten())
#             new_observation, reward, terminated = env.step(action)
#             replay_buffer.append((observation, action, reward, new_observation, terminated))
#             if len(replay_buffer) > max_size:
#                 replay_buffer.pop(0)
#             if move % 4 ==0 or terminated:
#                 agent.train(replay_buffer)
#
#             observation = new_observation
#             total_training_reward += reward
#             video_utility.save_image('img_{}.jpeg'.format(move), env.render('surface'))
#             if terminated:
#                 agent.target_network.set_weights(agent.qnetwork.get_weights())
#                 break
#         print(
#             "Episode: {episode}, Total Training reward: {reward}".format(episode=episode, reward=total_training_reward))
#         if episode % 5 == 0:
#             agent.save()
#         video_utility.compile_images()
#
#     env.close()

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
    # video_utility = VideoUtility()
    # env = GameEnv('surface')
    #
    # video_utility.initialize('ep1')
    # for i in range(1, 100):
    #     action = random.randint(0, 4)
    #     end = env.step()
    #     video_utility.save_image('img_{}.jpeg'.format(i), env.render('surface'))
    #     if end:
    #         break
    #
    # video_utility.compile_images()
    # env.close()



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
