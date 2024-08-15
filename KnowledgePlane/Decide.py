# -*- coding: utf-8 -*-
'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July/August 2024
    DECIDE MODULE: Based on the insights from the Orient Module, this module 
    determines the most optimal path to reroute traffic given the external stochastic
    disruptions.
'''

import numpy as np                             #Numerical operations
import tensorflow as tf                        #Use TensorFlow for building and training the neural network
from tensorflow.keras.models import Sequential #Sequential is used to build the model layer by layer
from tensorflow.keras.layers import Dense      #Type of neural network (Dense)
from collections import deque                  #Deque creates a memory buffer to store experiences
import random                                  #Random number generation (For the Agent exploration process)


#Define parameters
state_size = 196         #Capture the number of inputs (or features) the model takes
action_size = 5          #Set of discrete actions that the Agent can take
gamma = 0.95             #Discounted rate for future rewards
epsilon = 1.0            #Initial Exploration rate
epsilon_min = 0.01       #Minimum value for the Exploration rate 
epsilon_decay = 0.995    #Epsilon decay over time
learning_rate = 0.001    #Model learning speed (controls how big of a step the optimizer takes during learning)
batch_size = 32          #Number of samples to use in a single training epoch
memory_size = 2000       #Number of experiences to remember


#Define the Deep Q-Network Model - Acts like the brain of the DECIDE Model that should perform self-healing
def build_model():
    model=Sequential() #Defines the model as a sequence of layers where each layer feeds into the next one
    model.add(Dense(24, input_dim=state_size,activation='relu')) # Hidden layer 1: fully connected layer with 24 neurons  and an input size based on the state space
    model.add(Dense(24, activation='relu'))  #hidden layer 2: continues to process data from hidden layer 1
    model.add(Dense(action_size,activation='linear'))  #The output represents the different action values 
    model.compile(loss='mse',optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate))
    return model

'''
    Model compilation using mean squared error (measures how well the model's predictions match the actual outcomes during training)
    Uses the Adam optimizer to adjust the weights of the neurons to improve learning using the learning rate defined earlier
'''

#Define the threshold-triggered DQN self-healing agent
class DQNAgent:
    def __init__(self):
        self.model = build_model()
        self.target_model=build_model()
        self.memory = deque(maxlen=memory_size)
        self.epsilon = epsilon
        
    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
        
        
    def act(self,state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory,batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + gamma*np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay
            
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

#Threshold-triggered DQN self-healing process
class SelfHealingAgent:
    def __init__(self,qos_requirements):
        self.qos_requirements = qos_requirements
        self.agent = DQNAgent()
        
    def check_violation(self,state):
        TM_t, tau_t = state
        latency_threshold, utilization_threshold, temperature_threshold = self.qos_requirements
        latency_violated = np.any(TM_t[:,1] > latency_threshold)
        utilization_violated = np.any(TM_t[:,0] > utilization_threshold)
        temperature_violated = np.any(tau_t > temperature_threshold)
        
        return latency_violated or utilization_violated or temperature_violated
    
    
    def run(self,get_current_state):
        while True:
            state = get_current_state()
            state = np.reshape(state, [1,state_size])
            if self.check_violation(state):
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
        Create the customized environment based on the violation thresholds from the ABSTRACTION module
        Obtain the real-time network state (s_t) from the knowledge base defining the traffic matrix and temperature matrix
        Call the self-healing function to use these values as an input 
    '''
    qos_requirements = (100, 80, 70)  #latency, utilization, and temperature thresholds respectively
    self_healing_agent = SelfHealingAgent(qos_requirements)
    
    def get_current_state():
        TM_t = np.random.rand(10,2) #read from the OBSERVE Module
        tau_t = np.random.rand(10)  # Temperature matrix (tau_t)
        return TM_t, tau_t
    
    self_healing_agent.run(get_current_state)
        
        
        
        
        
        
        
        
        
        
        
        
        