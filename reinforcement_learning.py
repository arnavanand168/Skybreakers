

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import random
from collections import deque
import matplotlib.pyplot as plt

class FlightResourceEnvironment:

    def __init__(self, flight_data):
        self.flight_data = flight_data
        self.current_flight_idx = 0
        self.total_flights = len(flight_data)
        self.resources = {
            'ground_crew': 20,
            'equipment': 15,
            'special_services': 10
        }
        self.max_resources = self.resources.copy()

        self.state_size = 9

        self.action_size = 3

    def reset(self):

        self.current_flight_idx = 0
        self.resources = self.max_resources.copy()
        return self._get_state()

    def _get_state(self):

        if self.current_flight_idx >= self.total_flights:
            return None

        flight = self.flight_data.iloc[self.current_flight_idx]

        state = [
            flight['difficulty_score'],
            flight['load_factor'],
            flight['ground_time_pressure'],
            flight['transfer_bag_ratio'],
            flight['ssr_intensity'],
            flight['is_international'],
            self.resources['ground_crew'] / self.max_resources['ground_crew'],
            self.resources['equipment'] / self.max_resources['equipment'],
            self.resources['special_services'] / self.max_resources['special_services']
        ]

        return np.array(state, dtype=np.float32)

    def step(self, action):

        if self.current_flight_idx >= self.total_flights:
            return None, 0, True

        flight = self.flight_data.iloc[self.current_flight_idx]

        ground_crew_allocation = min(action[0], self.resources['ground_crew'])
        equipment_allocation = min(action[1], self.resources['equipment'])
        special_services_allocation = min(action[2], self.resources['special_services'])

        self.resources['ground_crew'] -= ground_crew_allocation
        self.resources['equipment'] -= equipment_allocation
        self.resources['special_services'] -= special_services_allocation

        reward = self._calculate_reward(flight, ground_crew_allocation,
                                      equipment_allocation, special_services_allocation)

        self.current_flight_idx += 1

        done = self.current_flight_idx >= self.total_flights

        next_state = self._get_state() if not done else None

        return next_state, reward, done

    def _calculate_reward(self, flight, ground_crew, equipment, special_services):

        base_reward = 10 if flight['is_delayed'] == 0 else -5

        difficulty = flight['difficulty_score']
        expected_crew = max(1, int(difficulty * 5))
        expected_equipment = max(1, int(difficulty * 3))
        expected_services = max(1, int(flight['ssr_intensity'] * 3))

        crew_efficiency = 1 - abs(ground_crew - expected_crew) / max(expected_crew, 1)
        equipment_efficiency = 1 - abs(equipment - expected_equipment) / max(expected_equipment, 1)
        services_efficiency = 1 - abs(special_services - expected_services) / max(expected_services, 1)

        efficiency_bonus = (crew_efficiency + equipment_efficiency + services_efficiency) * 5

        conservation_bonus = (self.resources['ground_crew'] +
                            self.resources['equipment'] +
                            self.resources['special_services']) * 0.1

        total_reward = base_reward + efficiency_bonus + conservation_bonus

        return total_reward

