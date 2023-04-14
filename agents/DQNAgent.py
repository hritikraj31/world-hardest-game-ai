import os

import tensorflow as tf
import numpy as np
import random


def make_model(input_dim, output_dim):
    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform()
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(50, input_shape=input_dim, activation='relu', kernel_initializer=init))
    model.add(tf.keras.layers.Dense(20, activation='relu', kernel_initializer=init))
    model.add(tf.keras.layers.Dense(12, activation='relu', kernel_initializer=init))
    model.add(tf.keras.layers.Dense(20, activation='relu', kernel_initializer=init))
    model.add(tf.keras.layers.Dense(output_dim, activation='linear', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.keras.optimizers.Adam(learning_rate),
                  metrics=['accuracy'])
    return model


class DQNAgent:

    def __init__(self, observation_dim, action_dim):
        tf.keras.utils.disable_interactive_logging()
        self.best_reward = -10000000
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self.qnetwork = make_model(observation_dim, action_dim)
        self.target_network = make_model(observation_dim, action_dim)
        if 'model.index' in os.listdir('./output/.'):
            print("Loading saved weights")
            if 'info' in os.listdir('./output/.'):
                file = open('output/info', 'r')
                self.best_reward = max(self.best_reward, float(file.read()))
                print(self.best_reward)
                file.close()
            self.target_network.load_weights('./output/model')
            self.qnetwork.load_weights('./output/model')

    def train(self, replay_buffer):
        discount_factor = 0.72
        learning_rate = 0.65

        MIN_REPLAY_SIZE = 300
        if len(replay_buffer) < MIN_REPLAY_SIZE:
            return

        batch_size = 64 * 2
        mini_batch = random.sample(replay_buffer, batch_size)
        current_states = np.array([transition[0] for transition in mini_batch])
        current_qs_list = self.qnetwork.predict(current_states)
        new_current_states = np.array([transition[3] for transition in mini_batch])
        future_qs_list = self.target_network.predict(new_current_states)

        X = []
        Y = []
        for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
            if not done:
                max_future_q = reward #+ discount_factor * np.max(future_qs_list[index])
            else:
                max_future_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

            X.append(observation)
            Y.append(current_qs)
        self.qnetwork.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

    def save(self, reward):
        print("Saving Target network")
        if reward > self.best_reward:
            self.best_reward = reward
            file = open('output/info', "w")
            file.write(str(reward))
            file.close()
        self.target_network.save_weights('./output/model')