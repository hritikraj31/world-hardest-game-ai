import tensorflow as tf


def agent(self, input_dim, output_dim):
    learning_rate = 0.001
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(30, input_shape=input_dim, activation='relu'))
    model.add(tf.keras.layers.Dense(15, activation='relu'))
    model.add(tf.keras.layers.Dense(output_dim, activation='linear'))
    model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.keras.optimizers.Adam(learning_rate),
                  metrics=['accuracy'])
    return model


class DQNAgent:

    def __init__(self, observation_dim, action_dim):
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self.model = self.agent(observation_dim, action_dim)



    def predict(self):
        pass


