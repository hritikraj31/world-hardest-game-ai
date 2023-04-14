import os

from envs.VideoUtility import VideoUtility
from agents.DQNAgent import  DQNAgent
import random
import pickle
import pygame
import numpy as np
from envs.GameEnv import GameEnv

def search_mode():
    pass

def bot_mode():
    episodes = 800

    video_utility = VideoUtility()
    env = GameEnv('surface')

    agent = DQNAgent(env.observation_dim, 5)
    replay_buffer = []
    if 'replay_buffer' in os.listdir('output'):
        file = open('output/replay_buffer', "rb")
        replay_buffer = pickle.load(file)
        file.close()
    max_size = 40960

    best_till_now = agent.best_reward
    for episode in range(1, episodes+1):
        observation = env.reset()
        if episode % 5 == 0:
            video_utility.initialize('ep{}'.format(episode))

        max_moves = 300

        total_training_reward = 0
        print("Length of replay buffer {}".format(len(replay_buffer)))
        if len(replay_buffer) > 1000:
            file = open("output/replay_buffer", "wb")
            pickle.dump(replay_buffer, file)
            file.close()
        for move in range(1, max_moves):
            epsilon = random.random()
            action = 0
            if epsilon < 0.1:
                action = random.randint(0, 4)
            else:
                fixed_observation = observation
                fixed_observation_reshaped = fixed_observation.reshape([1, fixed_observation.shape[0]])
                action = np.argmax(agent.qnetwork.predict(fixed_observation_reshaped).flatten())
            new_observation, reward, terminated = env.step(action)
            replay_buffer.append((observation, action, reward, new_observation, terminated))
            if len(replay_buffer) > max_size:
                replay_buffer.remove(random.randint(0, max_size - 1))
            if move % 4 == 0 or terminated:
                agent.train(replay_buffer)

            observation = new_observation
            total_training_reward += reward
            if episode % 5 == 0:
                video_utility.save_image('img_{}.jpeg'.format(move), env.render('surface'))
            if terminated:
                agent.target_network.set_weights(agent.qnetwork.get_weights())
                break
        print(
            "Episode: {episode}, Total Training reward: {reward}".format(episode=episode, reward=total_training_reward))
        if best_till_now < total_training_reward:
            best_till_now = total_training_reward
            agent.target_network.set_weights(agent.qnetwork.get_weights())
            agent.save(best_till_now)
        if episode % 5 == 0:
            video_utility.compile_images()

    env.close()


def generate_progress(agent, episode):
    video_utility = VideoUtility()
    env = GameEnv('surface')

    observation = env.reset()
    video_utility.initialize('ep{}'.format(episode))

    max_moves = 300

    total_training_reward = 0
    for move in range(1, max_moves):
        action = 0
        fixed_observation = observation
        fixed_observation_reshaped = fixed_observation.reshape([1, fixed_observation.shape[0]])
        action = np.argmax(agent.target_network.predict(fixed_observation_reshaped).flatten())
        new_observation, reward, terminated = env.step(action)

        observation = new_observation
        total_training_reward += reward
        video_utility.save_image('img_{}.jpeg'.format(move), env.render('surface'))
        if terminated:
            break
    print(
        "Episode: {episode}, Total Training reward: {reward}".format(episode=episode, reward=total_training_reward))
    video_utility.compile_images()
    env.close()
    return total_training_reward


def human_mode():
    terminated = False
    action = 0

    def get_input():
        nonlocal terminated, action
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
        state, reward, terminated = env.step(action)
        get_input()

    env.close()


if __name__ == '__main__':
    bot_mode()
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