class DQNAgent:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.gamma = 0.95

        self.q_network = self._build_model()
        self.target_network = self._build_model()
        self.update_target_network()

    def _build_model(self):

        model = Sequential([
            Dense(64, activation='relu', input_shape=(self.state_size,)),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])

        model.compile(
            optimizer=Adam(learning_rate=self.learning_rate),
            loss='mse'
        )

        return model

    def update_target_network(self):

        self.target_network.set_weights(self.q_network.get_weights())

    def remember(self, state, action, reward, next_state, done):

        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):

        if np.random.random() <= self.epsilon:

            return np.random.randint(0, 3, size=self.action_size)

        q_values = self.q_network.predict(state.reshape(1, -1), verbose=0)
        return np.argmax(q_values[0])

    def replay(self, batch_size=32):

        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states = np.array([e[0] for e in batch])
        actions = np.array([e[1] for e in batch])
        rewards = np.array([e[2] for e in batch])
        next_states = np.array([e[3] for e in batch])
        dones = np.array([e[4] for e in batch])

        current_q_values = self.q_network.predict(states, verbose=0)

        next_q_values = self.target_network.predict(next_states, verbose=0)

        for i in range(batch_size):
            if dones[i]:
                current_q_values[i][actions[i]] = rewards[i]
            else:
                current_q_values[i][actions[i]] = rewards[i] + self.gamma * np.max(next_q_values[i])

        self.q_network.fit(states, current_q_values, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class QLearningAgent:

    def __init__(self, state_size, action_size, learning_rate=0.1, gamma=0.95, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.q_table = {}

    def _get_state_key(self, state):

        state_key = tuple([
            int(state[0] * 10),
            int(state[1] * 10),
            int(state[2] * 10),
            int(state[3] * 10),
            int(state[4] * 10),
            int(state[5]),
            int(state[6] * 10),
            int(state[7] * 10),
            int(state[8] * 10)
        ])
        return state_key

    def act(self, state):

        state_key = self._get_state_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)

        if np.random.random() <= self.epsilon:

            return np.random.randint(0, self.action_size)

        return np.argmax(self.q_table[state_key])

    def update(self, state, action, reward, next_state, done):

        state_key = self._get_state_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)

        if not done:
            next_state_key = self._get_state_key(next_state)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = np.zeros(self.action_size)

            target = reward + self.gamma * np.max(self.q_table[next_state_key])
        else:
            target = reward

        self.q_table[state_key][action] += self.learning_rate * (
            target - self.q_table[state_key][action]
        )

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class RLResourceAllocator:

    def __init__(self, flight_data):
        self.flight_data = flight_data
        self.environment = FlightResourceEnvironment(flight_data)
        self.dqn_agent = DQNAgent(self.environment.state_size, self.environment.action_size)
        self.q_agent = QLearningAgent(self.environment.state_size, self.environment.action_size)

        self.dqn_rewards = []
        self.q_learning_rewards = []

    def train_dqn(self, episodes=100):

        print("Training DQN Agent...")

        for episode in range(episodes):
            state = self.environment.reset()
            total_reward = 0

            while state is not None:

                action = self.dqn_agent.act(state)

                next_state, reward, done = self.environment.step(action)
                total_reward += reward

                self.dqn_agent.remember(state, action, reward, next_state, done)

                self.dqn_agent.replay()

                state = next_state

            self.dqn_rewards.append(total_reward)

            if episode % 10 == 0:
                self.dqn_agent.update_target_network()

            if episode % 20 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward:.2f}, Epsilon: {self.dqn_agent.epsilon:.3f}")

    def train_q_learning(self, episodes=100):

        print("Training Q-Learning Agent...")

        for episode in range(episodes):
            state = self.environment.reset()
            total_reward = 0

            while state is not None:

                action = self.q_agent.act(state)

                next_state, reward, done = self.environment.step(action)
                total_reward += reward

                self.q_agent.update(state, action, reward, next_state, done)

                state = next_state

            self.q_learning_rewards.append(total_reward)

            if episode % 20 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward:.2f}, Epsilon: {self.q_agent.epsilon:.3f}")

    def evaluate_agent(self, agent_type='dqn', episodes=10):

        if agent_type == 'dqn':
            agent = self.dqn_agent
            agent.epsilon = 0
        else:
            agent = self.q_agent
            agent.epsilon = 0

        total_rewards = []

        for episode in range(episodes):
            state = self.environment.reset()
            episode_reward = 0

            while state is not None:
                action = agent.act(state)
                next_state, reward, done = self.environment.step(action)
                episode_reward += reward
                state = next_state

            total_rewards.append(episode_reward)

        return np.mean(total_rewards), np.std(total_rewards)

    def plot_training_progress(self):

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.dqn_rewards)
        plt.title('DQN Training Progress')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(self.q_learning_rewards)
        plt.title('Q-Learning Training Progress')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def get_optimal_policy(self, agent_type='dqn'):

        if agent_type == 'dqn':
            agent = self.dqn_agent
        else:
            agent = self.q_agent

        policy = {}
        state = self.environment.reset()

        while state is not None:
            action = agent.act(state)
            policy[tuple(state)] = action
            state = self.environment._get_state()
            if state is not None:
                self.environment.current_flight_idx += 1

        return policy
