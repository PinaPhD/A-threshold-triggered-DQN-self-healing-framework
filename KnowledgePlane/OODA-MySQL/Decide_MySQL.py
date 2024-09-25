# -*- coding: utf-8 -*-
'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July/August 2024
    DECIDE MODULE: Based on the insights from the Orient Module, this module 
    determines the most optimal path to reroute traffic given the external stochastic
    disruptions.
'''

#Connect to the OBSERVE Module
from Observe import current_network_state      # Loads the current network state from the OBSERVE Module

'''
    Reading the current network state from the OBSERVE Module
    Obtain the real-time network state (s_t) from the knowledge base defining the traffic matrix and temperature matrix
    Call the self-healing function to use these values as an input
'''

     
devices, links, hosts, flows, port_stats, paths = current_network_state()

# Action Space Row vector (RR)
#pwt = len(paths)       # Number of paths between the select source and destination 
#fht = len(flows)       # Number of flows transmitting the ETH-TYPE for a particular service type classification (IEC61850SV, GOOSE, IPV4-->>TCP/UDP, etc...)

# DNN Input parameters
state_size = len(devices) + len(links) + len(hosts)   # Capture the number of inputs (or features) the model takes
action_size = 3                                       # Set of discrete actions that the Agent can take


#Importing the relevant modules

import numpy as np                        
import tensorflow as tf                        # Use TensorFlow for building and training the neural network
from tensorflow.keras.models import Sequential # Sequential is used to build the model layer by layer
from tensorflow.keras.layers import Dense, Input # Input layer added explicitly
from collections import deque                  # Deque creates a memory buffer to store experiences
import random                                  # Random number generation (For the Agent exploration process)
import matplotlib.pyplot as plt
import psutil  # To track CPU and memory usage
   
#import pandas as pd 
#from datetime import datetime
#import time 


# Define DQN self-healing module parameters
gamma = 0.995            # Discounted rate for future rewards
epsilon = 1.0            # Initial Exploration rate
epsilon_min = 0.01       # Minimum value for the Exploration rate 
epsilon_decay = 0.995    # Epsilon decay over time
learning_rate = 0.001    # Model learning speed (controls how big of a step the optimizer takes during learning)
batch_size = 32          # Number of samples to use in a single training epoch
memory_size = 2000       # Number of experiences to remember
episodes = 1500          # Number of episodes for training


# Lists to store training statistics
reward_list = []
cpu_usage_list = []
memory_usage_list = []
epsilon_list = []  # List to store epsilon decay

# Define the Deep Q-Network Model - Acts like the brain of the DECIDE Model that should perform self-healing
def build_model():
    model = Sequential()
    model.add(Input(shape=(state_size,)))     # Explicit Input layer added to avoid the Keras warning
    model.add(Dense(24, activation='relu'))   # Hidden layer 1: fully connected layer with 24 neurons
    model.add(Dense(24, activation='relu'))   # Hidden layer 2: continues to process data from hidden layer 1
    model.add(Dense(action_size, activation='linear'))  # Output layer represents the different action values 
    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate))
    return model

'''
    Model compilation using mean squared error (measures how well the model's predictions match the actual outcomes during training)
    Uses the Adam optimizer to adjust the weights of the neurons to improve learning using the learning rate defined earlier
'''

# Define the DQN agent
class DQNAgent:
    def __init__(self):
        self.model = build_model()  # Primary model
        self.target_model = build_model()  # Target model for stable learning
        self.memory = deque(maxlen=memory_size)  # Experience replay buffer
        self.epsilon = epsilon  # Exploration rate

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

# Self-healing agent that tracks performance
class SelfHealingAgent:
    def __init__(self, qos_requirements):
        self.qos_sla_requirements = qos_requirements
        self.agent = DQNAgent()

    def check_violation(self, l_t, u_t, tau_t):
        latency_threshold, utilization_threshold, temperature_threshold = self.qos_sla_requirements
        latency_violated = np.any(l_t > latency_threshold)
        utilization_violated = np.any(u_t > utilization_threshold)
        temperature_violated = np.any((tau_t < temperature_threshold[0]) | (tau_t > temperature_threshold[-1]))
        return latency_violated or utilization_violated or temperature_violated

    def run(self, get_current_state):
        for episode in range(episodes):
            total_reward = 0  # Initialize reward
            l_t, u_t, tau_t = get_current_state()  # Get network state
            state = np.concatenate((l_t, u_t, tau_t))  # Concatenate the arrays
            state = np.reshape(state, [1, state_size])  # Reshape the state

            # Track CPU and memory usage
            cpu_usage_list.append(psutil.cpu_percent())
            memory_usage_list.append(psutil.virtual_memory().percent)

            if self.check_violation(l_t, u_t, tau_t):
                action = self.agent.act(state)
                next_state, reward, done = self.take_action(action)
                next_state = np.reshape(next_state, [1, state_size])
                self.agent.remember(state, action, reward, next_state, done)
                self.agent.replay()
                self.agent.update_target_model()
                total_reward += reward
            else:
                continue

            # Store the total reward for the episode
            reward_list.append(total_reward)

            # Store the current epsilon value for tracking decay
            epsilon_list.append(self.agent.epsilon)

    def take_action(self, action):
        next_state = np.random.rand(state_size)
        reward = 1
        done = False
        return next_state, reward, done


# Plot function for tracking
def plot_training_stats():
    fig, axs = plt.subplots(4, 1, figsize=(10, 20))

    # Plot reward curve
    axs[0].plot(reward_list)
    axs[0].set_title('Reward Curve')
    axs[0].set_xlabel('Episodes')
    axs[0].set_ylabel('Total Reward')

    # Plot CPU usage
    axs[1].plot(cpu_usage_list)
    axs[1].set_title('CPU Usage During Training')
    axs[1].set_xlabel('Episodes')
    axs[1].set_ylabel('CPU Usage (%)')

    # Plot memory usage
    axs[2].plot(memory_usage_list)
    axs[2].set_title('Memory Usage During Training')
    axs[2].set_xlabel('Episodes')
    axs[2].set_ylabel('Memory Usage (%)')

    # Plot epsilon decay
    axs[3].plot(epsilon_list)
    axs[3].set_title('Epsilon Decay')
    axs[3].set_xlabel('Episodes')
    axs[3].set_ylabel('Epsilon Value')

    plt.tight_layout()
    plt.show()
        
        
if __name__ == "__main__":
    
    '''
        From the ABSTRACTION Module; the path latency, link utilization, and temperature thresholds are defined. 
        The current network state is compared against these thresholds to check for violations.
    '''
    
    t_thr = np.arange(18, 27.001, 0.01)             # The nominal temperature operating range [ASHRAE,2016]
    l_thr = 3                                       # Path latency threshold
    u_thr = 0.8                                     # Link Utilization threshold
    qos_sla_requirements = (l_thr, u_thr, t_thr)    # Latency (ms), utilization (%), and temperature (0C) thresholds respectively
    self_healing_agent = SelfHealingAgent(qos_sla_requirements)
        
    
   
    # Choosing src-dest pairs for the study based on the offshore WPP data services in Table 2.
    
    def get_current_state():
        u_t = np.random.uniform(0, 0.99, 78)        # The link utilization (from OBSERVE Module)
        l_t = np.random.uniform(0, 10, 60)          # The path latency (from OBSERVE Module)
        tau_t = np.random.uniform(-15, 50, 40)      # The device temperature profiles
        return l_t, u_t, tau_t                      # Fixed return variables
    
    self_healing_agent.run(get_current_state)
    
    # Plot the training stats
    plot_training_stats()