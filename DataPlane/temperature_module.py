# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 14:11:18 2024

@author: amwangi254 Based on LNAHI Script 
"""

import numpy as np
import matplotlib.pyplot as plt

# Define constants
NUM_SWITCHES = 40  # Based on the provided switches in your file
HEALTHY_TEMP_RANGE = (18, 27)  # Healthy temperature range in °C
TIME_STEPS = 100  # Number of simulation steps
COOLING_RATE = 0.5  # Rate at which the HVAC unit cools down a switch (°C per time step)
HEATING_RATE = 0.3  # Rate at which the HVAC unit heats up a switch (°C per time step)


'''
    Reading the device temperature values (Temperature Module) 
'''
#Connect to the OBSERVE Module
from Observe import current_network_state      # Loads the current network state from the OBSERVE Module


device_id = devices['id'].tolist()    
#Assigning these switches temperature values
temp_values = np.random.uniform(low=10, high=30, size=len(device_id))
device_temp = pd.DataFrame({'id': device_id, 'temperature': temp_values})
#device_temp   #Viewing the device_temp DataFrame

# Initialize temperatures for each switch (randomly between 10 and 35°C)
current_temperatures = np.random.uniform(10, 35, size=NUM_SWITCHES)
temperature_history = np.zeros((NUM_SWITCHES, TIME_STEPS))

# Initialize control signals (1 for cooling, -1 for heating, 0 for no action)
control_signals = np.zeros((NUM_SWITCHES, TIME_STEPS))

# Simulate temperature control over time
for t in range(TIME_STEPS):
    for i in range(NUM_SWITCHES):
        if current_temperatures[i] > HEALTHY_TEMP_RANGE[1]:
            # Switch is overheating, activate cooling
            current_temperatures[i] -= COOLING_RATE
            control_signals[i, t] = 1
        elif current_temperatures[i] < HEALTHY_TEMP_RANGE[0]:
            # Switch is too cold, activate heating
            current_temperatures[i] += HEATING_RATE
            control_signals[i, t] = -1
        # Record the temperature
        temperature_history[i, t] = current_temperatures[i]

# Plot temperature profiles for a few switches
plt.figure(figsize=(10, 6))
for i in range(min(NUM_SWITCHES, 5)):  # Plot 5 random switches
    plt.plot(temperature_history[i], label=f'Switch {switches[i]}')

plt.axhline(y=HEALTHY_TEMP_RANGE[0], color='g', linestyle='--', label='Lower Healthy Limit')
plt.axhline(y=HEALTHY_TEMP_RANGE[1], color='r', linestyle='--', label='Upper Healthy Limit')
plt.title('Temperature Profile of Switches')
plt.xlabel('Time (steps)')
plt.ylabel('Temperature (°C)')
plt.legend(loc='best')
plt.show()

# Plot control signals for the same switches
plt.figure(figsize=(10, 6))
for i in range(min(NUM_SWITCHES, 5)):
    plt.plot(control_signals[i], label=f'Switch {switches[i]}')

plt.title('Control Signals to HVAC (1: Cooling, -1: Heating, 0: No Action)')
plt.xlabel('Time (steps)')
plt.ylabel('Control Signal')
plt.legend(loc='best')
plt.show()
