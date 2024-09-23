# -*- coding: utf-8 -*-
'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July/August 2024
    DECIDE MODULE: Based on the insights from the Orient Module, this module 
    determines the most optimal path to reroute traffic given the external stochastic
    disruptions.
'''

import numpy as np                             
import tensorflow as tf                        # Use TensorFlow for building and training the neural network
from tensorflow.keras.models import Sequential # Sequential is used to build the model layer by layer
from tensorflow.keras.layers import Dense      # Type of neural network (Dense)
from collections import deque                  # Deque creates a memory buffer to store experiences
import random                                  # Random number generation (For the Agent exploration process)
from Observe import current_network_state      # Loads the current network state from the OBSERVE Module



# Define parameters
state_size = 178         # Capture the number of inputs (or features) the model takes
action_size = 900          # Set of discrete actions that the Agent can take
gamma = 0.995            # Discounted rate for future rewards
epsilon = 1.0            # Initial Exploration rate
epsilon_min = 0.01       # Minimum value for the Exploration rate 
epsilon_decay = 0.995    # Epsilon decay over time
learning_rate = 0.001    # Model learning speed (controls how big of a step the optimizer takes during learning)
batch_size = 32          # Number of samples to use in a single training epoch
memory_size = 2000       # Number of experiences to remember


# Define the Deep Q-Network Model - Acts like the brain of the DECIDE Model that should perform self-healing
def build_model():
    model = Sequential() # Defines the model as a sequence of layers where each layer feeds into the next one
    model.add(Dense(24, activation='relu', input_shape=(state_size,))) # Hidden layer 1: fully connected layer with 24 neurons and an input size based on the state space
    model.add(Dense(24, activation='relu'))  # Hidden layer 2: continues to process data from hidden layer 1
    model.add(Dense(action_size, activation='linear'))  # The output represents the different action values 
    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate))
    return model

'''
    Model compilation using mean squared error (measures how well the model's predictions match the actual outcomes during training)
    Uses the Adam optimizer to adjust the weights of the neurons to improve learning using the learning rate defined earlier
'''

# Define the threshold-triggered DQN self-healing agent
class DQNAgent:
    def __init__(self):
        self.model = build_model()                # The primary DNN model
        self.target_model = build_model()         # Create a secondary memory (Q-target) for stable learning
        self.memory = deque(maxlen=memory_size)   # Creates an experience replay (using deque) for storing experiences
        self.epsilon = epsilon                    # Exploration rate
        
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


# A threshold-triggered DQN self-healing process
class SelfHealingAgent:
    def __init__(self, qos_requirements):
        self.qos_sla_requirements = qos_requirements  # Corrected variable name
        self.agent = DQNAgent()
        
    def check_violation(self, l_t, u_t, tau_t):
        latency_threshold, utilization_threshold, temperature_threshold = self.qos_sla_requirements
        
        # Latency and utilization violation logic remains the same
        latency_violated = np.any(l_t > latency_threshold)
        utilization_violated = np.any(u_t > utilization_threshold)

        # Temperature violation: check each value in tau_t against the range of t_thr
        temperature_violated = np.any((tau_t < temperature_threshold[0]) | (tau_t > temperature_threshold[-1]))
        
        return latency_violated or utilization_violated or temperature_violated

    
    def run(self, get_current_state):
        while True:
            l_t, u_t, tau_t = get_current_state()  # Get the original tuple
            # Concatenate the arrays to form a single state array for the agent's neural network
            state = np.concatenate((l_t, u_t, tau_t))
            state = np.reshape(state, [1, state_size])  # Reshape after concatenating
            if self.check_violation(l_t, u_t, tau_t):  # Pass original components to check_violation
                action = self.agent.act(state)
                next_state, reward, done = self.take_action(action)
                next_state = np.reshape(next_state, [1, state_size])
                self.agent.remember(state, action, reward, next_state, done)
                self.agent.replay()
                self.agent.update_target_model()
            else:
                continue
            
    def take_action(self, action):
        next_state = np.random.rand(state_size)
        reward = 1
        done = False
        return next_state, reward, done
    
if __name__ == "__main__":
    
    '''
        From the ABSTRACTION Module; the path latency, link utilization, and temperature thresholds are defined. 
        The current network state is compared against these thresholds to check for violations.
    '''
    
    t_thr = np.arange(18, 27.001, 0.01)             #The nominal temperature operating range [ASHRAE,2016]
    l_thr = 3                                       #Path latency threshold
    u_thr = 0.8                                     #Link Utilization threshold
    qos_sla_requirements = (l_thr, u_thr, t_thr)    #Latency (ms), utilization (%), and temperature (0C) thresholds respectively
    self_healing_agent = SelfHealingAgent(qos_sla_requirements)
        
    
    '''
        Reading the current network state from the OBSERVE Module
        Obtain the real-time network state (s_t) from the knowledge base defining the traffic matrix and temperature matrix
        Call the self-healing function to use these values as an input
    '''
    
    devices, links, hosts, flows, port_stats, paths = current_network_state()
    
    #Choosing src-dest pairs for the study based on the offshore WPP data services in Table 2.
    

    pwt = len(paths)      #Number of paths between the select source and destination 
    fht = len(flows)       #Number of flows transmitting the ETH-TYPE for a particular service type classification (IEC61850SV, GOOSE, IPV4-->>TCP/UDP, etc...)
    
    state_size = len(devices)+len(links)+len(hosts)         # Capture the number of inputs (or features) the model takes
    action_size = pwt+fht                                   # Set of discrete actions that the Agent can take

    def get_current_state():
        u_t = np.random.uniform(0, 0.99, 78)        # The link utilization (from OBSERVE Module)
        l_t = np.random.uniform(0, 10, 60)          # The path latency (from OBSERVE Module)
        tau_t = np.random.uniform(-40,50,40)        # The device temperature profiles
        return l_t, u_t, tau_t                      # Fixed return variables
    
    #self_healing_agent.run(get_current_state)

        
        
        
        